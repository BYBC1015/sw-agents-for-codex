#!/usr/bin/env python3
"""Lightweight SW release consistency checks.

The checker is intentionally dependency-free so it can run before every SW
maintenance publish without loading large docs into the model context.
"""

from __future__ import annotations

import json
import os
import re
import sys
import argparse
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
USERPROFILE = Path(os.environ.get("USERPROFILE", str(Path.home())))


ROOT_ACTIVE_FILES = [
    "AGENTS.md",
    "Command_Aliases.md",
    "SW_Runtime_Index.md",
    "SW_V1.0.md",
    "sw_update.md",
    "sw_rescue.md",
    "README.md",
    "Start_New_Project.md",
    "Project_Minimal_Entry_Pack.md",
    "Legacy_Conversation_Recovery.md",
    "Feature_Trigger_Index.md",
]

USER_SKILL_FILES = [
    USERPROFILE / ".codex" / "skills" / "sw-v1-0" / "SKILL.md",
    USERPROFILE / ".codex" / "skills" / "sw-update" / "SKILL.md",
    USERPROFILE / ".codex" / "skills" / "sw-rescue" / "SKILL.md",
    USERPROFILE / ".codex" / "skills" / "sw-help" / "SKILL.md",
    USERPROFILE / ".codex" / "skills" / "sw-update" / "agents" / "openai.yaml",
    USERPROFILE / ".codex" / "skills" / "sw-rescue" / "agents" / "openai.yaml",
    USERPROFILE / ".codex" / "skills" / "sw-help" / "agents" / "openai.yaml",
    USERPROFILE / ".codex" / "skills" / "banana-pro" / "SKILL.md",
    USERPROFILE / ".codex" / "skills" / "seedance-2-video" / "SKILL.md",
    USERPROFILE / ".codex" / "skills" / "url-relay" / "SKILL.md",
]

PLUGIN_FILES = [
    USERPROFILE / "plugins" / "sw-v1-0" / "skills" / "sw-v1-0" / "SKILL.md",
    USERPROFILE / "plugins" / "sw-v1-0" / "skills" / "sw-update" / "SKILL.md",
    USERPROFILE / "plugins" / "sw-v1-0" / "skills" / "sw-rescue" / "SKILL.md",
    USERPROFILE / "plugins" / "sw-v1-0" / "skills" / "sw-help" / "SKILL.md",
    USERPROFILE / "plugins" / "sw-v1-0" / "skills" / "banana-pro" / "SKILL.md",
    USERPROFILE / "plugins" / "sw-v1-0" / "skills" / "seedance-2-video" / "SKILL.md",
    USERPROFILE / "plugins" / "sw-v1-0" / "skills" / "url-relay" / "SKILL.md",
    USERPROFILE / "plugins" / "sw-v1-0" / "skills" / "sw-update" / "agents" / "openai.yaml",
    USERPROFILE / "plugins" / "sw-v1-0" / "skills" / "sw-rescue" / "agents" / "openai.yaml",
    USERPROFILE / "plugins" / "sw-v1-0" / "skills" / "sw-help" / "agents" / "openai.yaml",
    USERPROFILE / "plugins" / "sw-v1-0" / "commands" / "sw.md",
    USERPROFILE / "plugins" / "sw-v1-0" / "commands" / "sw-v1-0.md",
    USERPROFILE / "plugins" / "sw-v1-0" / "commands" / "sw-update.md",
    USERPROFILE / "plugins" / "sw-v1-0" / "commands" / "sw-rescue.md",
    USERPROFILE / "plugins" / "sw-v1-0" / "commands" / "sw-help.md",
]

PROMPT_REFERENCE_FILES = [
    ROOT / "Prompts" / "Image_Aesthetic_Prompt_Reference.md",
    ROOT / "Prompts" / "Video_Motion_Edit_Prompt_Rules.md",
    ROOT / "Prompts" / "Visual_Development_Board_Rules.md",
    ROOT / "01_Research" / "Oscar_Best_Picture_Visual_Reference.md",
    ROOT / "01_Research" / "Aesthetic_Daily_Selected" / "README.md",
    ROOT / "01_Research" / "Aesthetic_Daily_Selected" / "Daily_Selected_Index.md",
]

REPO_TOOL_SKILL_FILES = [
    ROOT / "banana-pro" / "SKILL.md",
    ROOT / "banana-pro" / "scripts" / "generate_openrouter_image.py",
    ROOT / "seedance-2-video" / "SKILL.md",
    ROOT / "seedance-2-video" / "scripts" / "seedance_task.py",
    ROOT / "url-relay" / "SKILL.md",
    ROOT / "url-relay" / "scripts" / "url_relay.py",
]

SECRET_PATTERNS = [
    re.compile(r"sk-or-v1-[A-Za-z0-9]{24,}"),
    re.compile(r"ark-[0-9a-fA-F]{8}-[0-9a-fA-F-]{20,}"),
    re.compile(r"swrel_[A-Za-z0-9_-]{32,}"),
]


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8-sig")


def fail(issues: list[str], message: str) -> None:
    issues.append(message)


def parse_version(issues: list[str]) -> str:
    version_file = ROOT / "VERSION.md"
    text = read_text(version_file)
    match = re.search(r"Current runtime version:\s*(V\d+\.\d+\.\d+)", text)
    if not match:
        fail(issues, "VERSION.md has no Current runtime version line")
        return "V0.0.0"
    return match.group(1)


def check_fixed_replies(issues: list[str], version: str) -> None:
    expected = [
        f"SW loaded successfully. Current version: {version}",
        f"SW version synchronized. Current version: {version}",
        f"SW rescue synchronized. Current version: {version}",
    ]
    for rel in ROOT_ACTIVE_FILES:
        path = ROOT / rel
        if not path.exists():
            continue
        text = read_text(path)
        if "SW loaded successfully." in text and expected[0] not in text:
            fail(issues, f"{rel} has stale activation reply")
        if "SW version synchronized." in text and expected[1] not in text:
            fail(issues, f"{rel} has stale sync reply")
        if "SW rescue synchronized." in text and expected[2] not in text:
            fail(issues, f"{rel} has stale rescue reply")


def check_external_copies(issues: list[str], version: str) -> None:
    expected_lines = {
        "SW loaded successfully.": f"SW loaded successfully. Current version: {version}",
        "SW version synchronized.": f"SW version synchronized. Current version: {version}",
        "SW rescue synchronized.": f"SW rescue synchronized. Current version: {version}",
    }
    for path in USER_SKILL_FILES + PLUGIN_FILES:
        if not path.exists():
            fail(issues, f"missing installed entry: {path}")
            continue
        text = read_text(path)
        for marker, expected in expected_lines.items():
            if marker in text and expected not in text:
                fail(issues, f"stale installed entry: {path}")

    manifest = USERPROFILE / "plugins" / "sw-v1-0" / ".codex-plugin" / "plugin.json"
    if manifest.exists():
        try:
            data = json.loads(read_text(manifest))
        except Exception as exc:  # pragma: no cover - diagnostic path
            fail(issues, f"plugin.json is not valid JSON: {exc}")
            return
        expected_manifest_version = version.removeprefix("V")
        if str(data.get("version")) != expected_manifest_version:
            fail(
                issues,
                f"plugin.json version is {data.get('version')}, expected {expected_manifest_version}",
            )
    else:
        fail(issues, f"missing plugin manifest: {manifest}")


def check_prompt_references(issues: list[str]) -> None:
    for path in PROMPT_REFERENCE_FILES:
        if not path.exists():
            fail(issues, f"missing prompt/reference file: {path.relative_to(ROOT)}")

    spec = ROOT / "Prompts" / "Prompt_Spec_Rules.md"
    if spec.exists():
        text = read_text(spec)
        for required in [
            "Image_Aesthetic_Prompt_Reference.md",
            "Video_Motion_Edit_Prompt_Rules.md",
            "Visual_Development_Board_Rules.md",
            "Daily_Selected_Index.md",
        ]:
            if required not in text:
                fail(issues, f"Prompt_Spec_Rules.md does not reference {required}")


def check_repo_tool_skills(issues: list[str]) -> None:
    for path in REPO_TOOL_SKILL_FILES:
        if not path.exists():
            fail(issues, f"missing repo tool skill file: {path.relative_to(ROOT)}")

    registry = ROOT / "Tool_Registry.md"
    if registry.exists():
        text = read_text(registry)
        for required in ["Banana Pro", "Seedance", "URL Relay"]:
            if required not in text:
                fail(issues, f"Tool_Registry.md does not mention {required}")


def check_secret_leaks(issues: list[str]) -> None:
    ignored_dirs = {".git", "__pycache__", "banana_outputs", "seedance_outputs"}
    for path in ROOT.rglob("*"):
        if not path.is_file():
            continue
        if any(part in ignored_dirs for part in path.parts):
            continue
        try:
            text = read_text(path)
        except UnicodeDecodeError:
            continue
        for pattern in SECRET_PATTERNS:
            if pattern.search(text):
                fail(issues, f"possible secret leaked in repo file: {path.relative_to(ROOT)}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Check SW release consistency.")
    parser.add_argument(
        "--scope",
        choices=["repo", "installed", "all"],
        default="all",
        help=(
            "repo checks only repository files for CI; installed checks local "
            "user/plugin copies; all does both."
        ),
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    issues: list[str] = []
    version = parse_version(issues)

    if args.scope in {"repo", "all"}:
        check_fixed_replies(issues, version)
        check_prompt_references(issues)
        check_repo_tool_skills(issues)
        check_secret_leaks(issues)

    if args.scope in {"installed", "all"}:
        check_external_copies(issues, version)

    if issues:
        print(f"SW consistency check failed for scope={args.scope}:")
        for issue in issues:
            print(f"- {issue}")
        return 1

    print(f"SW consistency check passed for {version} (scope={args.scope}).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
