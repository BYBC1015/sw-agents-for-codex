#!/usr/bin/env python3
"""Standalone Kling AI API task runner.

This script intentionally uses only the Python standard library so the skill can
be shared as a clean folder without dependency installation.
"""

from __future__ import annotations

import argparse
import base64
import getpass
import hashlib
import hmac
import json
import mimetypes
import os
from pathlib import Path
import re
import subprocess
import sys
import tempfile
import time
from typing import Any
import urllib.error
import urllib.parse
import urllib.request


DEFAULT_BASE_URL = "https://api-beijing.klingai.com"
CONFIG_DIR = Path(os.environ.get("XDG_CONFIG_HOME", Path.home() / ".config")) / "kling-api"
SECRETS_FILE = CONFIG_DIR / "secrets.json"
VALID_KINDS = ("text", "image", "multi-image", "omni")
ENDPOINTS = {
    "text": "text2video",
    "image": "image2video",
    "multi-image": "multi-image2video",
    "omni": "omni-video",
}
CURRENT_ENDPOINTS = {"text": "text-to-video", "image": "image-to-video", "omni": "omni-video"}


class KlingError(RuntimeError):
    pass


def b64url(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).rstrip(b"=").decode("ascii")


def json_dumps(data: Any) -> str:
    return json.dumps(data, ensure_ascii=False, separators=(",", ":"))


def create_jwt(access_key: str, secret_key: str, ttl_seconds: int = 1800) -> str:
    now = int(time.time())
    header = {"alg": "HS256", "typ": "JWT"}
    payload = {"iss": access_key, "exp": now + ttl_seconds, "nbf": now - 5}
    signing_input = f"{b64url(json_dumps(header).encode())}.{b64url(json_dumps(payload).encode())}"
    signature = hmac.new(secret_key.encode("utf-8"), signing_input.encode("ascii"), hashlib.sha256).digest()
    return f"{signing_input}.{b64url(signature)}"


def read_private_config() -> dict[str, str]:
    private: dict[str, str] = {}
    if SECRETS_FILE.exists():
        try:
            loaded = json.loads(SECRETS_FILE.read_text(encoding="utf-8-sig"))
            if not isinstance(loaded, dict):
                raise ValueError("Expected object")
            known = {"api_key", "api_token", "access_key", "secret_key", "base_url"}
            private = {k: v.strip() for k, v in loaded.items() if k in known and isinstance(v, str) and v.strip()}
        except (OSError, ValueError) as exc:
            raise KlingError("Cannot read private Kling config; check its JSON format and permissions.") from exc
    return private


def read_secrets(api_version: str | None = None) -> dict[str, str]:
    """Choose one complete authentication group; never splice file and env keys."""
    private = read_private_config()
    env = {key: os.environ.get("KLING_" + key.upper(), "").strip()
           for key in ("api_key", "api_token", "access_key", "secret_key", "base_url")}
    data = {"base_url": private.get("base_url") or env.get("base_url") or DEFAULT_BASE_URL}
    for source, values in (("private_config", private), ("environment", env)):
        groups = (("api_key",),) if api_version == "current" else (
            ("api_key",), ("api_token",), ("access_key", "secret_key"))
        for group in groups:
            if all(values.get(key) for key in group):
                data.update({key: values[key] for key in group})
                data["auth_source"] = source
                data["auth_mode"] = "ak_sk" if len(group) == 2 else group[0]
                return data
    return data


def restrict_private_file(path: str) -> None:
    """Restrict the still-empty temporary file before any credential bytes are written."""
    if os.name != "nt":
        os.chmod(path, 0o600)
        return
    options = {"capture_output": True, "text": True, "encoding": "utf-8", "errors": "replace", "creationflags": subprocess.CREATE_NO_WINDOW}
    identity = subprocess.run(["whoami", "/user", "/fo", "csv", "/nh"], **options)
    sid = re.search(r"S-1-\d+(?:-\d+)+", identity.stdout)
    if identity.returncode != 0 or not sid:
        raise KlingError("Cannot determine the current Windows user for private file permissions.")
    permissions = subprocess.run(["icacls", path, "/inheritance:r", "/grant:r", f"*{sid.group(0)}:(F)"], **options)
    if permissions.returncode != 0:
        raise KlingError("Cannot restrict Windows private file permissions; no credentials were written.")


def write_secrets(access_key: str = "", secret_key: str = "", base_url: str = DEFAULT_BASE_URL,
                  *, api_key: str = "") -> None:
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    data = read_private_config()
    data.update({"api_key": api_key} if api_key else {"access_key": access_key, "secret_key": secret_key})
    data["base_url"] = base_url
    fd, temporary = tempfile.mkstemp(prefix=".secrets-", suffix=".tmp", dir=CONFIG_DIR)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as stream:
            restrict_private_file(temporary)
            json.dump(data, stream, ensure_ascii=False, indent=2)
        os.replace(temporary, SECRETS_FILE)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)


def redact(value: str | None) -> str:
    return "present" if value else "missing"


def auth_header(api_version: str = "current") -> tuple[str, str]:
    secrets = read_secrets(api_version)
    if api_version == "current":
        token = secrets.get("api_key")
        if not token:
            raise KlingError("Current API requires KLING_API_KEY or setup-key private API Key config; AK/SK requires --api-version legacy.")
        if any(char.isspace() for char in token):
            raise KlingError("Configured API Key contains invalid whitespace.")
        return "Authorization", f"Bearer {token}"
    token = secrets.get("api_key") or secrets.get("api_token")
    if not token:
        ak = secrets.get("access_key")
        sk = secrets.get("secret_key")
        if not ak or not sk:
            raise KlingError("Legacy API requires an API Key, API token, or complete KLING_ACCESS_KEY/KLING_SECRET_KEY pair.")
        token = create_jwt(ak, sk)
    if any(char.isspace() for char in token):
        raise KlingError("Configured API token contains invalid whitespace.")
    return "Authorization", f"Bearer {token}"


def base_url() -> str:
    secrets = read_secrets()
    return secrets.get("base_url") or DEFAULT_BASE_URL


def safe_error(detail: Any, credentials: dict[str, str] | None = None, token: str = "") -> str:
    value = str(detail)
    values = list((credentials or {}).get(key, "") for key in ("api_key", "api_token", "access_key", "secret_key"))
    values.append(token.removeprefix("Bearer "))
    for secret in sorted(filter(None, values), key=len, reverse=True):
        value = value.replace(secret, "[REDACTED]")
    value = re.sub(r"api-key-kling-[A-Za-z0-9_-]+", "[REDACTED]", value)
    value = re.sub(r"(?i)Bearer\s+[^\s\"'<>]+", "Bearer [REDACTED]", value)
    return value[:500]


class NoAuthRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req: Any, fp: Any, code: int, msg: str, headers: Any, newurl: str) -> None:
        raise KlingError("Authenticated API redirects are refused; verify the configured Kling API base URL.")


def request_json(method: str, path: str, body: dict[str, Any] | None = None,
                 api_version: str = "current") -> dict[str, Any]:
    if (api_version == "legacy") != path.startswith("/v1/"):
        raise KlingError("API route and authentication version do not match; no request was sent.")
    url = urllib.parse.urljoin(base_url().rstrip("/") + "/", path.lstrip("/"))
    parsed = urllib.parse.urlsplit(url)
    if parsed.scheme != "https" or parsed.username or parsed.password:
        raise KlingError("Kling API base URL must use HTTPS without embedded credentials.")
    headers = {"Content-Type": "application/json"}
    credentials = read_secrets(api_version)
    name, value = auth_header(api_version)
    headers[name] = value
    data = None if body is None else json.dumps(body, ensure_ascii=False).encode("utf-8")
    req = urllib.request.Request(url, data=data, headers=headers, method=method.upper())
    try:
        with urllib.request.build_opener(NoAuthRedirect()).open(req, timeout=60) as resp:
            raw = resp.read().decode("utf-8", "replace")
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", "replace")
        raise KlingError(f"HTTP {exc.code}: {safe_error(detail, credentials, value)}") from exc
    except urllib.error.URLError as exc:
        raise KlingError(f"Network error: {safe_error(exc, credentials, value)}") from exc
    try:
        payload = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise KlingError("Non-JSON response from Kling API.") from exc
    if not isinstance(payload, dict):
        raise KlingError("Unexpected Kling API response shape.")
    if payload.get("code") not in (0, None):
        raise KlingError(safe_error(f"Kling API error code={payload.get('code')} message={payload.get('message')}", credentials, value))
    return payload


def file_to_base64(path: str, *, preview: bool = False, max_mb: int = 10) -> str:
    p = Path(path)
    if not p.exists():
        raise KlingError(f"Image file not found: {p}")
    if p.stat().st_size > max_mb * 1024 * 1024:
        raise KlingError(f"Image file exceeds official {max_mb}MB limit: {p}")
    mime, _ = mimetypes.guess_type(str(p))
    if mime not in ("image/jpeg", "image/png"):
        raise KlingError("Kling image inputs must be .jpg, .jpeg, or .png")
    return "[LOCAL_IMAGE_BASE64_REDACTED]" if preview else base64.b64encode(p.read_bytes()).decode("ascii")


def read_prompt(args: argparse.Namespace) -> str:
    if args.prompt_file:
        return Path(args.prompt_file).read_text(encoding="utf-8").strip()
    return (args.prompt or "").strip()


def parse_multi_prompt(value: str | None) -> list[dict[str, Any]] | None:
    if not value:
        return None
    raw = Path(value).read_text(encoding="utf-8") if not value.lstrip().startswith("[") and Path(value).exists() else value
    parsed = json.loads(raw)
    if not isinstance(parsed, list):
        raise KlingError("--multi-prompt-json must be a JSON array")
    return parsed


def build_camera_control(args: argparse.Namespace) -> dict[str, Any] | None:
    if not args.camera_type:
        return None
    cam: dict[str, Any] = {"type": args.camera_type}
    config_values = {
        "horizontal": args.camera_horizontal,
        "vertical": args.camera_vertical,
        "pan": args.camera_pan,
        "tilt": args.camera_tilt,
        "roll": args.camera_roll,
        "zoom": args.camera_zoom,
    }
    if args.camera_type == "simple":
        non_zero = {k: v for k, v in config_values.items() if v not in (None, 0)}
        if len(non_zero) != 1:
            raise KlingError("For camera_type=simple, set exactly one non-zero camera config field.")
        cam["config"] = {k: float(v or 0) for k, v in config_values.items()}
    return cam


def model_default(kind: str, explicit: str | None, api_version: str = "current") -> str:
    if api_version == "current":
        expected = "kling-3.0-omni" if kind == "omni" else "kling-3.0"
        aliases = {"kling-v3": "kling-3.0", "kling-v3-omni": "kling-3.0-omni"}
        selected = aliases.get(explicit, explicit) if explicit else expected
        if selected != expected:
            raise KlingError(f"Current {kind} route uses {expected}; use --api-version legacy for older models.")
        return selected
    if explicit:
        return explicit
    if kind == "omni":
        return "kling-v3-omni"
    return "kling-v1-6" if kind == "multi-image" else "kling-v3"


def append_omni_image(image_items: list[dict[str, str]], image: str, frame_type: str | None = None) -> None:
    item = {"image_url": image}
    if frame_type:
        item["type"] = frame_type
    image_items.append(item)


def build_legacy_payload(args: argparse.Namespace, *, preview: bool = False) -> dict[str, Any]:
    def image_data(path: str) -> str:
        return file_to_base64(path, preview=preview)

    kind = args.kind
    if args.video_url and kind != "omni":
        raise KlingError("--video-url requires --kind omni; no video input is accepted by this route.")
    if args.audio or args.resolution or args.video_element_id or args.omni_image_type != "refer_image":
        raise KlingError("--audio/--resolution/--video-element-id/--omni-image-type are current API options.")
    prompt = read_prompt(args)
    payload: dict[str, Any] = {
        "model_name": model_default(kind, args.model_name, "legacy"),
        "negative_prompt": args.negative_prompt or "",
        "duration": str(args.duration),
        "mode": args.mode or "pro",
    }
    if payload["model_name"] in ("kling-v3", "kling-v3-omni"):
        validate_duration(args.duration)
    if args.callback_url:
        payload["callback_url"] = args.callback_url
    if args.external_task_id:
        payload["external_task_id"] = args.external_task_id
    if args.watermark is not None:
        payload["watermark_info"] = {"enabled": args.watermark}

    multi_prompt = parse_multi_prompt(args.multi_prompt_json)
    if args.multi_shot or multi_prompt:
        payload["multi_shot"] = True
        payload["shot_type"] = args.shot_type or "customize"
        if multi_prompt:
            payload["multi_prompt"] = multi_prompt
    else:
        payload["prompt"] = prompt

    if kind in ("text", "multi-image", "omni") and args.aspect_ratio:
        payload["aspect_ratio"] = args.aspect_ratio
    if kind in ("text", "image", "omni") and args.sound:
        payload["sound"] = args.sound
    if args.cfg_scale is not None:
        payload["cfg_scale"] = args.cfg_scale

    camera_control = build_camera_control(args)
    if kind == "omni" and camera_control:
        raise KlingError("Omni-Video does not expose camera_control in the official payload. Put camera movement in the prompt or use video reference.")
    if camera_control:
        payload["camera_control"] = camera_control

    if kind == "image":
        image_url = args.image_url[0] if args.image_url else None
        image_file = args.image_file[0] if args.image_file else None
        image = image_url or (image_data(image_file) if image_file else None)
        image_tail = args.image_tail_url or (image_data(args.image_tail_file) if args.image_tail_file else None)
        if not image and not image_tail:
            raise KlingError("image-to-video requires --image-url/--image-file or --image-tail-url/--image-tail-file.")
        if image:
            payload["image"] = image
        if image_tail:
            payload["image_tail"] = image_tail
        if image_tail and camera_control:
            raise KlingError("Official docs say image_tail and camera_control cannot be used together.")
    elif kind == "multi-image":
        image_items: list[dict[str, str]] = []
        for url in args.image_url or []:
            image_items.append({"image": url})
        for path in args.image_file or []:
            image_items.append({"image": image_data(path)})
        if not image_items:
            raise KlingError("multi-image-to-video requires at least one --image-url or --image-file.")
        if len(image_items) > 4:
            raise KlingError("multi-image-to-video supports at most 4 images.")
        if not prompt and not multi_prompt:
            raise KlingError("multi-image-to-video requires --prompt or --prompt-file.")
        payload["image_list"] = image_items
        payload["prompt"] = prompt
    elif kind == "omni":
        image_items = []
        raw_images: list[str] = []
        for url in args.image_url or []:
            raw_images.append(url)
        for path in args.image_file or []:
            raw_images.append(image_data(path))

        image_tail = args.image_tail_url or (image_data(args.image_tail_file) if args.image_tail_file else None)
        has_typed_frame = False
        if image_tail:
            if not raw_images:
                raise KlingError("Omni-Video end_frame requires a first-frame --image-url/--image-file.")
            append_omni_image(image_items, raw_images[0], "first_frame")
            append_omni_image(image_items, image_tail, "end_frame")
            for image in raw_images[1:]:
                append_omni_image(image_items, image)
            has_typed_frame = True
        else:
            for image in raw_images:
                append_omni_image(image_items, image)

        if image_items:
            if len(image_items) > 7:
                raise KlingError("Omni-Video image/reference items should not exceed 7 in the no-video common case.")
            payload["image_list"] = image_items
        if args.element_id:
            payload["element_list"] = [{"element_id": int(value)} for value in args.element_id]
        if len(image_items) + len(args.element_id or []) > (4 if args.video_url else 7):
            raise KlingError("Omni image + multi-image Element count exceeds the reference limit (4 with video, 7 without).")
        if args.video_url:
            if len(args.video_url) > 1:
                raise KlingError("Omni-Video supports at most one reference/base video URL.")
            if args.sound == "on":
                raise KlingError("Official docs say sound must be off when video_list is provided.")
            payload["video_list"] = [{
                "video_url": args.video_url[0],
                "refer_type": args.video_refer_type,
                "keep_original_sound": args.keep_original_sound,
            }]
        if has_typed_frame or (args.video_url and args.video_refer_type == "base"):
            payload.pop("aspect_ratio", None)
        if args.video_url and args.video_refer_type == "base":
            if has_typed_frame or args.multi_shot or multi_prompt:
                raise KlingError("Base video editing does not support first/last frames or multi-shot generation.")
            payload.pop("duration", None)
        if not prompt and not multi_prompt:
            raise KlingError("Omni-Video requires --prompt/--prompt-file or --multi-prompt-json.")
    else:
        if not prompt and not multi_prompt:
            raise KlingError("text-to-video requires --prompt or --prompt-file.")

    if kind == "multi-image":
        payload.pop("sound", None)
        payload.pop("camera_control", None)
    return {k: v for k, v in payload.items() if v not in ("", None, [])}


def validate_duration(value: str) -> int:
    try:
        duration = int(value)
    except (ValueError, TypeError) as exc:
        raise KlingError("Kling 3.0 duration must be an integer from 3 to 15 seconds.") from exc
    if not 3 <= duration <= 15 or str(duration) != str(value):
        raise KlingError("Kling 3.0 duration must be an integer from 3 to 15 seconds.")
    return duration


def validate_public_url(value: str, label: str) -> str:
    parsed = urllib.parse.urlsplit(value)
    if parsed.scheme not in ("http", "https") or not parsed.netloc or parsed.username or parsed.password:
        raise KlingError(f"{label} requires a public HTTP(S) URL without embedded credentials.")
    return value


def build_current_payload(args: argparse.Namespace, *, preview: bool = False) -> dict[str, Any]:
    kind = args.kind
    if kind not in CURRENT_ENDPOINTS:
        raise KlingError("Current API supports text, image, and omni. Multi-image input uses --kind omni; old multi-image endpoint requires --api-version legacy.")
    model_default(kind, args.model_name)
    if args.cfg_scale is not None or args.camera_type or any((args.camera_horizontal, args.camera_vertical,
            args.camera_pan, args.camera_tilt, args.camera_roll, args.camera_zoom)):
        raise KlingError("Current Kling 3.0 API has no cfg_scale or camera_control; describe camera motion in the prompt.")
    if args.multi_prompt_json or args.shot_type:
        raise KlingError("Current API uses formatted shot prompts; --multi-prompt-json/--shot-type require --api-version legacy.")
    if args.video_url and kind != "omni":
        raise KlingError("--video-url requires --kind omni; no video input is accepted by this route.")
    if args.omni_image_type != "refer_image" and kind != "omni":
        raise KlingError("--omni-image-type requires --kind omni.")
    if kind == "text" and (args.image_url or args.image_file or args.image_tail_url or args.image_tail_file
                            or args.element_id or args.video_element_id):
        raise KlingError("Text-to-video does not accept reference media. Use --kind image or omni.")
    prompt = read_prompt(args)
    if args.negative_prompt:
        prompt = f"{prompt}\nAvoid: {args.negative_prompt}".strip()
    if not prompt or len(prompt) > 3072:
        raise KlingError("Current Kling API requires a prompt of 1 to 3072 characters.")
    duration = validate_duration(args.duration)
    resolution = args.resolution or {"std": "720p", "pro": "1080p", "4k": "4k"}.get(args.mode or "pro")
    if args.resolution and args.mode and args.resolution != {"std": "720p", "pro": "1080p", "4k": "4k"}[args.mode]:
        raise KlingError("--resolution conflicts with --mode. Use --resolution for the current API.")
    audio = args.audio or ("native" if args.sound == "on" else "off")
    if args.audio and args.sound and args.audio != ("native" if args.sound == "on" else "off"):
        raise KlingError("--audio conflicts with --sound. Use --audio for the current API.")
    if args.keep_original_sound == "yes":
        if (args.audio and args.audio != "original") or args.sound == "on":
            raise KlingError("--keep-original-sound conflicts with the requested audio.")
        audio = "original"
    multi_shot = bool(args.multi_shot)
    if kind == "omni" and args.video_url and args.video_refer_type == "feature" and args.multi_shot is None:
        multi_shot = True
    settings: dict[str, Any] = {"resolution": resolution, "duration": duration, "audio": audio,
                                "multi_shot": multi_shot}
    if args.aspect_ratio:
        settings["aspect_ratio"] = args.aspect_ratio
    payload: dict[str, Any] = {"settings": settings}
    options: dict[str, Any] = {}
    if args.callback_url:
        options["callback_url"] = validate_public_url(args.callback_url, "Callback")
    if args.external_task_id:
        options["external_task_id"] = args.external_task_id
    if args.watermark is not None:
        options["watermark_info"] = {"enabled": args.watermark}
    if options:
        payload["options"] = options
    if kind == "text":
        if audio == "original":
            raise KlingError("Original audio requires an Omni base video.")
        payload["prompt"] = prompt
        return payload

    contents: list[dict[str, str]] = [{"type": "prompt", "text": prompt}]
    images = [validate_public_url(url, "Image") for url in args.image_url or []]
    images.extend(file_to_base64(path, preview=preview, max_mb=50) for path in args.image_file or [])
    if args.image_tail_url and args.image_tail_file:
        raise KlingError("Choose one last-frame input: URL or local file.")
    tail = (validate_public_url(args.image_tail_url, "Last frame") if args.image_tail_url else
            file_to_base64(args.image_tail_file, preview=preview, max_mb=50) if args.image_tail_file else None)
    if kind == "image" and len(images) != 1:
        raise KlingError("Current image-to-video requires exactly one first frame; use --kind omni for reference images.")
    typed_frame = kind == "image" or args.omni_image_type == "first_frame" or bool(tail)
    if typed_frame and not images:
        raise KlingError("A last-frame or first-frame mode requires a first-frame image.")
    for index, image in enumerate(images, 1):
        item = {"type": "first_frame" if typed_frame and index == 1 else "refer_image", "url": image}
        if kind == "omni":
            item["id"] = f"image_{index}"
        contents.append(item)
    if tail:
        item = {"type": "last_frame", "url": tail}
        if kind == "omni":
            item["id"] = f"image_{len(images) + 1}"
        contents.append(item)
    multi_elements = args.element_id or []
    video_elements = args.video_element_id or []
    for index, element in enumerate(multi_elements + video_elements, 1):
        if not element.strip():
            raise KlingError("Element IDs must not be empty.")
        contents.append({"type": "element", "element_id": element, "id": f"element_{index}"})
    if typed_frame:
        if len(multi_elements) + len(video_elements) > 3:
            raise KlingError("First-frame generation supports at most 3 Elements.")
        settings.pop("aspect_ratio", None)
    if kind == "image":
        if audio == "original":
            raise KlingError("Original audio requires an Omni base video.")
    else:
        videos = args.video_url or []
        if len(videos) > 1:
            raise KlingError("Omni supports at most one reference/base video.")
        image_count = len(images) + bool(tail)
        if videos:
            if len(video_elements) > 1 or (video_elements and (multi_elements or image_count)):
                raise KlingError("With a reference video, use at most one video-character Element and do not combine it with image references or multi-image Elements.")
            if image_count + len(multi_elements) > 4:
                raise KlingError("With a reference video, image references + multi-image Elements must not exceed 4.")
            contents.append({"type": f"{args.video_refer_type}_video",
                             "url": validate_public_url(videos[0], "Video"), "id": "video_1"})
            if args.video_refer_type == "base":
                if typed_frame or args.multi_shot:
                    raise KlingError("Base video editing does not support first/last frames or multi-shot generation.")
                if audio == "native":
                    raise KlingError("Base video editing supports original or off audio; native audio is unavailable.")
                settings.pop("aspect_ratio", None)
                settings.pop("duration", None)
            elif audio != "off":
                raise KlingError("Feature video reference requires --audio off.")
        else:
            if audio == "original":
                raise KlingError("Original audio requires an Omni base video.")
            if len(video_elements) > 3:
                raise KlingError("Without a reference video, at most 3 video-character Elements are supported.")
            if image_count + len(multi_elements) > (4 if video_elements else 7):
                raise KlingError("Image references + multi-image Elements exceed the Omni limit (4 with video-character Elements, otherwise 7).")
    payload["contents"] = contents
    return payload


def build_payload(args: argparse.Namespace, *, preview: bool = False) -> dict[str, Any]:
    return (build_legacy_payload(args, preview=preview) if args.api_version == "legacy" else
            build_current_payload(args, preview=preview))


def endpoint_path(kind: str, task_id: str | None = None, api_version: str = "current",
                  model_name: str | None = None) -> str:
    if api_version == "current":
        if task_id:
            return "/tasks?" + urllib.parse.urlencode({"task_ids": task_id})
        if kind not in CURRENT_ENDPOINTS:
            raise KlingError("Current API has no legacy multi-image route; use --kind omni.")
        return f"/{CURRENT_ENDPOINTS[kind]}/{model_default(kind, model_name)}"
    endpoint = ENDPOINTS[kind]
    return f"/v1/videos/{endpoint}" + (f"/{urllib.parse.quote(task_id, safe='')}" if task_id else "")


def save_manifest(output_dir: str | Path, manifest: dict[str, Any]) -> Path:
    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)
    path = out / "kling_manifest.json"
    path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    return path


def load_manifest(output_dir: str | Path) -> dict[str, Any]:
    path = Path(output_dir) / "kling_manifest.json"
    if not path.exists():
        raise KlingError(f"No manifest found: {path}")
    return json.loads(path.read_text(encoding="utf-8"))


def extract_data(payload: dict[str, Any], task_id: str | None = None) -> dict[str, Any]:
    data = payload.get("data")
    if isinstance(data, list) and task_id:
        matches = [item for item in data if isinstance(item, dict) and str(item.get("id")) == str(task_id)]
        if len(matches) != 1:
            raise KlingError("Task query did not return exactly one matching task.")
        return matches[0]
    if not isinstance(data, dict):
        raise KlingError("Unexpected task response shape.")
    return data


def find_video_url(data: dict[str, Any]) -> str | None:
    outputs = data.get("outputs")
    if isinstance(outputs, list):
        for output in outputs:
            if isinstance(output, dict) and output.get("type") == "video" and output.get("url"):
                return output["url"]
    result = data.get("task_result") or {}
    videos = result.get("videos") if isinstance(result, dict) else None
    if isinstance(videos, list) and videos:
        first = videos[0]
        if isinstance(first, dict):
            return first.get("url") or first.get("watermark_url")
    return None


def download_file(url: str, output_path: Path) -> None:
    req = urllib.request.Request(url, headers={"User-Agent": "kling-api-skill/1.0"})
    with urllib.request.urlopen(req, timeout=120) as resp:
        output_path.write_bytes(resp.read())


def poll_task(kind: str, task_id: str, output_dir: str | Path, interval: int, timeout: int,
              api_version: str = "current") -> dict[str, Any]:
    if interval <= 0 or timeout <= 0:
        raise KlingError("Poll interval and timeout must be positive.")
    start = time.time()
    last_data: dict[str, Any] = {}
    while True:
        payload = request_json("GET", endpoint_path(kind, task_id, api_version), api_version=api_version)
        data = extract_data(payload, task_id)
        last_data = data
        status = data.get("status") if api_version == "current" else data.get("task_status")
        manifest = {
            "api_version": api_version,
            "kind": kind,
            "task_id": task_id,
            "status": status,
            "response": payload,
            "updated_at_local": int(time.time()),
        }
        save_manifest(output_dir, manifest)
        print(f"status={status} task_id={task_id}")
        if status == ("succeeded" if api_version == "current" else "succeed"):
            video_url = find_video_url(data)
            if video_url:
                output_path = Path(output_dir) / "final.mp4"
                download_file(video_url, output_path)
                manifest["downloaded_video"] = str(output_path)
                manifest["video_url"] = video_url
                save_manifest(output_dir, manifest)
            return manifest
        if status == "failed":
            raise KlingError(safe_error(f"Task failed: {data.get('message') or data.get('task_status_msg') or 'unknown reason'}", read_secrets(api_version)))
        if time.time() - start > timeout:
            return {
                "api_version": api_version,
                "kind": kind,
                "task_id": task_id,
                "status": status,
                "response_data": last_data,
                "timed_out": True,
            }
        time.sleep(interval)


def cmd_setup_key(args: argparse.Namespace) -> int:
    print("Kling API local private key setup.")
    base = args.base_url or DEFAULT_BASE_URL
    validate_public_url(base, "API base URL")
    if urllib.parse.urlsplit(base).scheme != "https":
        raise KlingError("API base URL must use HTTPS.")
    if args.legacy_ak_sk:
        access_key = getpass.getpass("AccessKey: ").strip()
        secret_key = getpass.getpass("SecretKey: ").strip()
        if not access_key or not secret_key:
            raise KlingError("AccessKey and SecretKey are required.")
        write_secrets(access_key, secret_key, base)
    else:
        api_key = (sys.stdin.read() if args.api_key_stdin else getpass.getpass("API Key: ")).strip()
        if not api_key or any(char.isspace() for char in api_key):
            raise KlingError("API Key must be a nonempty single value without whitespace.")
        write_secrets(base_url=base, api_key=api_key)
    print(f"Saved private config: {SECRETS_FILE}")
    print("Keys are not stored in the skill folder.")
    return 0


def cmd_doctor(args: argparse.Namespace) -> int:
    secrets = read_secrets(args.api_version)
    print("Kling API doctor")
    print(f"base_url: {secrets.get('base_url') or DEFAULT_BASE_URL}")
    for key in ("api_key", "access_key", "secret_key", "api_token"):
        print(f"{key}: {redact(secrets.get(key))}")
    print(f"auth_source: {secrets.get('auth_source', 'missing')}")
    print(f"api_version: {args.api_version}")
    try:
        _ = auth_header(args.api_version)
        print("auth: available")
    except KlingError as exc:
        print(f"auth: missing ({exc})")
        return 2
    if args.online:
        if args.api_version != "current":
            raise KlingError("Online doctor is supported for the current API Key only.")
        now_ms = int(time.time() * 1000)
        query = urllib.parse.urlencode({"start_time": now_ms - 3600000, "end_time": now_ms})
        response = request_json("GET", "/account/costs?" + query, api_version="current")
        inner = response.get("data")
        if response.get("code") != 0 or not isinstance(inner, dict) or inner.get("code") != 0:
            raise KlingError("Online authentication response did not confirm success.")
        print("online_auth: verified (read-only account query; no generation)")
    for image_file in args.image_file or []:
        p = Path(image_file)
        print(f"image_file: {p} exists={p.exists()} size={p.stat().st_size if p.exists() else 'n/a'}")
    for image_url in args.image_url or []:
        print(f"image_url: {image_url}")
    return 0


def cmd_dry_run(args: argparse.Namespace) -> int:
    payload = build_payload(args, preview=True)
    print(json.dumps({
        "dry_run": True,
        "base_url": base_url(),
        "method": "POST",
        "path": endpoint_path(args.kind, api_version=args.api_version, model_name=args.model_name),
        "api_version": args.api_version,
        "requires_auth": True,
        "payload": payload,
    }, ensure_ascii=False, indent=2))
    return 0


def cmd_run(args: argparse.Namespace) -> int:
    if not args.yes:
        raise KlingError("Real generation requires --yes after explicit user confirmation.")
    if (args.image_file or args.image_tail_file) and not args.confirm_upload:
        raise KlingError("Local media upload requires --confirm-upload.")
    payload = build_payload(args)
    response = request_json("POST", endpoint_path(args.kind, api_version=args.api_version, model_name=args.model_name),
                            payload, api_version=args.api_version)
    data = extract_data(response)
    task_id = data.get("id") if args.api_version == "current" else data.get("task_id")
    if not task_id:
        raise KlingError("Submit response has no task ID; do not resubmit automatically.")
    status = data.get("status") if args.api_version == "current" else data.get("task_status")
    manifest = {
        "api_version": args.api_version,
        "kind": args.kind,
        "task_id": task_id,
        "status": status,
        "submit_response": response,
        "submitted_at_local": int(time.time()),
        "base_url": base_url(),
    }
    save_manifest(args.output_dir, manifest)
    print(f"submitted task_id={task_id} status={status}")
    if args.submit_only:
        return 0
    final_manifest = poll_task(args.kind, task_id, args.output_dir, args.poll_interval, args.timeout, args.api_version)
    print(json.dumps(final_manifest, ensure_ascii=False, indent=2))
    return 0


def cmd_poll(args: argparse.Namespace) -> int:
    manifest = load_manifest(args.output_dir) if (Path(args.output_dir) / "kling_manifest.json").exists() else {}
    api_version = args.api_version or manifest.get("api_version") or ("legacy" if manifest else "current")
    kind = args.kind or manifest.get("kind")
    task_id = args.task_id or manifest.get("task_id")
    if kind not in VALID_KINDS or not task_id:
        raise KlingError("poll requires --kind and --task-id, or an output-dir with kling_manifest.json.")
    final_manifest = poll_task(kind, task_id, args.output_dir, args.poll_interval, args.timeout, api_version)
    print(json.dumps(final_manifest, ensure_ascii=False, indent=2))
    return 0


def add_payload_args(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--api-version", choices=("current", "legacy"), default="current")
    parser.add_argument("--kind", choices=VALID_KINDS, default="text")
    parser.add_argument("--prompt")
    parser.add_argument("--prompt-file")
    parser.add_argument("--negative-prompt", default="")
    parser.add_argument("--model-name")
    parser.add_argument("--duration", default="5")
    parser.add_argument("--mode", choices=("std", "pro", "4k"), help="Legacy mode; current API maps std/pro/4k to 720p/1080p/4k.")
    parser.add_argument("--sound", choices=("on", "off"), help="Legacy sound; current API maps on/off to native/off.")
    parser.add_argument("--resolution", choices=("720p", "1080p", "4k"), help="Current API resolution (default: 1080p).")
    parser.add_argument("--audio", choices=("native", "original", "off"), help="Current API audio (default: off).")
    parser.add_argument("--aspect-ratio", choices=("16:9", "9:16", "1:1"), default="16:9")
    parser.add_argument("--image-url", action="append")
    parser.add_argument("--image-file", action="append")
    parser.add_argument("--image-tail-url")
    parser.add_argument("--image-tail-file")
    parser.add_argument("--omni-image-type", choices=("refer_image", "first_frame"), default="refer_image")
    parser.add_argument("--video-url", action="append")
    parser.add_argument("--video-refer-type", choices=("feature", "base"), default="base")
    parser.add_argument("--keep-original-sound", choices=("yes", "no"), default="no")
    parser.add_argument("--element-id", action="append", help="Multi-image Element ID; prompt alias @element_N in current API.")
    parser.add_argument("--video-element-id", action="append", help="Video-character Element ID (current API only).")
    shots = parser.add_mutually_exclusive_group()
    shots.add_argument("--multi-shot", action="store_true", dest="multi_shot")
    shots.add_argument("--single-shot", action="store_false", dest="multi_shot")
    parser.set_defaults(multi_shot=None)
    parser.add_argument("--shot-type", choices=("customize", "intelligence"))
    parser.add_argument("--multi-prompt-json")
    parser.add_argument("--cfg-scale", type=float)
    parser.add_argument("--camera-type", choices=("simple", "down_back", "forward_up", "right_turn_forward", "left_turn_forward"))
    parser.add_argument("--camera-horizontal", type=float, default=0)
    parser.add_argument("--camera-vertical", type=float, default=0)
    parser.add_argument("--camera-pan", type=float, default=0)
    parser.add_argument("--camera-tilt", type=float, default=0)
    parser.add_argument("--camera-roll", type=float, default=0)
    parser.add_argument("--camera-zoom", type=float, default=0)
    parser.add_argument("--callback-url")
    parser.add_argument("--external-task-id")
    watermark = parser.add_mutually_exclusive_group()
    watermark.add_argument("--watermark", dest="watermark", action="store_true")
    watermark.add_argument("--no-watermark", dest="watermark", action="store_false")
    parser.set_defaults(watermark=None)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Standalone Kling AI official API runner.")
    sub = parser.add_subparsers(dest="command", required=True)

    setup = sub.add_parser("setup-key", help="Save an API Key outside the repository (default: hidden interactive input).")
    setup_mode = setup.add_mutually_exclusive_group()
    setup_mode.add_argument("--api-key-stdin", action="store_true", help="Read the API Key from stdin without displaying it.")
    setup_mode.add_argument("--legacy-ak-sk", action="store_true", help="Interactively configure legacy AccessKey/SecretKey instead.")
    setup.add_argument("--base-url", default=DEFAULT_BASE_URL)
    setup.set_defaults(func=cmd_setup_key)

    doctor = sub.add_parser("doctor", help="Check local configuration and media inputs without calling generation.")
    doctor.add_argument("--image-url", action="append")
    doctor.add_argument("--image-file", action="append")
    doctor.add_argument("--api-version", choices=("current", "legacy"), default="current")
    doctor.add_argument("--online", action="store_true", help="Check API Key authentication with a read-only account-cost query.")
    doctor.set_defaults(func=cmd_doctor)

    dry = sub.add_parser("dry-run", help="Print payload without submitting a task.")
    add_payload_args(dry)
    dry.set_defaults(func=cmd_dry_run)

    run = sub.add_parser("run", help="Submit a real task, then poll and download unless --submit-only is set.")
    add_payload_args(run)
    run.add_argument("--output-dir", default="outputs/kling-task")
    run.add_argument("--submit-only", action="store_true")
    run.add_argument("--poll-interval", type=int, default=20)
    run.add_argument("--timeout", type=int, default=3600)
    run.add_argument("--confirm-upload", action="store_true")
    run.add_argument("--yes", action="store_true")
    run.set_defaults(func=cmd_run)

    poll = sub.add_parser("poll", help="Poll an existing task and download final.mp4 on success.")
    poll.add_argument("--kind", choices=VALID_KINDS)
    poll.add_argument("--api-version", choices=("current", "legacy"), help="Defaults to the version saved in the manifest.")
    poll.add_argument("--task-id")
    poll.add_argument("--output-dir", default="outputs/kling-task")
    poll.add_argument("--poll-interval", type=int, default=20)
    poll.add_argument("--timeout", type=int, default=3600)
    poll.set_defaults(func=cmd_poll)
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        return int(args.func(args) or 0)
    except (KlingError, OSError, ValueError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
