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
            "Explicitly load the SW_V1.0 design studio workflow. Use only for "
            "/sw, /SW_V1.0, @SW_V1.0, call SW_V1.0, activate SW_V1.0, "
            "pull project architecture, or follow this project architecture. Do not use for ordinary "
            "creative-task wording unless an explicit SW invocation is present."
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
            "Show concise SW feature triggers for Banana Pro, Dreamina CLI, "
            "Seedance, URL Relay, Obsidian Aesthetic Vault, SW Rescue, and "
            "Historical Accuracy without starting a project."
        ),
    },
}

TOOL_SKILLS = [
    "banana-pro",
    "dreamina-cli",
    "kling-cli",
    "seedance-2-video",
    "url-relay",
    "black-background-cutout",
    "storyboard-visual-word",
    "feishu-docs",
]

RUNTIME_PACK_FILES = [
    "VERSION.md",
    "SW_Runtime_Index.md",
    "Cost_Governor.md",
    "Studio_Role_Label_Protocol.md",
    "Studio_Skill_Dispatch_Protocol.md",
]

PORTABLE_RUNTIME_DIRS = [
    "Studio_Skills",
    "Prompts",
]


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
- Project Asset Graph: automatic after SW activation for video/film/storyboard starts when recurring assets are not locked. Ask existing assets / assets to create / continuity locks before storyboard.
- Banana Pro: trigger with banana / Banana Pro / Nano Banana / @banana-pro / ? banana ??.
- Dreamina CLI: trigger with Dreamina CLI / Jimeng CLI / official Jimeng CLI / dreamina / @dreamina-cli / official Jimeng image generation / official Jimeng video generation. Uses the local dreamina command after prompt prep; inspect CLI help before real use.
- Kling CLI: trigger with Kling CLI / 可灵 MCP / kling-cli / @kling-cli / 可灵文生图 / 可灵图生视频 / 可灵生成视频. Uses the official kling command and OAuth credentials; inspect who_am_i/tool_list before real use.
- Seedance 2.0 Video: trigger with Seedance 2.0 / Ark Seedance / @seedance-2-video / use Seedance to generate video. This remains the Ark Seedance API route.
- URL Relay: trigger with URL relay / public URL / upload reference image / upload reference video / @url-relay. Used before downstream tools when local files need public URLs.
- Black Background Cutout: trigger with cutout / remove background / remove black background / transparent PNG / @black-background-cutout. Fast local transparent PNG preview for black/simple solid backgrounds; not finishing-grade.
- Storyboard Visual Word: trigger with visual plan document / visual director document / Word visual plan / DOCX visual plan / @storyboard-visual-word after selected storyboard or scene images are ready.
- Feishu Docs: trigger with publish to Feishu / sync to Feishu / Feishu visual plan / Feishu storyboard / Lark Docs / @feishu-docs after the visual plan or storyboard handoff is ready.
- Aesthetic Decision: trigger with /aesthetic, "SW decide the look", auto aesthetic choice, aesthetic profile, or moodboard direction. Reads the compact decision index first and does not load raw images by default.
- Obsidian Aesthetic Vault: trigger with Obsidian aesthetic vault / organize aesthetic vault / filter aesthetic images / open aesthetic library. Syncs a Markdown-only vault for browsing; normal SW work still uses the compact index.
- SW Rescue: trigger with /sw-rescue / @sw_rescue / SW_RESCUE when old SW chips keep returning stale versions.
- Historical Accuracy: reminder appears only for clear accuracy risk. Say "enable historical check" for the current request/visual chain; "enable historical check for this project" for the current conversation/project; "turn off historical check" to disable it.

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
    if skill_id == "sw-v1-0":
        sync_runtime_pack(skill_dir, dry_run)
    yaml_text = agent_yaml(skill_id, version)
    if yaml_text:
        write_text(skill_dir / "agents" / "openai.yaml", yaml_text, dry_run)


def ignore_generated(_: str, names: list[str]) -> set[str]:
    blocked = {
        "__pycache__",
        ".DS_Store",
        "banana_outputs",
        "seedance_outputs",
        "cutout_transparent_png",
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


def sync_runtime_pack(skill_dir: Path, dry_run: bool) -> None:
    """Copy the compact runtime pack next to the installed loader skill.

    This prevents simple image/poster edits from wasting time searching the
    original repository path after the skill is installed on another machine or
    invoked from a project folder that does not contain the full SW tree.
    """

    for rel in RUNTIME_PACK_FILES:
        src = ROOT / rel
        if src.exists():
            write_text(skill_dir / rel, read_text(src), dry_run)
    for rel in PORTABLE_RUNTIME_DIRS:
        src = ROOT / rel
        if src.exists():
            copy_skill_dir(src, skill_dir / rel, dry_run)


def plugin_manifest(version: str) -> dict:
    return {
        "name": "sw-v1-0",
        "version": version.removeprefix("V"),
        "description": (
            "SW_V1.0 explicit design studio workflow loader for /sw, "
            "/SW_V1.0, @SW_V1.0, update/help/rescue entries, optional tool "
            "skills, and stale-chat rescue. Ordinary design words do not "
            "auto-activate the full SW framework."
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
            "sw",
            "sw-v1-0",
            "explicit-invocation",
            "update",
            "sync",
            "rescue",
            "repair",
            "url-relay",
            "black-background-cutout",
            "cutout",
            "transparent-png",
            "dreamina",
            "dreamina-cli",
            "jimeng",
            "kling",
            "kling-cli",
            "kling-mcp",
            "klingai",
            "seedance",
            "banana-pro",
            "storyboard-visual-word",
            "feishu-docs",
            "feishu",
            "lark",
            "docx",
            "visual-bible",
            "aesthetic",
            "moodboard",
            "obsidian",
            "aesthetic-vault",
        ],
        "skills": "./skills/",
        "interface": {
            "displayName": "SW_V1.0",
            "shortDescription": "Call the design studio workflow architecture.",
            "longDescription": (
                "Explicitly loads the SW_V1.0 design studio architecture after "
                "/sw, /SW_V1.0, @SW_V1.0, or a written SW invocation. Ordinary "
                "creative-task wording does not auto-activate the full framework. Separate update, "
                "help, rescue, Feishu handoff, and Obsidian aesthetic vault "
                "support remain available."
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
                "@black-background-cutout",
                "@dreamina-cli",
                "@kling-cli",
                "@seedance-2-video",
                "@banana-pro",
                "@storyboard-visual-word",
                "@feishu-docs",
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
