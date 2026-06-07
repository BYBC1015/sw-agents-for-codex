#!/usr/bin/env python3
"""Generate images through OpenRouter for the banana-pro skill.

The script intentionally uses only Python standard-library modules so it can run
inside a fresh Codex workspace without dependency setup.
"""

from __future__ import annotations

import argparse
import base64
import getpass
import json
import mimetypes
import os
from pathlib import Path
import re
import sys
import time
from typing import Any
from urllib import request, error


ENDPOINT = "https://openrouter.ai/api/v1/chat/completions"
DEFAULT_MODEL = "google/gemini-3-pro-image-preview"
DEFAULT_ASPECT_RATIO = "16:9"
DEFAULT_IMAGE_SIZE = "2K"
DEFAULT_OUTPUT_ROOT = "banana_outputs"
DEFAULT_COMPRESS_LIMIT = 1600
DEFAULT_ENV_FILE = Path.home() / ".config" / "banana-pro" / "openrouter.env"


def _read_prompt(args: argparse.Namespace) -> str:
    if args.prompt:
        return args.prompt
    if args.prompt_file:
        return Path(args.prompt_file).read_text(encoding="utf-8")
    raise SystemExit("Provide --prompt or --prompt-file.")


def _slugify(value: str, fallback: str = "banana-image") -> str:
    words = re.findall(r"[A-Za-z0-9]+", value.lower())
    if words:
        base = "-".join(words[:8])
    else:
        cjk = re.findall(r"[\u4e00-\u9fff]", value)
        base = "".join(cjk[:16]) if cjk else fallback
    base = re.sub(r"[-_\s]+", "-", base).strip("-_. ")
    return (base or fallback)[:80]


def _resolve_output_dir(args: argparse.Namespace, prompt: str, stamp: str) -> Path:
    if args.output_dir:
        return Path(args.output_dir)
    slug = _slugify(args.slug or prompt)
    return Path(args.output_root) / f"{slug}-{stamp}"


def _compress_prompt(prompt: str, limit: int) -> tuple[str, bool]:
    if len(prompt) <= limit:
        return prompt, False

    important_terms = (
        "用途", "主体", "场景", "构图", "景别", "镜头", "光线", "色彩", "风格", "画幅",
        "限制", "禁止", "负面", "留白", "一致", "reference", "subject", "scene",
        "composition", "shot", "lens", "lighting", "color", "style", "aspect",
        "negative", "avoid", "no text", "no logo", "continuity",
    )
    lines = [line.strip(" \t-*•") for line in prompt.splitlines() if line.strip()]
    selected = [
        line for line in lines
        if any(term.lower() in line.lower() for term in important_terms)
    ]
    if not selected:
        selected = lines

    compact = "；".join(selected)
    if len(compact) <= limit:
        return compact, True

    constraints = [
        line for line in selected
        if any(term in line.lower() for term in ("禁止", "负面", "negative", "avoid", "no text", "no logo"))
    ]
    head_limit = max(400, limit - 220)
    head = compact[:head_limit].rstrip("；,， ")
    tail = "；".join(constraints)[-200:].lstrip("；,， ")
    if tail:
        return f"{head}；关键限制：{tail}", True
    return head, True


def _retry_prompt(prompt: str) -> str:
    compact, _ = _compress_prompt(prompt, 900)
    return (
        f"{compact}\n"
        "Generate one clean image only. Keep the subject clear, composition simple, no text, no logo, no watermark."
    )


def _data_url_for_file(path: str) -> str:
    file_path = Path(path)
    mime_type = mimetypes.guess_type(file_path.name)[0] or "image/png"
    data = base64.b64encode(file_path.read_bytes()).decode("ascii")
    return f"data:{mime_type};base64,{data}"


def _message_content(prompt: str, references: list[str], reference_urls: list[str]) -> Any:
    if not references and not reference_urls:
        return prompt

    content: list[dict[str, Any]] = [{"type": "text", "text": prompt}]
    for path in references:
        content.append({"type": "image_url", "image_url": {"url": _data_url_for_file(path)}})
    for url in reference_urls:
        content.append({"type": "image_url", "image_url": {"url": url}})
    return content


def _build_payload(args: argparse.Namespace, prompt: str) -> dict[str, Any]:
    return {
        "model": args.model,
        "messages": [
            {
                "role": "user",
                "content": _message_content(prompt, args.reference_image, args.reference_url),
            }
        ],
        "modalities": ["image", "text"],
        "stream": False,
        "image_config": {
            "aspect_ratio": args.aspect_ratio,
            "image_size": args.image_size,
        },
    }


def _headers(api_key: str) -> dict[str, str]:
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    referer = os.environ.get("OPENROUTER_HTTP_REFERER")
    title = os.environ.get("OPENROUTER_X_TITLE")
    if referer:
        headers["HTTP-Referer"] = referer
    if title:
        headers["X-Title"] = title
    return headers


def _read_env_file_key() -> str | None:
    if os.environ.get("BANANA_PRO_DISABLE_USER_ENV_FALLBACK") == "1":
        return None

    env_path = Path(os.environ.get("BANANA_PRO_ENV", str(DEFAULT_ENV_FILE))).expanduser()
    if not env_path.exists():
        return None

    try:
        lines = env_path.read_text(encoding="utf-8").splitlines()
    except OSError:
        return None

    for raw_line in lines:
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        if key.strip() == "OPENROUTER_API_KEY":
            cleaned = value.strip().strip('"').strip("'")
            if cleaned:
                return cleaned
    return None


def _redacted_key_state(api_key: str) -> str:
    if len(api_key) <= 12:
        return f"present:{len(api_key)}"
    return f"{api_key[:6]}...{api_key[-4:]}:{len(api_key)}"


def _write_env_file_key(env_path: Path, api_key: str, force: bool) -> None:
    env_path = env_path.expanduser()
    if env_path.exists() and not force:
        existing = _read_env_file_key()
        if existing:
            raise SystemExit(
                f"Key file already contains OPENROUTER_API_KEY: {env_path}. "
                "Use --force to overwrite it."
            )

    lines: list[str] = []
    if env_path.exists():
        try:
            lines = env_path.read_text(encoding="utf-8").splitlines()
        except OSError:
            lines = []

    updated = False
    next_lines: list[str] = []
    for raw_line in lines:
        if raw_line.strip().startswith("OPENROUTER_API_KEY="):
            next_lines.append(f"OPENROUTER_API_KEY={api_key}")
            updated = True
        else:
            next_lines.append(raw_line)
    if not updated:
        next_lines.append(f"OPENROUTER_API_KEY={api_key}")

    env_path.parent.mkdir(parents=True, exist_ok=True)
    env_path.write_text("\n".join(next_lines).rstrip() + "\n", encoding="utf-8")
    try:
        env_path.chmod(0o600)
    except OSError:
        pass


def _command_setup_key(args: argparse.Namespace) -> int:
    env_path = Path(args.env_file or DEFAULT_ENV_FILE).expanduser()
    if args.from_stdin:
        api_key = sys.stdin.read().strip()
    else:
        print(f"Saving OpenRouter key to local private file: {env_path}", file=sys.stderr)
        api_key = getpass.getpass("Paste OPENROUTER_API_KEY (input hidden): ").strip()

    if not api_key:
        raise SystemExit("Empty key; nothing was saved.")
    if any(char.isspace() for char in api_key):
        raise SystemExit("OPENROUTER_API_KEY must not contain whitespace.")

    _write_env_file_key(env_path, api_key, force=args.force)
    print(json.dumps({
        "status": "key-saved",
        "env_file": str(env_path.resolve()),
        "OPENROUTER_API_KEY": _redacted_key_state(api_key),
    }, ensure_ascii=False))
    return 0


def _read_api_key() -> str | None:
    key = os.environ.get("OPENROUTER_API_KEY")
    if key:
        return key

    key = _read_env_file_key()
    if key:
        return key

    if os.environ.get("BANANA_PRO_DISABLE_USER_ENV_FALLBACK") == "1":
        return None

    if os.name == "nt":
        try:
            import winreg  # type: ignore

            with winreg.OpenKey(winreg.HKEY_CURRENT_USER, "Environment") as env_key:
                value, _ = winreg.QueryValueEx(env_key, "OPENROUTER_API_KEY")
            if isinstance(value, str) and value.strip():
                return value
        except OSError:
            return None
    return None


def _post_json(payload: dict[str, Any], api_key: str, timeout: int) -> dict[str, Any]:
    body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    req = request.Request(ENDPOINT, data=body, headers=_headers(api_key), method="POST")
    try:
        with request.urlopen(req, timeout=timeout) as resp:
            raw = resp.read().decode("utf-8")
    except error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        raise SystemExit(f"OpenRouter HTTP {exc.code}: {detail}") from exc
    except error.URLError as exc:
        raise SystemExit(f"OpenRouter request failed: {exc}") from exc
    return json.loads(raw)


def _save_data_url(data_url: str, output_path: Path) -> None:
    if "," not in data_url:
        raise ValueError("Invalid data URL")
    _, encoded = data_url.split(",", 1)
    output_path.write_bytes(base64.b64decode(encoded))


def _download_url(url: str, output_path: Path, timeout: int) -> None:
    with request.urlopen(url, timeout=timeout) as resp:
        output_path.write_bytes(resp.read())


def _extract_image_urls(result: dict[str, Any]) -> list[str]:
    images: list[str] = []
    for choice in result.get("choices", []):
        message = choice.get("message", {})
        for image in message.get("images", []) or []:
            image_url = image.get("image_url", {})
            url = image_url.get("url")
            if url:
                images.append(url)
    return images


def _guess_extension(url: str) -> str:
    if url.startswith("data:image/jpeg") or url.startswith("data:image/jpg"):
        return ".jpg"
    if url.startswith("data:image/webp"):
        return ".webp"
    return ".png"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate a Banana Pro image via OpenRouter.")
    parser.add_argument("--prompt", help="Final image prompt text.")
    parser.add_argument("--prompt-file", help="UTF-8 file containing the final image prompt.")
    parser.add_argument("--output-dir", help="Directory for payload, response, and images. Overrides --output-root.")
    parser.add_argument("--output-root", default=DEFAULT_OUTPUT_ROOT, help="Root directory used when --output-dir is omitted.")
    parser.add_argument("--slug", help="Optional readable output folder slug.")
    parser.add_argument("--model", default=DEFAULT_MODEL)
    parser.add_argument("--aspect-ratio", default=DEFAULT_ASPECT_RATIO)
    parser.add_argument("--image-size", default=DEFAULT_IMAGE_SIZE, choices=["0.5K", "1K", "2K", "4K"])
    parser.add_argument("--env-file", default=str(DEFAULT_ENV_FILE), help="Private env file containing OPENROUTER_API_KEY.")
    parser.add_argument("--reference-image", action="append", default=[], help="Local reference image path. Repeatable.")
    parser.add_argument("--reference-url", action="append", default=[], help="Remote or data URL reference image. Repeatable.")
    parser.add_argument("--no-compress", dest="compress_prompt", action="store_false", help="Send the full prompt without deterministic compression.")
    parser.add_argument("--compress-limit", type=int, default=DEFAULT_COMPRESS_LIMIT)
    parser.add_argument("--no-retry-on-empty", dest="retry_on_empty", action="store_false", help="Disable one simplified retry when the API returns no image.")
    parser.add_argument("--fast", action="store_true", help="Fast draft mode: 1K default, shorter prompt compression, and no empty-result retry unless rerun manually.")
    parser.add_argument("--dry-run", action="store_true", help="Write payload only; do not call OpenRouter.")
    parser.add_argument("--setup-key", action="store_true", help="Save OPENROUTER_API_KEY to the local private env file and exit.")
    parser.add_argument("--from-stdin", action="store_true", help="Read setup key from stdin. Intended for automation/tests.")
    parser.add_argument("--force", action="store_true", help="Overwrite existing OPENROUTER_API_KEY in the local private env file during --setup-key.")
    parser.add_argument("--timeout", type=int, default=180)
    parser.set_defaults(compress_prompt=True, retry_on_empty=True)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if args.env_file:
        os.environ["BANANA_PRO_ENV"] = args.env_file
    if args.setup_key:
        return _command_setup_key(args)

    if args.fast:
        if "--image-size" not in sys.argv:
            args.image_size = "1K"
        if "--compress-limit" not in sys.argv:
            args.compress_limit = min(args.compress_limit, 1000)
        args.retry_on_empty = False

    prompt = _read_prompt(args).strip()
    if not prompt:
        raise SystemExit("Prompt is empty.")

    stamp = time.strftime("%Y%m%d-%H%M%S")
    output_dir = _resolve_output_dir(args, prompt, stamp)
    output_dir.mkdir(parents=True, exist_ok=True)

    full_prompt_path = output_dir / "banana_prompt_full.txt"
    used_prompt_path = output_dir / "banana_prompt_used.txt"
    full_prompt_path.write_text(prompt, encoding="utf-8")
    prompt_to_send, compressed = _compress_prompt(prompt, args.compress_limit) if args.compress_prompt else (prompt, False)
    used_prompt_path.write_text(prompt_to_send, encoding="utf-8")

    payload = _build_payload(args, prompt_to_send)
    payload_path = output_dir / "openrouter_payload.json"
    payload_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")

    if args.dry_run:
        print(json.dumps({
            "status": "dry-run",
            "payload": str(payload_path.resolve()),
            "prompt_full": str(full_prompt_path.resolve()),
            "prompt_used": str(used_prompt_path.resolve()),
            "settings": {
                "model": args.model,
                "aspect_ratio": args.aspect_ratio,
                "image_size": args.image_size,
                "compressed_prompt": compressed,
                "fast_mode": args.fast,
            },
        }, ensure_ascii=False))
        return 0

    api_key = _read_api_key()
    if not api_key:
        print(json.dumps({
            "status": "missing-key",
            "payload": str(payload_path.resolve()),
            "prompt_full": str(full_prompt_path.resolve()),
            "prompt_used": str(used_prompt_path.resolve()),
            "env": "OPENROUTER_API_KEY",
        }, ensure_ascii=False))
        return 2

    result = _post_json(payload, api_key, args.timeout)
    response_path = output_dir / "openrouter_response.json"
    response_path.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")

    images = _extract_image_urls(result)
    retried = False
    if not images and args.retry_on_empty:
        retry_payload = _build_payload(args, _retry_prompt(prompt_to_send))
        retry_payload_path = output_dir / "openrouter_payload_retry.json"
        retry_payload_path.write_text(json.dumps(retry_payload, ensure_ascii=False, indent=2), encoding="utf-8")
        result = _post_json(retry_payload, api_key, args.timeout)
        response_path = output_dir / "openrouter_response_retry.json"
        response_path.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
        images = _extract_image_urls(result)
        retried = True

    saved: list[str] = []
    for index, url in enumerate(images, start=1):
        output_path = output_dir / f"banana-pro-{stamp}-{index}{_guess_extension(url)}"
        if url.startswith("data:"):
            _save_data_url(url, output_path)
        else:
            _download_url(url, output_path, args.timeout)
        saved.append(str(output_path.resolve()))

    print(json.dumps({
        "status": "ok" if saved else "no-image",
        "payload": str(payload_path.resolve()),
        "response": str(response_path.resolve()),
        "prompt_full": str(full_prompt_path.resolve()),
        "prompt_used": str(used_prompt_path.resolve()),
        "images": saved,
        "images_markdown": [f"![Banana Pro output]({Path(path).as_posix()})" for path in saved],
        "settings": {
            "model": args.model,
            "aspect_ratio": args.aspect_ratio,
            "image_size": args.image_size,
            "compressed_prompt": compressed,
            "retried_on_empty": retried,
            "fast_mode": args.fast,
            "output_dir": str(output_dir.resolve()),
        },
    }, ensure_ascii=False))
    return 0 if saved else 3


if __name__ == "__main__":
    sys.exit(main())
