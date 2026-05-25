#!/usr/bin/env python3
"""Synchronize installed SW skills and plugin entries from this repository.

This script is intentionally dependency-free. It keeps runtime SW usage cheap by
moving repetitive file copying and version alignment into a deterministic local
command instead of asking Codex to re-read and repair many paths by hand.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
USERPROFILE = Path(os.environ.get("USERPROFILE", str(Path.home())))
USER_SKILLS = USERPROFILE / ".codex" / "skills"
PLUGIN_ROOT = USERPROFILE / "plugins" / "sw-v1-0"


ENTRY_SKILLS = {
    "sw-v1-0": {
        "source": ROOT / "SW_V1.0.md",
        "description": (
            "Load the SW_V1.0 design studio workflow. Use for /sw, /SW_V1.0, "
            "@SW_V1.0, poster, presentation, video, storyboard, edit-plan, "
            "aesthetic direction, AI prompt, review, revision, and tool-integration projects."
        ),
    },
    "sw-update": {
        "source": ROOT / "sw_update.md",
        "description": (
            "Synchronize the current conversation with the latest SW runtime "
            "version. Use for @sw_update, /sw_update, /sw-update, SW_UPDATE, "
            "or SW_REFRESH."
        ),
    },
    "sw-rescue": {
        "source": ROOT / "sw_rescue.md",
        "description": (
            "Force-refresh SW when old conversations, stale chips, or version "
            "mismatches keep returning an outdated runtime."
        ),
    },
    "sw-help": {
        "source": ROOT / "sw_help.md",
        "description": (
            "Show concise SW feature triggers for Banana Pro, Seedance, URL "
            "Relay, SW Rescue, and Historical Accuracy without starting a project."
        ),
    },
}

TOOL_SKILLS = ["banana-pro", "seedance-2-video", "url-relay", "storyboard-visual-word"]


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8-sig")


def parse_version() -> str:
    text = read_text(ROOT / "VERSION.md")
    match = re.search(r"Current runtime version:\s*(V\d+\.\d+\.\d+)", text)
    if not match:
        raise RuntimeError("VERSION.md has no Current runtime version line")
    return match.group(1)


def write_text(path: Path, text: str, dry_run: bool) -> None:
    old = path.read_text(encoding="utf-8-sig") if path.exists() else None
    if old == text:
        print(f"unchanged: {path}")
        return
    print(f"write: {path}")
    if dry_run:
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8", newline="\n")


def write_json(path: Path, data: dict, dry_run: bool) -> None:
    text = json.dumps(data, ensure_ascii=False, indent=2) + "\n"
    write_text(path, text, dry_run)


def build_skill(skill_id: str) -> str:
    meta = ENTRY_SKILLS[skill_id]
    body = read_text(meta["source"]).strip()
    return (
        "---\n"
        f"name: {skill_id}\n"
        f"description: {meta['description']}\n"
        "---\n\n"
        f"{body}\n\n"
        "## Installed Source\n\n"
        "This installed entry is generated from the SW repository by "
        "`tools/sw_sync_installed.py`. If it conflicts with repository files, "
        "rerun the sync script and then run `tools/sw_doctor.py`.\n"
    )


def fixed_help_reply() -> str:
    return """SW Help:
- Banana Pro: trigger with 香蕉 / banana / Banana Pro / Nano Banana / @banana-pro / 用 banana 出图.
- Seedance 2.0 Video: trigger with 即梦2.0生成 / 即梦生成 / Seedance 2.0 / @seedance-2-video / 用即梦生成视频.
- URL Relay: trigger with URL中转 / 公网URL / 上传参考图 / 上传参考视频 / @url-relay. Used before Seedance when local files need public URLs.
- Storyboard Visual Word: trigger with 视觉方案文件 / 视觉导演方案 / Word视觉方案 / DOCX视觉方案 / @storyboard-visual-word after selected storyboard or scene images are ready.
- Aesthetic Decision: trigger with /aesthetic, "SW decide the look", 自动选择审美, 审美画像, or moodboard direction. Reads the compact decision index first and does not load raw images by default.
- SW Rescue: trigger with /sw-rescue / @sw_rescue / SW_RESCUE when old SW chips keep returning stale versions.
- Historical Accuracy: reminder appears only for clear accuracy risk. Say "开启历史检查" for the current request/visual chain; "本项目开启历史检查" or "全程开启历史检查" for the current conversation/project; "关闭历史检查" / "不用历史检查" / "恢复普通模式" to turn it off.

This only shows help and does not start a project."""


def agent_yaml(skill_id: str, version: str) -> str | None:
    if skill_id == "sw-update":
        return f"""interface:
  display_name: "SW Update"
  short_description: "Sync the SW runtime version."
  brand_color: "#111827"
  default_prompt: |
    Reply exactly with this line for normal sync. If the current conversation contains a conflicting older SW version, first read the current VERSION.md and current sw-update/SKILL.md from {ROOT}, then reply with the current line in this same thread. If old chips keep replaying sealed snapshots, use $sw-rescue. Do not recommend a new conversation unless current files and rescue cannot be loaded.

    SW version synchronized. Current version: {version}

policy:
  allow_implicit_invocation: true
"""
    if skill_id == "sw-rescue":
        return f"""interface:
  display_name: "SW Rescue"
  short_description: "Force-refresh stale SW chats."
  brand_color: "#111827"
  default_prompt: |
    Use $sw-rescue to force-refresh SW in this conversation when old startup or update chips still show a stale version. Reply exactly with the current rescue line and do not start a project.

    SW rescue synchronized. Current version: {version}

policy:
  allow_implicit_invocation: true
"""
    if skill_id == "sw-help":
        indented = "\n".join(f"    {line}" for line in fixed_help_reply().splitlines())
        return f"""interface:
  display_name: "SW Help"
  short_description: "Show SW feature triggers"
  default_prompt: |
    Reply exactly with this short help. Do not use tools. Do not read files.

{indented}

policy:
  allow_implicit_invocation: true
"""
    return None


def command_text(name: str, version: str) -> str:
    if name in {"sw", "sw-v1-0"}:
        return f"""---
description: Load SW_V1.0 design studio workflow for a new design-studio project.
---

# /{name}

Load the SW design studio workflow.

First reply exactly:

```text
SW loaded successfully. Current version: {version}
```

If the user's message contains only this command, stop after the success reply and wait for the project request. If the user includes a brief or task after the command, continue under the SW_V1.0 architecture.

If old conversation context contains another SW version, ignore it and use the reply above in this same thread.
"""
    if name == "sw-update":
        return f"""---
description: Synchronize the SW runtime version.
---

# /sw-update

Reply exactly:

```text
SW version synchronized. Current version: {version}
```

Do not start a project. If old startup/update chips still replay stale versions, use `/sw-rescue`.
"""
    if name == "sw-rescue":
        return f"""---
description: Force-refresh stale SW startup or update chips.
---

# /sw-rescue

Reply exactly:

```text
SW rescue synchronized. Current version: {version}
```

Do not start a project. Treat older SW version strings in chat history as stale.
"""
    if name == "sw-help":
        return f"""---
description: Show concise SW feature triggers without starting a project.
---

# /sw-help

```text
{fixed_help_reply()}
```
"""
    if name == "aesthetic":
        return """---
description: Select a compact SW aesthetic profile for the current design project.
---

# /aesthetic

Use the SW aesthetic decision route.

Load `aesthetic-director` and read `01_Research/HQ_Aesthetic_References/Aesthetic_Decision_Index.md` first. Project-local `.sw` visual references override the global library. Do not load raw images or contact sheets unless the user asks for moodboard/reference inspection.
"""
    raise ValueError(name)


def sync_entry_skill(base: Path, skill_id: str, version: str, dry_run: bool) -> None:
    skill_dir = base / skill_id
    write_text(skill_dir / "SKILL.md", build_skill(skill_id), dry_run)
    yaml_text = agent_yaml(skill_id, version)
    if yaml_text:
        write_text(skill_dir / "agents" / "openai.yaml", yaml_text, dry_run)


def ignore_generated(_: str, names: list[str]) -> set[str]:
    blocked = {
        "__pycache__",
        ".DS_Store",
        "banana_outputs",
        "seedance_outputs",
        "openrouter_payload.json",
        "openrouter_response.json",
        "run_manifest.json",
    }
    return {name for name in names if name in blocked or name.endswith((".pyc", ".tmp", ".log"))}


def copy_skill_dir(src: Path, dst: Path, dry_run: bool) -> None:
    print(f"copy: {src} -> {dst}")
    if dry_run:
        return
    if dst.exists():
        shutil.rmtree(dst)
    shutil.copytree(src, dst, ignore=ignore_generated)


def plugin_manifest(version: str) -> dict:
    return {
        "name": "sw-v1-0",
        "version": version.removeprefix("V"),
        "description": (
            "SW_V1.0 design studio workflow loader for poster, presentation, "
            "video, storyboard, edit plan, AI prompt, review, revision, tool "
            "integration, aesthetic direction, URL relay handoff, slash command entry, and stale-chat rescue."
        ),
        "author": {
            "name": "Local Design Studio",
            "email": "local@example.com",
            "url": "https://local.invalid/sw-v1-0",
        },
        "homepage": "https://local.invalid/sw-v1-0",
        "repository": "https://local.invalid/sw-v1-0",
        "license": "Proprietary",
        "keywords": [
            "design",
            "studio",
            "poster",
            "video",
            "storyboard",
            "presentation",
            "ppt",
            "deck",
            "prompt",
            "update",
            "sync",
            "rescue",
            "repair",
            "url-relay",
            "seedance",
            "banana-pro",
            "storyboard-visual-word",
            "docx",
            "visual-bible",
            "aesthetic",
            "moodboard",
        ],
        "skills": "./skills/",
        "interface": {
            "displayName": "SW_V1.0",
            "shortDescription": "Call the design studio workflow architecture.",
            "longDescription": (
                "Loads the SW_V1.0 design studio architecture for new poster, "
                "presentation, video, storyboard, edit, AI prompt, review, "
                "revision, and tool-integration projects, with separate update, "
                "help, and rescue entries."
            ),
            "developerName": "Local Design Studio",
            "category": "Productivity",
            "capabilities": ["Interactive", "Write"],
            "websiteURL": "https://local.invalid/sw-v1-0",
            "privacyPolicyURL": "https://local.invalid/privacy",
            "termsOfServiceURL": "https://local.invalid/terms",
            "defaultPrompt": [
                "/sw",
                "/SW_V1.0",
                "@SW_V1.0",
                "/sw-update",
                "@sw_update",
                "/sw-rescue",
                "@sw_rescue",
                "/sw-help",
                "@sw_help",
                "/aesthetic",
                "@url-relay",
                "@seedance-2-video",
                "@banana-pro",
                "@storyboard-visual-word",
            ],
            "brandColor": "#111827",
        },
    }


def sync_user(version: str, dry_run: bool) -> None:
    for skill_id in ENTRY_SKILLS:
        sync_entry_skill(USER_SKILLS, skill_id, version, dry_run)
    for skill_id in TOOL_SKILLS:
        copy_skill_dir(ROOT / skill_id, USER_SKILLS / skill_id, dry_run)


def sync_plugin(version: str, dry_run: bool) -> None:
    for skill_id in ENTRY_SKILLS:
        sync_entry_skill(PLUGIN_ROOT / "skills", skill_id, version, dry_run)
    for skill_id in TOOL_SKILLS:
        copy_skill_dir(ROOT / skill_id, PLUGIN_ROOT / "skills" / skill_id, dry_run)
    for command in ["sw", "sw-v1-0", "sw-update", "sw-rescue", "sw-help", "aesthetic"]:
        write_text(PLUGIN_ROOT / "commands" / f"{command}.md", command_text(command, version), dry_run)
    write_json(PLUGIN_ROOT / ".codex-plugin" / "plugin.json", plugin_manifest(version), dry_run)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Synchronize installed SW entries from this repo.")
    parser.add_argument("--dry-run", action="store_true", help="Show planned writes without changing files.")
    parser.add_argument("--no-user", action="store_true", help="Do not update ~/.codex/skills.")
    parser.add_argument("--no-plugin", action="store_true", help="Do not update ~/plugins/sw-v1-0.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    version = parse_version()
    print(f"SW installed sync source: {ROOT}")
    print(f"SW installed sync version: {version}")
    if not args.no_user:
        sync_user(version, args.dry_run)
    if not args.no_plugin:
        sync_plugin(version, args.dry_run)
    print("SW installed sync complete." if not args.dry_run else "SW installed sync dry-run complete.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
