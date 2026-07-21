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


def run(command: list[str], label: str) -> int:
    print(f"check: {label}", flush=True)
    completed = subprocess.run(command, cwd=ROOT)
    return completed.returncode


def summarize_git_status(status: str) -> str:
    counts = {
        "modified": 0,
        "untracked": 0,
        "staged": 0,
        "deleted": 0,
        "renamed": 0,
        "other": 0,
    }
    for line in status.splitlines():
        if not line:
            continue
        if line.startswith("??"):
            counts["untracked"] += 1
            continue
        code = line[:2]
        if "R" in code:
            counts["renamed"] += 1
        if "D" in code:
            counts["deleted"] += 1
        if "M" in code:
            counts["modified"] += 1
        if code[0] not in {" ", "?"}:
            counts["staged"] += 1
        if not any(marker in code for marker in ("M", "D", "R")) and code[0] not in {" ", "?"}:
            counts["other"] += 1
    changed = sum(1 for line in status.splitlines() if line and not line.startswith("??"))
    return (
        f"changed={changed} modified={counts['modified']} "
        f"untracked={counts['untracked']} staged={counts['staged']} "
        f"deleted={counts['deleted']} renamed={counts['renamed']} other={counts['other']}"
    )


def git_status(details: bool = False) -> None:
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
    ).stdout.rstrip("\r\n")
    print(f"git branch: {branch or '(detached)'}", flush=True)
    if not status:
        print("git status: clean", flush=True)
        return
    if details:
        print(f"git status:\n{status}", flush=True)
        return
    print(f"git status summary: {summarize_git_status(status)}", flush=True)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run compact SW doctor checks.")
    parser.add_argument(
        "--scope",
        choices=["repo", "installed", "all"],
        default="repo",
        help="Pass-through scope for sw_consistency_check.py.",
    )
    parser.add_argument(
        "--profile",
        choices=["hot", "work", "release"],
        default="hot",
        help="Pass-through profile for sw_consistency_check.py.",
    )
    parser.add_argument(
        "--details",
        action="store_true",
        help="Print full git status instead of the compact summary.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    version = parse_version()
    print(f"SW doctor: {version}", flush=True)
    print(f"root: {ROOT}", flush=True)
    git_status(details=args.details)
    check = ROOT / "tools" / "sw_consistency_check.py"
    code = run(
        [sys.executable, str(check), "--scope", args.scope, "--profile", args.profile],
        label=f"SW consistency ({args.scope}, {args.profile})",
    )
    if code == 0:
        print("SW doctor passed.")
        return 0
    print("SW doctor found issues.")
    if args.profile != "release":
        print("Suggested deeper check: run release-level SW doctor with details.")
    else:
        print("Suggested first repair: resync installed SW entries.")
        print("Then rerun release-level SW doctor.")
    return code


if __name__ == "__main__":
    raise SystemExit(main())
