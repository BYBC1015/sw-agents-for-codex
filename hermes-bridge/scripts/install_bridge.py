#!/usr/bin/env python3
"""Install only the non-secret SW bridge in an existing Hermes home."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import sys

SKILL_NAME = "hermes-bridge"
MANAGED = ".sw-bridge-managed.json"


def default_hermes_home() -> Path:
    configured = os.environ.get("HERMES_HOME", "").strip()
    if configured:
        return Path(configured).expanduser().resolve()
    if sys.platform == "win32":
        base = os.environ.get("LOCALAPPDATA", "").strip()
        root = Path(base) if base else Path.home() / "AppData" / "Local"
        return (root / "hermes").resolve()
    return (Path.home() / ".hermes").resolve()


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def json_bytes(value: dict) -> bytes:
    return (json.dumps(value, ensure_ascii=False, indent=2) + "\n").encode("utf-8")


def expected_files(project: Path) -> dict[str, bytes]:
    source = project / SKILL_NAME
    runner = project / "kling-api" / "scripts" / "kling_task.py"
    for required in (project / "VERSION.md", project / "AGENTS.md", runner):
        if not required.is_file():
            raise ValueError(f"Missing SW project file: {required}")
    return {
        "SKILL.md": (source / "SKILL.md").read_bytes(),
        "references/collaboration.md": (source / "references" / "collaboration.md").read_bytes(),
        "references/runtime.json": json_bytes({
            "sw_project_root": str(project),
            "source_skill": str(source / "SKILL.md"),
            "kling_runner": str(runner),
            "version_source": str(project / "VERSION.md"),
        }),
    }


def install(project: Path, hermes_home: Path, *, execute: bool = False) -> dict:
    project = project.expanduser().resolve()
    hermes_home = hermes_home.expanduser().resolve()
    if not hermes_home.is_dir() or not (hermes_home / "skills").is_dir():
        raise ValueError("Hermes home/skills does not exist; select the installed home with --hermes-home.")
    marker = hermes_home / "active_profile"
    if marker.is_file():
        active = marker.read_text(encoding="utf-8").strip()
        if active and active != "default" and not os.environ.get("HERMES_HOME"):
            raise ValueError("A named Hermes profile is active; select that profile's home explicitly through HERMES_HOME.")
    target = hermes_home / "skills" / SKILL_NAME
    if target.resolve() != target or (target / "references").resolve() != target / "references":
        raise ValueError("Bridge target contains a symlink/junction; refusing to write through it.")
    files = expected_files(project)
    manifest_path = target / MANAGED
    if manifest_path.is_symlink():
        raise ValueError("Bridge management file is a symlink; refusing to write through it.")
    previous = {}
    if target.exists():
        if not manifest_path.is_file():
            raise ValueError("Existing bridge is unmanaged; no files were overwritten.")
        previous = json.loads(manifest_path.read_text(encoding="utf-8"))
        if previous.get("owner") != "sw-hermes-bridge":
            raise ValueError("Existing bridge has an unknown owner; no files were overwritten.")
    old_hashes = previous.get("sha256", {})
    for relative in files:
        path = target / relative
        if path.is_symlink():
            raise ValueError(f"Refusing to replace symlink: {path}")
        if path.exists() and digest(path.read_bytes()) != old_hashes.get(relative):
            raise ValueError(f"Bridge file was locally modified; preserve or reconcile it first: {path}")
    changed = [rel for rel, data in files.items()
               if not (target / rel).exists() or (target / rel).read_bytes() != data]
    if execute:
        for relative in changed:
            path = target / relative
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(files[relative])
        manifest = {"owner": "sw-hermes-bridge", "sha256": {name: digest(data) for name, data in files.items()}}
        manifest_path.write_bytes(json_bytes(manifest))
    return {
        "mode": "installed" if execute else "preview",
        "hermes_home": str(hermes_home),
        "skill_path": str(target / "SKILL.md"),
        "sw_project_root": str(project),
        "changed_files": changed,
        "credential_files_read_or_copied": False,
        "model_requests_sent": False,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project-root", type=Path, default=Path(__file__).resolve().parents[2])
    parser.add_argument("--hermes-home", type=Path, default=None)
    parser.add_argument("--execute", action="store_true", help="Write the bridge; default only previews.")
    args = parser.parse_args()
    try:
        report = install(args.project_root, args.hermes_home or default_hermes_home(), execute=args.execute)
    except (OSError, ValueError) as exc:
        print(json.dumps({"error": str(exc)}, ensure_ascii=False), file=sys.stderr)
        return 1
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
