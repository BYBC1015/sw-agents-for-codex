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
import sys
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


def read_secrets() -> dict[str, str]:
    data: dict[str, str] = {}
    if SECRETS_FILE.exists():
        try:
            loaded = json.loads(SECRETS_FILE.read_text(encoding="utf-8"))
            if isinstance(loaded, dict):
                data.update({str(k): str(v) for k, v in loaded.items() if v})
        except Exception as exc:
            raise KlingError(f"Cannot read private config: {SECRETS_FILE} ({exc})") from exc
    if os.environ.get("KLING_ACCESS_KEY"):
        data["access_key"] = os.environ["KLING_ACCESS_KEY"]
    if os.environ.get("KLING_SECRET_KEY"):
        data["secret_key"] = os.environ["KLING_SECRET_KEY"]
    if os.environ.get("KLING_API_TOKEN"):
        data["api_token"] = os.environ["KLING_API_TOKEN"]
    if os.environ.get("KLING_BASE_URL"):
        data["base_url"] = os.environ["KLING_BASE_URL"]
    return data


def write_secrets(access_key: str, secret_key: str, base_url: str) -> None:
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    data = {"access_key": access_key, "secret_key": secret_key, "base_url": base_url}
    SECRETS_FILE.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    try:
        os.chmod(SECRETS_FILE, 0o600)
    except OSError:
        pass


def redact(value: str | None, keep: int = 4) -> str:
    if not value:
        return "missing"
    if len(value) <= keep * 2:
        return "***"
    return f"{value[:keep]}...{value[-keep:]}"


def auth_header() -> tuple[str, str]:
    secrets = read_secrets()
    token = secrets.get("api_token")
    if not token:
        ak = secrets.get("access_key")
        sk = secrets.get("secret_key")
        if not ak or not sk:
            raise KlingError("Missing KLING_ACCESS_KEY/KLING_SECRET_KEY or private setup-key config.")
        token = create_jwt(ak, sk)
    return "Authorization", f"Bearer {token}"


def base_url() -> str:
    secrets = read_secrets()
    return secrets.get("base_url") or DEFAULT_BASE_URL


def request_json(method: str, path: str, body: dict[str, Any] | None = None) -> dict[str, Any]:
    url = urllib.parse.urljoin(base_url().rstrip("/") + "/", path.lstrip("/"))
    headers = {"Content-Type": "application/json"}
    name, value = auth_header()
    headers[name] = value
    data = None if body is None else json.dumps(body, ensure_ascii=False).encode("utf-8")
    req = urllib.request.Request(url, data=data, headers=headers, method=method.upper())
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            raw = resp.read().decode("utf-8", "replace")
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", "replace")
        raise KlingError(f"HTTP {exc.code}: {detail}") from exc
    except urllib.error.URLError as exc:
        raise KlingError(f"Network error: {exc}") from exc
    try:
        payload = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise KlingError(f"Non-JSON response: {raw[:500]}") from exc
    if payload.get("code") not in (0, None):
        raise KlingError(f"Kling API error code={payload.get('code')} message={payload.get('message')}")
    return payload


def file_to_base64(path: str) -> str:
    p = Path(path)
    if not p.exists():
        raise KlingError(f"Image file not found: {p}")
    if p.stat().st_size > 10 * 1024 * 1024:
        raise KlingError(f"Image file exceeds official 10MB limit: {p}")
    mime, _ = mimetypes.guess_type(str(p))
    if mime not in ("image/jpeg", "image/png"):
        raise KlingError("Kling image inputs must be .jpg, .jpeg, or .png")
    return base64.b64encode(p.read_bytes()).decode("ascii")


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


def model_default(kind: str, explicit: str | None) -> str:
    if explicit:
        return explicit
    if kind == "omni":
        return "kling-v3-omni"
    return "kling-v1-6" if kind == "multi-image" else "kling-v2-6"


def append_omni_image(image_items: list[dict[str, str]], image: str, frame_type: str | None = None) -> None:
    item = {"image_url": image}
    if frame_type:
        item["type"] = frame_type
    image_items.append(item)


def build_payload(args: argparse.Namespace) -> dict[str, Any]:
    kind = args.kind
    prompt = read_prompt(args)
    payload: dict[str, Any] = {
        "model_name": model_default(kind, args.model_name),
        "negative_prompt": args.negative_prompt or "",
        "duration": str(args.duration),
        "mode": args.mode,
    }
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
        image = image_url or (file_to_base64(image_file) if image_file else None)
        image_tail = args.image_tail_url or (file_to_base64(args.image_tail_file) if args.image_tail_file else None)
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
            image_items.append({"image": file_to_base64(path)})
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
            raw_images.append(file_to_base64(path))

        image_tail = args.image_tail_url or (file_to_base64(args.image_tail_file) if args.image_tail_file else None)
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
        if not prompt and not multi_prompt:
            raise KlingError("Omni-Video requires --prompt/--prompt-file or --multi-prompt-json.")
    else:
        if not prompt and not multi_prompt:
            raise KlingError("text-to-video requires --prompt or --prompt-file.")

    if kind == "multi-image":
        payload.pop("sound", None)
        payload.pop("camera_control", None)
    return {k: v for k, v in payload.items() if v not in ("", None, [])}


def endpoint_path(kind: str, task_id: str | None = None) -> str:
    endpoint = ENDPOINTS[kind]
    return f"/v1/videos/{endpoint}" + (f"/{task_id}" if task_id else "")


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


def extract_data(payload: dict[str, Any]) -> dict[str, Any]:
    data = payload.get("data")
    if not isinstance(data, dict):
        raise KlingError(f"Unexpected response shape: {payload}")
    return data


def find_video_url(data: dict[str, Any]) -> str | None:
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


def poll_task(kind: str, task_id: str, output_dir: str | Path, interval: int, timeout: int) -> dict[str, Any]:
    start = time.time()
    last_data: dict[str, Any] = {}
    while True:
        payload = request_json("GET", endpoint_path(kind, task_id))
        data = extract_data(payload)
        last_data = data
        status = data.get("task_status")
        manifest = {
            "kind": kind,
            "task_id": task_id,
            "status": status,
            "response": payload,
            "updated_at_local": int(time.time()),
        }
        save_manifest(output_dir, manifest)
        print(f"status={status} task_id={task_id}")
        if status == "succeed":
            video_url = find_video_url(data)
            if video_url:
                output_path = Path(output_dir) / "final.mp4"
                download_file(video_url, output_path)
                manifest["downloaded_video"] = str(output_path)
                manifest["video_url"] = video_url
                save_manifest(output_dir, manifest)
            return manifest
        if status == "failed":
            raise KlingError(f"Task failed: {data.get('task_status_msg') or data}")
        if time.time() - start > timeout:
            return {
                "kind": kind,
                "task_id": task_id,
                "status": status,
                "response_data": last_data,
                "timed_out": True,
            }
        time.sleep(interval)


def cmd_setup_key(args: argparse.Namespace) -> int:
    print("Kling API local private key setup.")
    access_key = getpass.getpass("AccessKey: ").strip()
    secret_key = getpass.getpass("SecretKey: ").strip()
    base = (input(f"Base URL [{DEFAULT_BASE_URL}]: ").strip() or DEFAULT_BASE_URL)
    if not access_key or not secret_key:
        raise KlingError("AccessKey and SecretKey are required.")
    write_secrets(access_key, secret_key, base)
    print(f"Saved private config: {SECRETS_FILE}")
    print("Keys are not stored in the skill folder.")
    return 0


def cmd_doctor(args: argparse.Namespace) -> int:
    secrets = read_secrets()
    print("Kling API doctor")
    print(f"base_url: {secrets.get('base_url') or DEFAULT_BASE_URL}")
    print(f"access_key: {redact(secrets.get('access_key') or os.environ.get('KLING_ACCESS_KEY'))}")
    print(f"secret_key: {redact(secrets.get('secret_key') or os.environ.get('KLING_SECRET_KEY'))}")
    print(f"api_token: {redact(secrets.get('api_token') or os.environ.get('KLING_API_TOKEN'))}")
    try:
        _ = auth_header()
        print("auth: available")
    except KlingError as exc:
        print(f"auth: missing ({exc})")
    for image_file in args.image_file or []:
        p = Path(image_file)
        print(f"image_file: {p} exists={p.exists()} size={p.stat().st_size if p.exists() else 'n/a'}")
    for image_url in args.image_url or []:
        print(f"image_url: {image_url}")
    return 0


def cmd_dry_run(args: argparse.Namespace) -> int:
    payload = build_payload(args)
    print(json.dumps({
        "dry_run": True,
        "base_url": base_url(),
        "method": "POST",
        "path": endpoint_path(args.kind),
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
    response = request_json("POST", endpoint_path(args.kind), payload)
    data = extract_data(response)
    task_id = data.get("task_id")
    if not task_id:
        raise KlingError(f"Submit succeeded but no task_id found: {response}")
    manifest = {
        "kind": args.kind,
        "task_id": task_id,
        "status": data.get("task_status"),
        "submit_response": response,
        "submitted_at_local": int(time.time()),
        "base_url": base_url(),
    }
    save_manifest(args.output_dir, manifest)
    print(f"submitted task_id={task_id} status={data.get('task_status')}")
    if args.submit_only:
        return 0
    final_manifest = poll_task(args.kind, task_id, args.output_dir, args.poll_interval, args.timeout)
    print(json.dumps(final_manifest, ensure_ascii=False, indent=2))
    return 0


def cmd_poll(args: argparse.Namespace) -> int:
    manifest = load_manifest(args.output_dir) if args.output_dir else {}
    kind = args.kind or manifest.get("kind")
    task_id = args.task_id or manifest.get("task_id")
    if kind not in VALID_KINDS or not task_id:
        raise KlingError("poll requires --kind and --task-id, or an output-dir with kling_manifest.json.")
    final_manifest = poll_task(kind, task_id, args.output_dir, args.poll_interval, args.timeout)
    print(json.dumps(final_manifest, ensure_ascii=False, indent=2))
    return 0


def add_payload_args(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--kind", choices=VALID_KINDS, default="text")
    parser.add_argument("--prompt")
    parser.add_argument("--prompt-file")
    parser.add_argument("--negative-prompt", default="")
    parser.add_argument("--model-name")
    parser.add_argument("--duration", default="5")
    parser.add_argument("--mode", choices=("std", "pro", "4k"), default="pro")
    parser.add_argument("--sound", choices=("on", "off"), default="off")
    parser.add_argument("--aspect-ratio", choices=("16:9", "9:16", "1:1"), default="16:9")
    parser.add_argument("--image-url", action="append")
    parser.add_argument("--image-file", action="append")
    parser.add_argument("--image-tail-url")
    parser.add_argument("--image-tail-file")
    parser.add_argument("--video-url", action="append")
    parser.add_argument("--video-refer-type", choices=("feature", "base"), default="base")
    parser.add_argument("--keep-original-sound", choices=("yes", "no"), default="no")
    parser.add_argument("--element-id", action="append")
    parser.add_argument("--multi-shot", action="store_true")
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

    setup = sub.add_parser("setup-key", help="Save AccessKey and SecretKey to a local private config file.")
    setup.set_defaults(func=cmd_setup_key)

    doctor = sub.add_parser("doctor", help="Check local configuration and media inputs without calling generation.")
    doctor.add_argument("--image-url", action="append")
    doctor.add_argument("--image-file", action="append")
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
    except KlingError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
