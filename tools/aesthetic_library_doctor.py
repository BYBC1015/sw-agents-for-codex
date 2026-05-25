#!/usr/bin/env python3
"""Check the local SW aesthetic library roots.

The doctor is intentionally read-only and dependency-free. It helps move large
image libraries to another disk without changing tracked SW indexes.
"""

from __future__ import annotations

import os
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


ROOTS = [
    {
        "name": "HQ aesthetic library",
        "env": "SW_AESTHETIC_LIBRARY_ROOT",
        "default": ROOT / "01_Research" / "HQ_Aesthetic_References",
        "required": ["images", "contact_sheets"],
    },
    {
        "name": "Daily selected library",
        "env": "SW_AESTHETIC_DAILY_ROOT",
        "default": ROOT / "01_Research" / "Aesthetic_Daily_Selected",
        "required": ["images", "contact_sheets"],
    },
    {
        "name": "Source preview library",
        "env": "SW_AESTHETIC_SOURCE_ROOT",
        "default": ROOT / "01_Research" / "Aesthetic_Reference_Archive",
        "required": ["images", "contact_sheets"],
    },
    {
        "name": "Oscar frame legacy library",
        "env": "SW_OSCAR_FRAME_ROOT",
        "default": ROOT / "01_Research" / "Oscar_Frame_References",
        "required": ["images", "contact_sheets"],
    },
]


IMAGE_SUFFIXES = {".jpg", ".jpeg", ".png", ".webp", ".avif"}


def active_root(item: dict[str, object]) -> tuple[Path, bool]:
    env = str(item["env"])
    value = os.environ.get(env)
    if value:
        return Path(value).expanduser(), True
    return Path(item["default"]), False


def folder_size(path: Path) -> tuple[int, int]:
    files = 0
    total = 0
    if not path.exists():
        return files, total
    for child in path.rglob("*"):
        if child.is_file():
            files += 1
            try:
                total += child.stat().st_size
            except OSError:
                pass
    return files, total


def image_count(path: Path) -> int:
    if not path.exists():
        return 0
    return sum(1 for child in path.rglob("*") if child.is_file() and child.suffix.lower() in IMAGE_SUFFIXES)


def fmt_bytes(num: int) -> str:
    value = float(num)
    for unit in ["B", "KB", "MB", "GB", "TB"]:
        if value < 1024 or unit == "TB":
            return f"{value:.1f} {unit}" if unit != "B" else f"{int(value)} B"
        value /= 1024
    return f"{num} B"


def main() -> int:
    issues: list[str] = []
    print("SW aesthetic library doctor")
    print(f"Repository: {ROOT}")

    for item in ROOTS:
        path, from_env = active_root(item)
        label = str(item["name"])
        env = str(item["env"])
        source = f"{env}" if from_env else "repo default"
        print(f"\n[{label}]")
        print(f"root: {path}")
        print(f"source: {source}")

        if not path.exists():
            issues.append(f"{label}: root does not exist: {path}")
            print("status: missing root")
            continue

        for folder in item["required"]:  # type: ignore[index]
            sub = path / str(folder)
            if sub.exists():
                print(f"{folder}: ok ({image_count(sub)} image files)")
            else:
                issues.append(f"{label}: missing {folder}/ under {path}")
                print(f"{folder}: missing")

        files, total = folder_size(path)
        print(f"files: {files}")
        print(f"size: {fmt_bytes(total)}")

    if issues:
        print("\nIssues:")
        for issue in issues:
            print(f"- {issue}")
        return 1

    print("\nAll configured aesthetic library roots look usable.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
