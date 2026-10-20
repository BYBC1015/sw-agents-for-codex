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
import subprocess
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

HOT_ENTRY_FILES = [
    "VERSION.md",
    "SW_V1.0.md",
    "sw_update.md",
    "sw_rescue.md",
    "sw_help.md",
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
    USERPROFILE / ".codex" / "skills" / "dreamina-cli" / "SKILL.md",
    USERPROFILE / ".codex" / "skills" / "kling-cli" / "SKILL.md",
    USERPROFILE / ".codex" / "skills" / "seedance-2-video" / "SKILL.md",
    USERPROFILE / ".codex" / "skills" / "url-relay" / "SKILL.md",
    USERPROFILE / ".codex" / "skills" / "black-background-cutout" / "SKILL.md",
    USERPROFILE / ".codex" / "skills" / "storyboard-visual-word" / "SKILL.md",
    USERPROFILE / ".codex" / "skills" / "feishu-docs" / "SKILL.md",
]

PLUGIN_FILES = [
    USERPROFILE / "plugins" / "sw-v1-0" / "skills" / "sw-v1-0" / "SKILL.md",
    USERPROFILE / "plugins" / "sw-v1-0" / "skills" / "sw-update" / "SKILL.md",
    USERPROFILE / "plugins" / "sw-v1-0" / "skills" / "sw-rescue" / "SKILL.md",
    USERPROFILE / "plugins" / "sw-v1-0" / "skills" / "sw-help" / "SKILL.md",
    USERPROFILE / "plugins" / "sw-v1-0" / "skills" / "banana-pro" / "SKILL.md",
    USERPROFILE / "plugins" / "sw-v1-0" / "skills" / "dreamina-cli" / "SKILL.md",
    USERPROFILE / "plugins" / "sw-v1-0" / "skills" / "kling-cli" / "SKILL.md",
    USERPROFILE / "plugins" / "sw-v1-0" / "skills" / "seedance-2-video" / "SKILL.md",
    USERPROFILE / "plugins" / "sw-v1-0" / "skills" / "url-relay" / "SKILL.md",
    USERPROFILE / "plugins" / "sw-v1-0" / "skills" / "black-background-cutout" / "SKILL.md",
    USERPROFILE / "plugins" / "sw-v1-0" / "skills" / "storyboard-visual-word" / "SKILL.md",
    USERPROFILE / "plugins" / "sw-v1-0" / "skills" / "feishu-docs" / "SKILL.md",
    USERPROFILE / "plugins" / "sw-v1-0" / "skills" / "sw-update" / "agents" / "openai.yaml",
    USERPROFILE / "plugins" / "sw-v1-0" / "skills" / "sw-rescue" / "agents" / "openai.yaml",
    USERPROFILE / "plugins" / "sw-v1-0" / "skills" / "sw-help" / "agents" / "openai.yaml",
    USERPROFILE / "plugins" / "sw-v1-0" / "commands" / "sw.md",
    USERPROFILE / "plugins" / "sw-v1-0" / "commands" / "sw-v1-0.md",
    USERPROFILE / "plugins" / "sw-v1-0" / "commands" / "sw-update.md",
    USERPROFILE / "plugins" / "sw-v1-0" / "commands" / "sw-rescue.md",
    USERPROFILE / "plugins" / "sw-v1-0" / "commands" / "sw-help.md",
    USERPROFILE / "plugins" / "sw-v1-0" / "commands" / "aesthetic.md",
]

INSTALLED_RUNTIME_PACK_FILES = [
    USERPROFILE / ".codex" / "skills" / "sw-v1-0" / "SW_Runtime_Index.md",
    USERPROFILE / ".codex" / "skills" / "sw-v1-0" / "Cost_Governor.md",
    USERPROFILE / ".codex" / "skills" / "sw-v1-0" / "Studio_Skills" / "poster-art-director" / "SKILL.md",
    USERPROFILE / ".codex" / "skills" / "sw-v1-0" / "Studio_Skills" / "layout-designer" / "SKILL.md",
    USERPROFILE / ".codex" / "skills" / "sw-v1-0" / "Studio_Skills" / "prompt-director" / "SKILL.md",
    USERPROFILE / "plugins" / "sw-v1-0" / "skills" / "sw-v1-0" / "SW_Runtime_Index.md",
    USERPROFILE / "plugins" / "sw-v1-0" / "skills" / "sw-v1-0" / "Cost_Governor.md",
    USERPROFILE / "plugins" / "sw-v1-0" / "skills" / "sw-v1-0" / "Studio_Skills" / "poster-art-director" / "SKILL.md",
    USERPROFILE / "plugins" / "sw-v1-0" / "skills" / "sw-v1-0" / "Studio_Skills" / "layout-designer" / "SKILL.md",
    USERPROFILE / "plugins" / "sw-v1-0" / "skills" / "sw-v1-0" / "Studio_Skills" / "prompt-director" / "SKILL.md",
]

PROMPT_REFERENCE_FILES = [
    ROOT / "Prompts" / "Image_Aesthetic_Prompt_Reference.md",
    ROOT / "Prompts" / "Video_Motion_Edit_Prompt_Rules.md",
    ROOT / "Prompts" / "Visual_Development_Board_Rules.md",
    ROOT / "Prompts" / "Tool_Official_Prompt_Deltas.md",
    ROOT / "01_Research" / "HQ_Aesthetic_References" / "Aesthetic_Decision_Index.md",
    ROOT / "01_Research" / "HQ_Aesthetic_References" / "Aesthetic_Library_Config.md",
    ROOT / "01_Research" / "HQ_Aesthetic_References" / "HQ_Aesthetic_Master_Index.md",
    ROOT / "01_Research" / "HQ_Aesthetic_References" / "Top_Tier_Collection_Queue.md",
    ROOT / "01_Research" / "Oscar_Best_Picture_Visual_Reference.md",
    ROOT / "01_Research" / "Aesthetic_Daily_Selected" / "README.md",
    ROOT / "01_Research" / "Aesthetic_Daily_Selected" / "Daily_Selected_Index.md",
]

STUDIO_SKILL_FILES = [
    ROOT / "Studio_Skills" / "aesthetic-director" / "SKILL.md",
]

PROJECT_MEMORY_TEMPLATE_FILES = [
    ROOT / "Project_Memory_Templates" / ".sw" / "PROJECT.md",
    ROOT / "Project_Memory_Templates" / ".sw" / "RULES.md",
    ROOT / "Project_Memory_Templates" / ".sw" / "MEMORY.md",
    ROOT / "Project_Memory_Templates" / ".sw" / "ASSETS.md",
    ROOT / "Project_Memory_Templates" / ".sw" / "CHANGELOG.md",
]

REPO_TOOL_SKILL_FILES = [
    ROOT / "Storyboard_Continuity_Protocol.md",
    ROOT / "apps" / "media-canvas" / "storyboard.py",
    ROOT / "apps" / "media-canvas" / "web" / "storyboard.js",
    ROOT / "apps" / "media-canvas" / "integrations" / "media-canvas" / "SKILL.md",
    ROOT / "apps" / "media-canvas" / "integrations" / "sw-canvas" / "SKILL.md",
    ROOT / "INSTALL_SW.md",
    ROOT / "tools" / "sw_bootstrap.py",
    ROOT / "banana-pro" / "SKILL.md",
    ROOT / "banana-pro" / "scripts" / "generate_openrouter_image.py",
    ROOT / "banana-pro" / "bin" / "banana-pro",
    ROOT / "dreamina-cli" / "SKILL.md",
    ROOT / "dreamina-cli" / "agents" / "openai.yaml",
    ROOT / "kling-cli" / "SKILL.md",
    ROOT / "kling-cli" / "reference.md",
    ROOT / "seedance-2-video" / "SKILL.md",
    ROOT / "seedance-2-video" / "scripts" / "seedance_task.py",
    ROOT / "url-relay" / "SKILL.md",
    ROOT / "url-relay" / "scripts" / "url_relay.py",
    ROOT / "black-background-cutout" / "SKILL.md",
    ROOT / "black-background-cutout" / "agents" / "openai.yaml",
    ROOT / "black-background-cutout" / "scripts" / "black_background_cutout.py",
    ROOT / "storyboard-visual-word" / "SKILL.md",
    ROOT / "storyboard-visual-word" / "scripts" / "build_scene_visual_docx.py",
    ROOT / "feishu-docs" / "SKILL.md",
    ROOT / "feishu-docs" / "agents" / "openai.yaml",
    ROOT / "feishu-docs" / "scripts" / "feishu_doc_cli.py",
    ROOT / "tools" / "sync_obsidian_aesthetic_vault.py",
    ROOT / "Obsidian_Aesthetic_Vault" / "Home.md",
    ROOT / "Obsidian_Aesthetic_Vault" / "00_Index" / "Profile Router.md",
    ROOT / "Obsidian_Aesthetic_Vault" / "obsidian-vault-config.json",
]

TOOL_REGISTRY_LITE_FILE = ROOT / "tools" / "sw_tool_registry_lite.json"
TOOL_REGISTRY_LITE_REQUIRED_IDS = {
    "black-background-cutout",
    "banana-pro",
    "dreamina-cli",
    "kling-cli",
    "seedance-2-video",
    "url-relay",
    "kling-api",
    "hermes-bridge",
    "storyboard-visual-word",
    "feishu-docs",
}
TOOL_REGISTRY_LITE_REQUIRED_FIELDS = {
    "id",
    "name",
    "capability",
    "skill_path",
    "loads_as",
    "trigger_mode",
    "configured_by",
    "cost_lane",
    "confirmation_required",
    "fallback",
}
TOOL_REGISTRY_LITE_COST_LANES = {"low", "medium", "high"}

SECRET_PATTERNS = [
    re.compile(r"api-key-kling-[A-Za-z0-9_-]{24,}"),
    re.compile(r"sk-or-v1-[A-Za-z0-9]{24,}"),
    re.compile(r"ark-[0-9a-fA-F]{8}-[0-9a-fA-F-]{20,}"),
    re.compile(r"swrel_[A-Za-z0-9_-]{32,}"),
]

TEXT_SUFFIXES = {".md", ".yaml", ".yml", ".json", ".py", ".toml", ".txt"}
MEDIA_SUFFIXES = {".jpg", ".jpeg", ".png", ".webp", ".gif", ".mp4", ".mov", ".avi"}
IGNORED_SCAN_DIRS = {
    ".tmp", "tmp", "output", "outputs", "node_modules", ".venv", "venv", ".runtime", ".codex-hub-state",
    ".codex",
    ".git",
    "__pycache__",
    "banana_outputs",
    "seedance_outputs",
    "cutout_transparent_png",
}
AESTHETIC_MEDIA_ROOTS = [
    ROOT / "01_Research" / "HQ_Aesthetic_References",
    ROOT / "01_Research" / "Aesthetic_Daily_Selected",
    ROOT / "01_Research" / "Aesthetic_Reference_Archive",
    ROOT / "01_Research" / "Oscar_Frame_References",
]

MOJIBAKE_SEQUENCE_ESCAPES = [
    r"\u9357\u866b",
    r"\u93c2\u89c4",
    r"\u7459\u55da",
    r"\u6d93\ue161",
    r"\u6d93\u5a41",
    r"\u68e3\u6b12",
    r"\u7ef1\u72b3",
    r"\u93c8\ue104",
    r"\u934f\u3127",
    r"\u934f\u62bd",
    r"\u93ad\u3220",
    r"\u9422\u71b8",
    r"\u9359\u509d",
    r"\u93cd\u714e",
    r"\u9225",
    r"\u9239",
    r"\ufffd",
]
MOJIBAKE_SEQUENCES = [
    item.encode("ascii").decode("unicode_escape") for item in MOJIBAKE_SEQUENCE_ESCAPES
]
PRIVATE_USE_RE = re.compile(r"[\ue000-\uf8ff]")


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8-sig")


def fail(issues: list[str], message: str) -> None:
    issues.append(message)


def emit(line: str) -> None:
    try:
        print(line)
    except UnicodeEncodeError:
        encoding = sys.stdout.encoding or "utf-8"
        safe = line.encode(encoding, errors="backslashreplace").decode(encoding)
        print(safe)


def is_ignored_scan_path(path: Path) -> bool:
    return any(part in IGNORED_SCAN_DIRS for part in path.parts)


def check_required_repo_files(issues: list[str], rel_paths: list[str]) -> None:
    for rel in rel_paths:
        if not (ROOT / rel).exists():
            fail(issues, f"missing required repo file: {rel}")


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

    for path in INSTALLED_RUNTIME_PACK_FILES:
        if not path.exists():
            fail(issues, f"missing installed runtime pack file: {path}")


def check_prompt_references(issues: list[str]) -> None:
    for path in PROMPT_REFERENCE_FILES:
        if not path.exists():
            fail(issues, f"missing prompt/reference file: {path.relative_to(ROOT)}")
    for path in STUDIO_SKILL_FILES:
        if not path.exists():
            fail(issues, f"missing studio skill file: {path.relative_to(ROOT)}")

    spec = ROOT / "Prompts" / "Prompt_Spec_Rules.md"
    if spec.exists():
        text = read_text(spec)
        for required in [
            "Aesthetic_Decision_Index.md",
            "Image_Aesthetic_Prompt_Reference.md",
            "Video_Motion_Edit_Prompt_Rules.md",
            "Visual_Development_Board_Rules.md",
            "Tool_Official_Prompt_Deltas.md",
            "Daily_Selected_Index.md",
        ]:
            if required not in text:
                fail(issues, f"Prompt_Spec_Rules.md does not reference {required}")

    role_registry = ROOT / "Studio_Role_Label_Protocol.md"
    if role_registry.exists() and "aesthetic-director" not in read_text(role_registry):
        fail(issues, "Studio_Role_Label_Protocol.md does not mention aesthetic-director")

    poster_text_rules = {
        ROOT / "Prompts" / "Prompt_Spec_Rules.md": ["视觉文字", "系统字体", "Poster Image-Native Typography"],
        ROOT / "Stage_Runbook.md": ["海报快速改稿", "Poster Default: Image-Native Typography"],
        ROOT / "SW_Runtime_Index.md": ["Poster quick edit", "image-native"],
        ROOT / "Studio_Skills" / "poster-art-director" / "SKILL.md": ["image-native typography", "plain system fonts"],
        ROOT / "Studio_Skills" / "layout-designer" / "SKILL.md": ["system/editable text overlays", "poster hero titles"],
    }
    for path, required_terms in poster_text_rules.items():
        if not path.exists():
            fail(issues, f"missing poster text-rule file: {path.relative_to(ROOT)}")
            continue
        text = read_text(path)
        for term in required_terms:
            if term not in text:
                fail(issues, f"{path.relative_to(ROOT)} does not mention poster text rule: {term}")


def check_project_memory_templates(issues: list[str]) -> None:
    for path in PROJECT_MEMORY_TEMPLATE_FILES:
        if not path.exists():
            fail(issues, f"missing project memory template: {path.relative_to(ROOT)}")

    assets = ROOT / "Project_Memory_Templates" / ".sw" / "ASSETS.md"
    if assets.exists():
        text = read_text(assets)
        for required in ["Visual References", "Extract", "Do not copy"]:
            if required not in text:
                fail(issues, f"ASSETS.md template does not mention {required}")


def check_repo_tool_skills(issues: list[str]) -> None:
    for path in REPO_TOOL_SKILL_FILES:
        if not path.exists():
            fail(issues, f"missing repo tool skill file: {path.relative_to(ROOT)}")

    registry = ROOT / "Tool_Registry.md"
    if registry.exists():
        text = read_text(registry)
        for required in [
            "Banana Pro",
            "Dreamina CLI",
            "Kling CLI",
            "Seedance",
            "URL Relay",
            "Black Background Cutout",
            "Storyboard Visual Word",
            "Feishu Docs",
            "Obsidian Aesthetic Vault",
        ]:
            if required not in text:
                fail(issues, f"Tool_Registry.md does not mention {required}")


def check_tool_registry_lite(issues: list[str]) -> None:
    if not TOOL_REGISTRY_LITE_FILE.exists():
        fail(issues, f"missing lite tool registry: {TOOL_REGISTRY_LITE_FILE.relative_to(ROOT)}")
        return

    try:
        data = json.loads(read_text(TOOL_REGISTRY_LITE_FILE))
    except Exception as exc:
        fail(issues, f"lite tool registry is not valid JSON: {exc}")
        return

    if data.get("purpose") != "internal_sw_tool_routing":
        fail(issues, "lite tool registry has an unexpected purpose")

    tools = data.get("tools")
    if not isinstance(tools, list):
        fail(issues, "lite tool registry tools must be a list")
        return

    seen: set[str] = set()
    for index, tool in enumerate(tools):
        if not isinstance(tool, dict):
            fail(issues, f"lite tool registry entry #{index} must be an object")
            continue

        tool_id = tool.get("id")
        if not isinstance(tool_id, str) or not tool_id:
            fail(issues, f"lite tool registry entry #{index} has no id")
            continue
        if tool_id in seen:
            fail(issues, f"duplicate lite tool registry id: {tool_id}")
        seen.add(tool_id)

        missing = sorted(TOOL_REGISTRY_LITE_REQUIRED_FIELDS - set(tool))
        if missing:
            fail(issues, f"lite tool registry {tool_id} missing fields: {', '.join(missing)}")

        skill_path = tool.get("skill_path")
        if not isinstance(skill_path, str) or not skill_path:
            fail(issues, f"lite tool registry {tool_id} has invalid skill_path")
        elif Path(skill_path).is_absolute():
            fail(issues, f"lite tool registry {tool_id} uses an absolute skill_path")
        elif not (ROOT / skill_path).exists():
            fail(issues, f"lite tool registry {tool_id} skill_path missing: {skill_path}")

        if tool.get("loads_as") != "tool_skill":
            fail(issues, f"lite tool registry {tool_id} must load as tool_skill")
        if tool.get("cost_lane") not in TOOL_REGISTRY_LITE_COST_LANES:
            fail(issues, f"lite tool registry {tool_id} has invalid cost_lane")

        for field in ["configured_by", "confirmation_required", "fallback"]:
            values = tool.get(field)
            if not isinstance(values, list) or not all(isinstance(item, str) for item in values):
                fail(issues, f"lite tool registry {tool_id} {field} must be a string list")

        serialized = json.dumps(tool, sort_keys=True)
        for pattern in SECRET_PATTERNS:
            if pattern.search(serialized):
                fail(issues, f"possible secret in lite tool registry entry: {tool_id}")

    missing_ids = sorted(TOOL_REGISTRY_LITE_REQUIRED_IDS - seen)
    extra_ids = sorted(seen - TOOL_REGISTRY_LITE_REQUIRED_IDS)
    if missing_ids:
        fail(issues, f"lite tool registry missing ids: {', '.join(missing_ids)}")
    if extra_ids:
        fail(issues, f"lite tool registry has unexpected ids: {', '.join(extra_ids)}")

    by_id = {tool.get("id"): tool for tool in tools if isinstance(tool, dict)}
    for tool_id in ["banana-pro", "dreamina-cli", "kling-cli", "seedance-2-video", "kling-api"]:
        confirmations = by_id.get(tool_id, {}).get("confirmation_required", [])
        if "real_generation" not in confirmations:
            fail(issues, f"lite tool registry {tool_id} must require real_generation confirmation")


def check_secret_leaks(issues: list[str]) -> None:
    for path in scan_files(ROOT):
        if not path.is_file():
            continue
        if is_ignored_scan_path(path):
            continue
        try:
            text = read_text(path)
        except UnicodeDecodeError:
            continue
        for pattern in SECRET_PATTERNS:
            if pattern.search(text):
                fail(issues, f"possible secret leaked in repo file: {path.relative_to(ROOT)}")


def scan_files(base: Path):
    if base.is_file():
        yield base
        return
    for directory, dirs, names in os.walk(base):
        dirs[:] = [name for name in dirs if name not in IGNORED_SCAN_DIRS]
        for name in names:
            yield Path(directory) / name


def iter_text_files(paths: list[Path]) -> list[Path]:
    files: list[Path] = []
    for base in paths:
        if not base.exists():
            continue
        candidates = scan_files(base)
        for path in candidates:
            if not path.is_file():
                continue
            if path.suffix.lower() not in TEXT_SUFFIXES:
                continue
            if is_ignored_scan_path(path):
                continue
            files.append(path)
    return files


def check_text_integrity(issues: list[str], scope: str) -> None:
    roots: list[Path] = []
    if scope in {"repo", "all"}:
        roots.append(ROOT)
    if scope in {"installed", "all"}:
        roots.extend(
            [
                USERPROFILE / ".codex" / "skills" / "sw-v1-0",
                USERPROFILE / ".codex" / "skills" / "sw-update",
                USERPROFILE / ".codex" / "skills" / "sw-rescue",
                USERPROFILE / ".codex" / "skills" / "sw-help",
                USERPROFILE / "plugins" / "sw-v1-0",
            ]
        )
    for path in iter_text_files(roots):
        try:
            text = read_text(path)
        except UnicodeDecodeError:
            fail(issues, f"text file is not UTF-8 readable: {path}")
            continue
        for seq in MOJIBAKE_SEQUENCES:
            if seq in text:
                fail(issues, f"possible mojibake sequence {seq!r} in {path}")
                break
        if PRIVATE_USE_RE.search(text):
            fail(issues, f"possible corrupted/private-use character in {path}")


def check_aesthetic_media_not_tracked(issues: list[str]) -> None:
    if not (ROOT / ".git").exists():
        return
    completed = subprocess.run(
        ["git", "ls-files"],
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL,
    )
    if completed.returncode != 0:
        return
    tracked = [ROOT / line.strip() for line in completed.stdout.splitlines() if line.strip()]
    for path in tracked:
        if path.suffix.lower() not in MEDIA_SUFFIXES:
            continue
        for root in AESTHETIC_MEDIA_ROOTS:
            try:
                path.relative_to(root)
            except ValueError:
                continue
            fail(issues, f"aesthetic media file is tracked by git: {path.relative_to(ROOT)}")
            break


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Check SW release consistency.")
    parser.add_argument(
        "--scope",
        choices=["repo", "installed", "all"],
        default=None,
        help=(
            "repo checks only repository files for CI; installed checks local "
            "user/plugin copies; all does both."
        ),
    )
    parser.add_argument(
        "--profile",
        choices=["hot", "work", "release"],
        default=None,
        help=(
            "hot runs the minimal daily gate, work runs normal maintenance "
            "checks, and release keeps the full legacy publish gate."
        ),
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    profile = args.profile or "release"
    scope = args.scope or ("repo" if profile in {"hot", "work"} else "all")
    issues: list[str] = []
    version = parse_version(issues)

    if scope in {"repo", "all"}:
        check_required_repo_files(issues, HOT_ENTRY_FILES)
        check_fixed_replies(issues, version)
        check_tool_registry_lite(issues)

    if profile in {"work", "release"} and scope in {"repo", "all"}:
        check_prompt_references(issues)
        check_project_memory_templates(issues)
        check_repo_tool_skills(issues)
        check_aesthetic_media_not_tracked(issues)

    if profile == "release" and scope in {"repo", "all"}:
        check_secret_leaks(issues)

    if scope in {"installed", "all"}:
        check_external_copies(issues, version)

    if profile == "release":
        check_text_integrity(issues, scope)

    if issues:
        emit(f"SW consistency check failed for {version} (scope={scope}, profile={profile}):")
        for issue in issues:
            emit(f"- {issue}")
        return 1

    emit(f"SW consistency check passed for {version} (scope={scope}, profile={profile}).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
