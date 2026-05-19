#!/usr/bin/env python3
"""Upload local media to the SW public URL relay.

Uses only Python standard library so the skill can be copied between projects.
"""

from __future__ import annotations

import argparse
import getpass
import json
import mimetypes
import os
import secrets
import sys
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any


DEFAULT_CONFIG_FILE = "~/.config/sw-media-uploader/config.json"
DEFAULT_MAX_BYTES = 200 * 1024 * 1024
CATBOX_API_URL = "https://catbox.moe/user/api.php"
LITTERBOX_API_URL = "https://litterbox.catbox.moe/resources/internals/api.php"
TEMPORARY_RELAY_FALLBACKS = {"none", "auto", "litterbox", "catbox"}
VALID_LITTERBOX_TIMES = {"1h", "12h", "24h", "72h"}
DEFAULT_LITTERBOX_TIME = "24h"
ALLOWED_EXTS = {
    ".jpg",
    ".jpeg",
    ".png",
    ".webp",
    ".gif",
    ".mp4",
    ".mov",
    ".webm",
}


class RelayError(RuntimeError):
    pass


class RelayUnavailableError(RelayError):
    pass


def is_server_unavailable_status(status_code: int) -> bool:
    return status_code in {408, 429, 500, 502, 503, 504} or 520 <= status_code <= 524


def is_http_url(value: str) -> bool:
    return value.startswith("http://") or value.startswith("https://")


def normalize_temporary_fallback(value: Any) -> str:
    raw = str(value or "none").strip().lower().replace("_", "-")
    if raw in {"1", "true", "yes", "on", "enabled"}:
        return "auto"
    if raw not in TEMPORARY_RELAY_FALLBACKS:
        raise RelayError(
            f"temporary fallback must be one of {sorted(TEMPORARY_RELAY_FALLBACKS)}, got {raw}"
        )
    return raw


def normalize_litterbox_time(value: Any) -> str:
    raw = str(value or DEFAULT_LITTERBOX_TIME).strip().lower()
    if raw not in VALID_LITTERBOX_TIMES:
        raise RelayError(f"litterbox time must be one of {sorted(VALID_LITTERBOX_TIMES)}, got {raw}")
    return raw


def config_path(value: str | None = None) -> Path:
    raw = value or os.environ.get("SW_RELAY_CONFIG") or DEFAULT_CONFIG_FILE
    return Path(raw).expanduser()


def read_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8-sig"))


def write_json(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    try:
        os.chmod(path.parent, 0o700)
    except OSError:
        pass
    tmp = path.with_name(path.name + ".tmp")
    tmp.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    try:
        os.chmod(tmp, 0o600)
    except OSError:
        pass
    tmp.replace(path)


def token_state(value: str | None) -> str:
    if not value:
        return "missing"
    return f"present:{len(value)}chars"


def load_config(path_arg: str | None = None) -> tuple[dict[str, Any], Path]:
    path = config_path(path_arg)
    data = read_json(path)
    upload_url = (os.environ.get("SW_RELAY_UPLOAD_URL") or data.get("upload_url") or "").strip()
    public_base = (os.environ.get("SW_RELAY_PUBLIC_BASE") or data.get("public_base") or "").strip()
    token = (os.environ.get("SW_RELAY_TOKEN") or data.get("token") or "").strip()
    max_bytes = int(os.environ.get("SW_RELAY_MAX_BYTES") or data.get("max_bytes") or DEFAULT_MAX_BYTES)
    temporary_fallback = normalize_temporary_fallback(
        os.environ.get("SW_RELAY_TEMPORARY_FALLBACK")
        or data.get("temporary_fallback")
        or data.get("temporary_relay_fallback")
        or "none"
    )
    litterbox_time = normalize_litterbox_time(
        os.environ.get("SW_RELAY_LITTERBOX_TIME") or data.get("litterbox_time") or DEFAULT_LITTERBOX_TIME
    )
    return {
        "upload_url": upload_url,
        "public_base": public_base,
        "token": token,
        "max_bytes": max_bytes,
        "temporary_fallback": temporary_fallback,
        "litterbox_time": litterbox_time,
    }, path


def validate_local_file(path: Path, max_bytes: int) -> None:
    if not path.exists() or not path.is_file():
        raise RelayError(f"file does not exist: {path}")
    if path.stat().st_size <= 0:
        raise RelayError(f"file is empty: {path}")
    if path.stat().st_size > max_bytes:
        raise RelayError(f"file exceeds relay max size: {path.stat().st_size} > {max_bytes}")
    ext = path.suffix.lower()
    if ext not in ALLOWED_EXTS:
        raise RelayError(f"unsupported media extension: {ext or '<none>'}")


def build_multipart_form(fields: dict[str, str], file_field_name: str, file_path: Path) -> tuple[bytes, str]:
    boundary = "----swrelay" + secrets.token_hex(16)
    content_type = mimetypes.guess_type(str(file_path))[0] or "application/octet-stream"
    file_bytes = file_path.read_bytes()
    parts: list[bytes] = []
    for name, value in fields.items():
        parts.extend(
            [
                f"--{boundary}\r\n".encode("utf-8"),
                f'Content-Disposition: form-data; name="{name}"\r\n\r\n'.encode("utf-8"),
                str(value).encode("utf-8"),
                b"\r\n",
            ]
        )
    parts.extend(
        [
            f"--{boundary}\r\n".encode("utf-8"),
            (
                f'Content-Disposition: form-data; name="{file_field_name}"; '
                f'filename="{file_path.name}"\r\n'
            ).encode("utf-8"),
            f"Content-Type: {content_type}\r\n\r\n".encode("utf-8"),
            file_bytes,
            b"\r\n",
            f"--{boundary}--\r\n".encode("utf-8"),
        ]
    )
    return b"".join(parts), f"multipart/form-data; boundary={boundary}"


def build_multipart(file_path: Path) -> tuple[bytes, str]:
    return build_multipart_form({}, "file", file_path)


def upload_to_sw(file_path: Path, cfg: dict[str, Any], cfg_path: Path, timeout: int = 120) -> dict[str, Any]:
    if not cfg["upload_url"]:
        raise RelayError(f"upload_url is missing in {cfg_path}")
    if not cfg["token"]:
        raise RelayError(f"upload token is missing in {cfg_path}")
    body, content_type = build_multipart(file_path)
    req = urllib.request.Request(
        cfg["upload_url"],
        data=body,
        headers={
            "Content-Type": content_type,
            "Content-Length": str(len(body)),
            "X-Upload-Token": cfg["token"],
            "Accept": "application/json",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            raw = resp.read()
            status = getattr(resp, "status", 200)
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")[:300]
        err_cls = RelayUnavailableError if is_server_unavailable_status(exc.code) else RelayError
        raise err_cls(f"relay upload failed: HTTP {exc.code}: {detail}") from exc
    except urllib.error.URLError as exc:
        raise RelayUnavailableError(f"relay upload failed: {exc.reason}") from exc
    except OSError as exc:
        raise RelayUnavailableError(f"relay upload failed: {exc}") from exc
    data = json.loads(raw.decode("utf-8"))
    if not data.get("ok") or not data.get("url"):
        raise RelayUnavailableError(f"relay upload returned invalid response: {json.dumps(data, ensure_ascii=False)[:300]}")
    data["http_status"] = status
    data["config_file"] = str(cfg_path)
    data["relay"] = "sw-media-uploader"
    return data


def upload_file(file_path: Path, path_arg: str | None = None, timeout: int = 120) -> dict[str, Any]:
    cfg, cfg_path = load_config(path_arg)
    validate_local_file(file_path, int(cfg["max_bytes"]))
    return upload_to_sw(file_path, cfg, cfg_path, timeout)


def upload_to_litterbox(file_path: Path, litterbox_time: str, timeout: int = 120) -> dict[str, Any]:
    expiry = normalize_litterbox_time(litterbox_time)
    body, content_type = build_multipart_form({"reqtype": "fileupload", "time": expiry}, "fileToUpload", file_path)
    req = urllib.request.Request(
        LITTERBOX_API_URL,
        data=body,
        headers={"Content-Type": content_type, "Content-Length": str(len(body))},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            raw = resp.read().decode("utf-8", errors="replace").strip()
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")[:300]
        raise RelayError(f"Litterbox fallback upload failed: HTTP {exc.code}: {detail}") from exc
    except urllib.error.URLError as exc:
        raise RelayError(f"Litterbox fallback upload failed: {exc.reason}") from exc
    except OSError as exc:
        raise RelayError(f"Litterbox fallback upload failed: {exc}") from exc
    if not is_http_url(raw):
        raise RelayError(f"Litterbox fallback returned invalid response: {raw[:300]}")
    return {"ok": True, "url": raw, "relay": "litterbox", "expires_hint": expiry}


def upload_to_catbox(file_path: Path, timeout: int = 120) -> dict[str, Any]:
    body, content_type = build_multipart_form({"reqtype": "fileupload"}, "fileToUpload", file_path)
    req = urllib.request.Request(
        CATBOX_API_URL,
        data=body,
        headers={"Content-Type": content_type, "Content-Length": str(len(body))},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            raw = resp.read().decode("utf-8", errors="replace").strip()
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")[:300]
        raise RelayError(f"Catbox fallback upload failed: HTTP {exc.code}: {detail}") from exc
    except urllib.error.URLError as exc:
        raise RelayError(f"Catbox fallback upload failed: {exc.reason}") from exc
    except OSError as exc:
        raise RelayError(f"Catbox fallback upload failed: {exc}") from exc
    if not is_http_url(raw):
        raise RelayError(f"Catbox fallback returned invalid response: {raw[:300]}")
    return {"ok": True, "url": raw, "relay": "catbox", "expires_hint": None}


def upload_to_temporary_relay(file_path: Path, fallback: str, litterbox_time: str, timeout: int) -> dict[str, Any]:
    relay = "litterbox" if fallback == "auto" else fallback
    if relay == "litterbox":
        return upload_to_litterbox(file_path, litterbox_time, timeout)
    if relay == "catbox":
        return upload_to_catbox(file_path, timeout)
    raise RelayError("temporary relay fallback is not enabled")


def upload_file_with_priority(
    file_path: Path,
    path_arg: str | None = None,
    timeout: int = 120,
    temporary_fallback: str | None = None,
    litterbox_time: str | None = None,
) -> dict[str, Any]:
    cfg, cfg_path = load_config(path_arg)
    validate_local_file(file_path, int(cfg["max_bytes"]))
    fallback = normalize_temporary_fallback(temporary_fallback or cfg["temporary_fallback"])
    expiry = normalize_litterbox_time(litterbox_time or cfg["litterbox_time"])
    try:
        return upload_to_sw(file_path, cfg, cfg_path, timeout)
    except RelayUnavailableError as exc:
        primary_error = str(exc)
        if fallback == "none":
            raise RelayError(
                "SW media uploader unavailable; temporary relay fallback is not enabled. "
                f"Primary error: {primary_error}"
            ) from exc
        data = upload_to_temporary_relay(file_path, fallback, expiry, timeout)
        data["primary_relay_error"] = primary_error
        data["warning"] = (
            "SW media uploader unavailable; used confirmed temporary relay fallback "
            f"({data['relay']})."
        )
        return data


def command_doctor(args: argparse.Namespace) -> int:
    cfg, path = load_config(args.config)
    checks: list[dict[str, Any]] = [
        {"name": "config_file", "path": str(path), "ok": path.exists()},
        {"name": "upload_url", "ok": bool(cfg["upload_url"]), "value": cfg["upload_url"] or None},
        {"name": "public_base", "ok": bool(cfg["public_base"]), "value": cfg["public_base"] or None},
        {"name": "token", "ok": bool(cfg["token"]), "state": token_state(cfg["token"])},
        {"name": "temporary_fallback", "ok": True, "value": cfg["temporary_fallback"]},
        {"name": "litterbox_time", "ok": True, "value": cfg["litterbox_time"]},
    ]
    if args.file:
        file_path = Path(args.file).expanduser()
        try:
            validate_local_file(file_path, int(cfg["max_bytes"]))
            checks.append({"name": "local_file", "path": str(file_path), "ok": True, "bytes": file_path.stat().st_size})
        except RelayError as exc:
            checks.append({"name": "local_file", "path": str(file_path), "ok": False, "error": str(exc)})
    ok = all(check["ok"] for check in checks)
    print(json.dumps({"ok": ok, "checks": checks}, ensure_ascii=False, indent=2))
    return 0 if ok else 1


def command_upload(args: argparse.Namespace) -> int:
    data = upload_file_with_priority(
        Path(args.file).expanduser(),
        args.config,
        args.timeout,
        args.temporary_relay_fallback,
        args.litterbox_time,
    )
    safe = {
        "ok": True,
        "url": data["url"],
        "relay": data.get("relay"),
        "expires_hint": data.get("expires_hint"),
        "path": data.get("path"),
        "warning": data.get("warning"),
    }
    print(json.dumps(safe, ensure_ascii=False, indent=2))
    return 0


def command_setup(args: argparse.Namespace) -> int:
    path = config_path(args.config)
    token = os.environ.get("SW_RELAY_TOKEN", "").strip()
    if not token:
        token = getpass.getpass("Paste upload token (hidden): ").strip()
    if not token:
        raise RelayError("empty upload token")
    payload = {
        "upload_url": args.upload_url.rstrip("/"),
        "public_base": args.public_base.rstrip("/"),
        "token": token,
        "max_bytes": args.max_bytes,
        "temporary_fallback": normalize_temporary_fallback(args.temporary_relay_fallback),
        "litterbox_time": normalize_litterbox_time(args.litterbox_time),
        "managed_by": "url-relay setup",
    }
    write_json(path, payload)
    print(json.dumps({"ok": True, "config_file": str(path), "token": token_state(token)}, ensure_ascii=False, indent=2))
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Upload local media to the SW public URL relay")
    sub = parser.add_subparsers(dest="command", required=True)

    doctor = sub.add_parser("doctor", help="Check relay config and optional local file")
    doctor.add_argument("--config", default=None)
    doctor.add_argument("--file", default=None)
    doctor.set_defaults(func=command_doctor)

    upload = sub.add_parser("upload", help="Upload a local image/video and print a public URL")
    upload.add_argument("--config", default=None)
    upload.add_argument("--file", required=True)
    upload.add_argument("--timeout", type=int, default=120)
    upload.add_argument(
        "--temporary-relay-fallback",
        choices=sorted(TEMPORARY_RELAY_FALLBACKS),
        default=None,
        help="Use only after SW media uploader fails. 'auto' currently chooses Litterbox.",
    )
    upload.add_argument("--litterbox-time", choices=sorted(VALID_LITTERBOX_TIMES), default=None)
    upload.set_defaults(func=command_upload)

    setup = sub.add_parser("setup", help="Save relay settings to a private local config file")
    setup.add_argument("--config", default=None)
    setup.add_argument("--upload-url", required=True)
    setup.add_argument("--public-base", required=True)
    setup.add_argument("--max-bytes", type=int, default=DEFAULT_MAX_BYTES)
    setup.add_argument("--temporary-relay-fallback", choices=sorted(TEMPORARY_RELAY_FALLBACKS), default="none")
    setup.add_argument("--litterbox-time", choices=sorted(VALID_LITTERBOX_TIMES), default=DEFAULT_LITTERBOX_TIME)
    setup.set_defaults(func=command_setup)
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        return int(args.func(args) or 0)
    except RelayError as exc:
        print(
            json.dumps(
                {
                    "ok": False,
                    "error": str(exc),
                    "fallback": "sw_first_then_confirmed_temporary_relay_or_user_public_url",
                },
                ensure_ascii=False,
                indent=2,
            ),
            file=sys.stderr,
        )
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
