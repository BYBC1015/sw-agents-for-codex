#!/usr/bin/env python3
"""Small SW maintenance doctor.

Runs the cheap checks first and prints a compact next-step suggestion. Use this
before publishing, after syncing installed entries, or when a conversation shows
different SW versions across startup/update/rescue.
"""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8-sig")


def parse_version() -> str:
    text = read_text(ROOT / "VERSION.md")
    match = re.search(r"Current runtime version:\s*(V\d+\.\d+\.\d+)", text)
    if not match:
        return "unknown"
    return match.group(1)


def run(command: list[str]) -> int:
    print(f"$ {' '.join(command)}", flush=True)
    completed = subprocess.run(command, cwd=ROOT)
    return completed.returncode


def git_status() -> None:
    git_dir = ROOT / ".git"
    if not git_dir.exists():
        print("git: not a repository; skipping branch/status check", flush=True)
        return
    branch = subprocess.run(
        ["git", "branch", "--show-current"],
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL,
    ).stdout.strip()
    status = subprocess.run(
        ["git", "status", "--short"],
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL,
    ).stdout.strip()
    print(f"git branch: {branch or '(detached)'}", flush=True)
    print("git status: clean" if not status else f"git status:\n{status}", flush=True)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run compact SW doctor checks.")
    parser.add_argument(
        "--scope",
        choices=["repo", "installed", "all"],
        default="all",
        help="Pass-through scope for sw_consistency_check.py.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    version = parse_version()
    print(f"SW doctor: {version}", flush=True)
    print(f"root: {ROOT}", flush=True)
    git_status()
    check = ROOT / "tools" / "sw_consistency_check.py"
    code = run([sys.executable, str(check), "--scope", args.scope])
    if code == 0:
        print("SW doctor passed.")
        return 0
    print("SW doctor found issues.")
    print("Suggested first repair: python tools/sw_sync_installed.py")
    print("Then rerun: python tools/sw_doctor.py")
    return code


if __name__ == "__main__":
    raise SystemExit(main())
