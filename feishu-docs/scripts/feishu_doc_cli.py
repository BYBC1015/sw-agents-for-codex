#!/usr/bin/env python3
"""SW Feishu/Lark document handoff helper.

The default path is conservative: render local Markdown and dry-run publish
plans without sending content. Real Feishu publishing requires --execute plus
local private app credentials.
"""

from __future__ import annotations

import argparse
import getpass
import json
import os
import re
import stat
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any


DEFAULT_BASE_URL = "https://open.feishu.cn/open-apis"
CONFIG_PATH = Path.home() / ".config" / "sw-feishu" / "config.json"


def configure_stdio() -> None:
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8")
        except Exception:
            pass


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8-sig")


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8", newline="\n")


def read_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    return json.loads(read_text(path))


def write_private_json(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    try:
        path.chmod(stat.S_IRUSR | stat.S_IWUSR)
    except OSError:
        pass


def load_config(path: Path) -> dict[str, str]:
    data = read_json(path)
    return {
        "app_id": os.environ.get("FEISHU_APP_ID") or str(data.get("app_id") or ""),
        "app_secret": os.environ.get("FEISHU_APP_SECRET") or str(data.get("app_secret") or ""),
        "folder_token": os.environ.get("FEISHU_FOLDER_TOKEN") or str(data.get("folder_token") or ""),
        "base_url": (
            os.environ.get("FEISHU_BASE_URL")
            or str(data.get("base_url") or DEFAULT_BASE_URL)
        ).rstrip("/"),
    }


def secret_state(value: str | None) -> str:
    value = (value or "").strip()
    return "missing" if not value else f"present:{len(value)}chars"


def api_post(url: str, payload: dict[str, Any], token: str | None = None, timeout: int = 20) -> dict[str, Any]:
    headers = {"Content-Type": "application/json; charset=utf-8"}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    req = urllib.request.Request(
        url,
        data=json.dumps(payload, ensure_ascii=False).encode("utf-8"),
        headers=headers,
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            body = resp.read().decode("utf-8", errors="replace")
            return {"ok": True, "status": getattr(resp, "status", 200), "json": json.loads(body)}
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        return {"ok": False, "status": exc.code, "error": exc.reason, "body": body[:1000]}
    except (urllib.error.URLError, OSError, json.JSONDecodeError) as exc:
        return {"ok": False, "status": None, "error": str(exc)}


def get_tenant_access_token(config: dict[str, str], timeout: int) -> tuple[bool, str | None, dict[str, Any]]:
    if not config["app_id"] or not config["app_secret"]:
        return False, None, {"error": "missing app_id or app_secret"}
    url = f"{config['base_url']}/auth/v3/tenant_access_token/internal"
    result = api_post(
        url,
        {"app_id": config["app_id"], "app_secret": config["app_secret"]},
        timeout=timeout,
    )
    if not result.get("ok"):
        return False, None, result
    data = result.get("json", {})
    if data.get("code") != 0:
        return False, None, {"status": result.get("status"), "json": data}
    token = data.get("tenant_access_token")
    return bool(token), token, {"status": result.get("status"), "code": data.get("code")}


def clean_title(value: str) -> str:
    return re.sub(r"\s+", " ", value.strip())[:120] or "SW Feishu Handoff"


def heading_level(line: str) -> tuple[int, str] | None:
    match = re.match(r"^(#{1,6})\s+(.+?)\s*$", line)
    if not match:
        return None
    return len(match.group(1)), match.group(2).strip()


def extract_toc(markdown: str) -> list[tuple[int, str]]:
    toc: list[tuple[int, str]] = []
    for line in markdown.splitlines():
        found = heading_level(line)
        if found and found[0] <= 3:
            toc.append(found)
    return toc[:80]


def is_probable_local_path(value: str) -> bool:
    if re.match(r"^[a-zA-Z]+://", value):
        return False
    return bool(re.match(r"^[a-zA-Z]:[\\/]", value) or value.startswith(("/", "./", "../")))


def sanitize_local_paths(text: str, strip_local_paths: bool) -> str:
    def repl_image(match: re.Match[str]) -> str:
        alt = match.group(1).strip() or "image"
        target = match.group(2).strip()
        if is_probable_local_path(target):
            name = Path(target.replace("\\", "/")).name
            if strip_local_paths:
                return f"> Image placeholder: {alt} ({name}; local file not published)"
            return f"> Image placeholder: {alt} ({target}; local file not published)"
        return f"![{alt}]({target})"

    text = re.sub(r"!\[([^\]]*)\]\(([^)]+)\)", repl_image, text)
    if strip_local_paths:
        text = re.sub(r"([A-Za-z]:[\\/][^\s`|)]+)", lambda m: Path(m.group(1).replace("\\", "/")).name, text)
    return text


def render_markdown(source: str, title: str, mode: str, strip_local_paths: bool) -> str:
    body = sanitize_local_paths(source, strip_local_paths=strip_local_paths)
    toc = extract_toc(body)
    lines: list[str] = [f"# {clean_title(title)}", ""]
    lines.append(f"> SW Feishu handoff mode: {mode}.")
    lines.append("> Generated for review/publishing. Confirm privacy before publishing external workspace content.")
    lines.append("")
    if toc:
        lines.append("## Contents")
        lines.append("")
        for level, heading in toc:
            indent = "  " * max(level - 1, 0)
            lines.append(f"{indent}- {heading}")
        lines.append("")
    lines.append("## Document")
    lines.append("")
    lines.append(body.strip())
    lines.append("")
    return "\n".join(lines)


def markdown_to_block_plan(markdown: str) -> list[dict[str, Any]]:
    blocks: list[dict[str, Any]] = []
    in_code = False
    code_lines: list[str] = []

    def flush_code() -> None:
        nonlocal code_lines
        if code_lines:
            blocks.append({"type": "code", "text": "\n".join(code_lines)})
            code_lines = []

    for raw_line in markdown.splitlines():
        line = raw_line.rstrip()
        if line.startswith("```"):
            if in_code:
                flush_code()
                in_code = False
            else:
                in_code = True
            continue
        if in_code:
            code_lines.append(line)
            continue
        if not line.strip():
            continue
        found = heading_level(line)
        if found:
            blocks.append({"type": f"heading{min(found[0], 3)}", "text": found[1]})
            continue
        if line.lstrip().startswith(("- ", "* ")):
            blocks.append({"type": "bullet", "text": line.lstrip()[2:].strip()})
            continue
        ordered = re.match(r"^\s*\d+[.)]\s+(.+)$", line)
        if ordered:
            blocks.append({"type": "ordered", "text": ordered.group(1).strip()})
            continue
        blocks.append({"type": "paragraph", "text": line.strip()})
    if in_code:
        flush_code()
    return blocks


def text_elements(text: str) -> list[dict[str, Any]]:
    return [{"text_run": {"content": text, "text_element_style": {}}}]


def feishu_block(block: dict[str, Any]) -> dict[str, Any]:
    text = block["text"][:4000]
    typ = block["type"]
    if typ == "heading1":
        return {"block_type": 3, "heading1": {"elements": text_elements(text), "style": {}}}
    if typ == "heading2":
        return {"block_type": 4, "heading2": {"elements": text_elements(text), "style": {}}}
    if typ == "heading3":
        return {"block_type": 5, "heading3": {"elements": text_elements(text), "style": {}}}
    if typ == "bullet":
        return {"block_type": 12, "bullet": {"elements": text_elements(text), "style": {}}}
    if typ == "ordered":
        return {"block_type": 13, "ordered": {"elements": text_elements(text), "style": {}}}
    if typ == "code":
        return {"block_type": 14, "code": {"elements": text_elements(text), "style": {}}}
    return {"block_type": 2, "text": {"elements": text_elements(text), "style": {}}}


def create_document(config: dict[str, str], tenant_token: str, title: str, folder_token: str, timeout: int) -> tuple[bool, str | None, dict[str, Any]]:
    payload: dict[str, Any] = {"title": clean_title(title)}
    if folder_token:
        payload["folder_token"] = folder_token
    result = api_post(f"{config['base_url']}/docx/v1/documents", payload, token=tenant_token, timeout=timeout)
    if not result.get("ok"):
        return False, None, result
    data = result.get("json", {})
    if data.get("code") not in (0, None):
        return False, None, {"json": data}
    document = data.get("data", {}).get("document", {}) if isinstance(data.get("data"), dict) else {}
    doc_id = document.get("document_id") or document.get("revision_id") or data.get("data", {}).get("document_id")
    return bool(doc_id), doc_id, {"json": data}


def append_blocks(config: dict[str, str], tenant_token: str, document_id: str, blocks: list[dict[str, Any]], timeout: int) -> dict[str, Any]:
    # Feishu docx uses block children creation under a parent block. The root
    # block is normally the document id for new empty docs. If an app tenant has
    # a different root id behavior, use the rendered Markdown fallback.
    url = f"{config['base_url']}/docx/v1/documents/{urllib.parse.quote(document_id)}/blocks/{urllib.parse.quote(document_id)}/children"
    created = 0
    errors: list[dict[str, Any]] = []
    for idx in range(0, len(blocks), 20):
        children = [feishu_block(block) for block in blocks[idx : idx + 20]]
        result = api_post(url, {"children": children}, token=tenant_token, timeout=timeout)
        if result.get("ok") and result.get("json", {}).get("code") in (0, None):
            created += len(children)
        else:
            errors.append({"batch": idx // 20 + 1, "result": result})
            break
        time.sleep(0.2)
    return {"ok": not errors, "created_blocks": created, "errors": errors}


def cmd_setup(args: argparse.Namespace) -> int:
    config_path = Path(args.config).expanduser()
    existing = read_json(config_path)
    app_secret = args.app_secret or os.environ.get("FEISHU_APP_SECRET") or existing.get("app_secret")
    if not app_secret:
        app_secret = getpass.getpass("Feishu/Lark app secret (hidden): ").strip()
    data = {
        "app_id": args.app_id or os.environ.get("FEISHU_APP_ID") or existing.get("app_id", ""),
        "app_secret": app_secret or "",
        "folder_token": args.folder_token or os.environ.get("FEISHU_FOLDER_TOKEN") or existing.get("folder_token", ""),
        "base_url": (args.base_url or os.environ.get("FEISHU_BASE_URL") or existing.get("base_url") or DEFAULT_BASE_URL).rstrip("/"),
    }
    missing = [key for key in ("app_id", "app_secret") if not data.get(key)]
    if missing:
        print(json.dumps({"ok": False, "missing": missing, "config": str(config_path)}, ensure_ascii=False, indent=2))
        return 2
    write_private_json(config_path, data)
    print(json.dumps({
        "ok": True,
        "config": str(config_path),
        "app_id": secret_state(data["app_id"]),
        "app_secret": secret_state(data["app_secret"]),
        "folder_token": secret_state(data.get("folder_token")),
        "base_url": data["base_url"],
    }, ensure_ascii=False, indent=2))
    return 0


def cmd_doctor(args: argparse.Namespace) -> int:
    config_path = Path(args.config).expanduser()
    config = load_config(config_path)
    report: dict[str, Any] = {
        "ok": True,
        "config": str(config_path),
        "app_id": secret_state(config["app_id"]),
        "app_secret": secret_state(config["app_secret"]),
        "folder_token": secret_state(config["folder_token"]),
        "base_url": config["base_url"],
    }
    missing = [key for key in ("app_id", "app_secret") if not config[key]]
    if missing:
        report["ok"] = False
        report["missing"] = missing
    elif args.no_network:
        report["network"] = "skipped"
    else:
        ok, _token, token_report = get_tenant_access_token(config, args.timeout)
        report["tenant_token"] = "available" if ok else "unavailable"
        report["tenant_token_check"] = token_report
        report["ok"] = ok
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if report["ok"] else 1


def cmd_render(args: argparse.Namespace) -> int:
    input_path = Path(args.input)
    output_path = Path(args.output)
    source = read_text(input_path)
    rendered = render_markdown(
        source,
        title=args.title or input_path.stem,
        mode=args.mode,
        strip_local_paths=args.strip_local_paths,
    )
    write_text(output_path, rendered)
    blocks = markdown_to_block_plan(rendered)
    print(json.dumps({
        "ok": True,
        "output": str(output_path),
        "mode": args.mode,
        "block_count": len(blocks),
        "local_paths_stripped": bool(args.strip_local_paths),
    }, ensure_ascii=False, indent=2))
    return 0


def cmd_publish(args: argparse.Namespace) -> int:
    input_path = Path(args.input)
    source = read_text(input_path)
    rendered = render_markdown(
        source,
        title=args.title or input_path.stem,
        mode=args.mode,
        strip_local_paths=args.strip_local_paths,
    )
    blocks = markdown_to_block_plan(rendered)
    plan = {
        "ok": True,
        "dry_run": not args.execute,
        "input": str(input_path),
        "title": clean_title(args.title or input_path.stem),
        "mode": args.mode,
        "block_count": len(blocks),
        "note": "Use --execute to publish to Feishu/Lark. No content was sent." if not args.execute else "Publishing requested.",
    }
    if not args.execute:
        print(json.dumps(plan, ensure_ascii=False, indent=2))
        return 0

    config_path = Path(args.config).expanduser()
    config = load_config(config_path)
    folder_token = args.folder_token or config["folder_token"]
    ok, tenant_token, token_report = get_tenant_access_token(config, args.timeout)
    if not ok or not tenant_token:
        print(json.dumps({"ok": False, "stage": "tenant_access_token", "detail": token_report}, ensure_ascii=False, indent=2))
        return 1

    created, document_id, create_report = create_document(
        config,
        tenant_token,
        plan["title"],
        folder_token=folder_token,
        timeout=args.timeout,
    )
    if not created or not document_id:
        print(json.dumps({"ok": False, "stage": "create_document", "detail": create_report}, ensure_ascii=False, indent=2))
        return 1

    append_report = append_blocks(config, tenant_token, document_id, blocks, timeout=args.timeout)
    result = {
        "ok": append_report.get("ok", False),
        "document_id": document_id,
        "created_blocks": append_report.get("created_blocks", 0),
        "block_count": len(blocks),
        "append": append_report,
        "fallback": "If block creation fails, use render output and import/paste into Feishu manually.",
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["ok"] else 1


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Render or publish SW handoffs to Feishu/Lark Docs.")
    parser.add_argument("--config", default=str(CONFIG_PATH), help="Private config JSON path.")
    sub = parser.add_subparsers(dest="command", required=True)

    setup = sub.add_parser("setup", help="Save local private Feishu/Lark app config.")
    setup.add_argument("--app-id", default="")
    setup.add_argument("--app-secret", default="")
    setup.add_argument("--folder-token", default="")
    setup.add_argument("--base-url", default=DEFAULT_BASE_URL)
    setup.set_defaults(func=cmd_setup)

    doctor = sub.add_parser("doctor", help="Check local config and optional tenant token access.")
    doctor.add_argument("--no-network", action="store_true")
    doctor.add_argument("--timeout", type=int, default=20)
    doctor.set_defaults(func=cmd_doctor)

    render = sub.add_parser("render", help="Render Feishu-friendly Markdown locally.")
    render.add_argument("--input", required=True)
    render.add_argument("--output", required=True)
    render.add_argument("--title", default="")
    render.add_argument("--mode", choices=["visual-plan", "storyboard", "generic"], default="generic")
    render.add_argument("--strip-local-paths", action="store_true")
    render.set_defaults(func=cmd_render)

    publish = sub.add_parser("publish", help="Dry-run or publish a Markdown handoff to Feishu/Lark.")
    publish.add_argument("--input", required=True)
    publish.add_argument("--title", default="")
    publish.add_argument("--mode", choices=["visual-plan", "storyboard", "generic"], default="generic")
    publish.add_argument("--folder-token", default="")
    publish.add_argument("--strip-local-paths", action="store_true")
    publish.add_argument("--execute", action="store_true", help="Actually publish. Without this flag, publish is a dry-run.")
    publish.add_argument("--timeout", type=int, default=20)
    publish.set_defaults(func=cmd_publish)
    return parser.parse_args()


def main() -> int:
    configure_stdio()
    args = parse_args()
    return int(args.func(args))


if __name__ == "__main__":
    raise SystemExit(main())
