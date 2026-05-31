#!/usr/bin/env python3
"""Build a lightweight Obsidian vault for SW aesthetic references.

The vault is intentionally Markdown-only. It embeds local preview images from
the existing aesthetic library without copying large media, so normal SW runtime
remains cheap and the image library can move later via config/env paths.
"""

from __future__ import annotations

import argparse
import json
import os
import re
from datetime import date
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_VAULT = ROOT / "Obsidian_Aesthetic_Vault"
AESTHETIC_ROOT = ROOT / "01_Research" / "HQ_Aesthetic_References"
DAILY_ROOT = ROOT / "01_Research" / "Aesthetic_Daily_Selected"

SOURCE_FILES = {
    "decision": AESTHETIC_ROOT / "Aesthetic_Decision_Index.md",
    "master": AESTHETIC_ROOT / "HQ_Aesthetic_Master_Index.md",
    "config": AESTHETIC_ROOT / "Aesthetic_Library_Config.md",
    "queue": AESTHETIC_ROOT / "Top_Tier_Collection_Queue.md",
    "expansion": AESTHETIC_ROOT / "Aesthetic_Expansion_Queue_2026_05_25.md",
    "interactive": AESTHETIC_ROOT / "Interactive_Aesthetic_Browser_Tech_Notes.md",
    "daily": DAILY_ROOT / "Daily_Selected_Index.md",
    "daily_readme": DAILY_ROOT / "README.md",
    "oscar": ROOT / "01_Research" / "Oscar_Best_Picture_Visual_Reference.md",
    "oscar_frames": ROOT / "01_Research" / "Oscar_Frame_References" / "Oscar_Frame_Image_Index.md",
    "ai_film_notes": ROOT / "01_Research" / "AI_Film_Workflow_Reference_Notes.md",
    "ai_film_cases": ROOT / "01_Research" / "AI_Film_Workflow_Case_Studies.md",
    "prompt_image": ROOT / "Prompts" / "Image_Aesthetic_Prompt_Reference.md",
    "prompt_motion": ROOT / "Prompts" / "Video_Motion_Edit_Prompt_Rules.md",
    "visual_boards": ROOT / "Prompts" / "Visual_Development_Board_Rules.md",
}


def active_obsidian_vault() -> Path | None:
    config_candidates = []
    for base_name in ("APPDATA", "LOCALAPPDATA"):
        base = os.environ.get(base_name)
        if not base:
            continue
        config_candidates.extend(
            [
                Path(base) / "obsidian" / "obsidian.json",
                Path(base) / "Obsidian" / "obsidian.json",
            ]
        )
    for config_path in config_candidates:
        if not config_path.exists():
            continue
        try:
            data = json.loads(config_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            continue
        vaults = data.get("vaults") or {}
        candidates = []
        for item in vaults.values():
            path = item.get("path")
            if not path:
                continue
            candidates.append((bool(item.get("open")), int(item.get("ts") or 0), Path(path)))
        if candidates:
            candidates.sort(key=lambda item: (item[0], item[1]), reverse=True)
            return candidates[0][2]
    return None


def default_vault() -> Path:
    env_vault = os.environ.get("SW_OBSIDIAN_AESTHETIC_VAULT")
    if env_vault:
        return Path(env_vault)
    return active_obsidian_vault() or DEFAULT_VAULT


def read_text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8")


def write_if_changed(path: Path, content: str) -> bool:
    path.parent.mkdir(parents=True, exist_ok=True)
    normalized = content.replace("\r\n", "\n").rstrip() + "\n"
    if path.exists() and path.read_text(encoding="utf-8").replace("\r\n", "\n") == normalized:
        return False
    path.write_text(normalized, encoding="utf-8", newline="\n")
    return True


def display_path(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def rel_link(from_file: Path, target: Path, label: str | None = None) -> str:
    label = label or target.name
    try:
        rel = os.path.relpath(target, start=from_file.parent).replace("\\", "/")
    except ValueError:
        # Windows cannot create relative links across drives. Use a file URI so
        # an Obsidian vault on E: can still link to the SW repository on C:.
        rel = target.resolve().as_uri()
    return f"[{label}]({rel})"


def media_src(from_file: Path, target: Path) -> str:
    try:
        return os.path.relpath(target, start=from_file.parent).replace("\\", "/")
    except ValueError:
        return target.resolve().as_uri()


def media_embed(from_file: Path, target: Path, alt: str | None = None) -> str:
    clean_alt = (alt or target.stem).replace("[", "(").replace("]", ")")
    return f"![{clean_alt}]({media_src(from_file, target)})"


def media_gallery(
    note: Path,
    paths: list[Path],
    *,
    heading: str = "Visual Preview",
    limit: int = 12,
) -> str:
    if not paths:
        return f"## {heading}\n\nNo local preview images found yet.\n"
    lines = [
        f"## {heading}",
        "",
        "Embedded local previews. Source files stay in the SW image library and are not copied into the vault.",
        "",
    ]
    for path in paths[:limit]:
        lines.append(media_embed(note, path, path.name))
        lines.append("")
    if len(paths) > limit:
        lines.append(f"_Showing {limit} of {len(paths)} previews._")
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def wiki_path(path: Path) -> str:
    return path.with_suffix("").as_posix()


def split_cell(cell: str) -> list[str]:
    parts = [p.strip() for p in re.split(r",|，|;|；", cell) if p.strip()]
    return parts or [cell.strip()]


def parse_profiles() -> list[dict[str, str]]:
    text = read_text(SOURCE_FILES["decision"])
    profiles: list[dict[str, str]] = []
    in_profiles = False
    for raw_line in text.splitlines():
        line = raw_line.strip()
        if line == "## Profiles":
            in_profiles = True
            continue
        if in_profiles and line.startswith("## "):
            break
        if not in_profiles or not line.startswith("|"):
            continue
        cells = [cell.strip() for cell in line.strip("|").split("|")]
        if len(cells) != 5:
            continue
        if cells[0] in {"Profile", "---"} or set(cells[0]) == {"-"}:
            continue
        profiles.append(
            {
                "profile": cells[0],
                "best_for": cells[1],
                "visual_levers": cells[2],
                "avoid": cells[3],
                "source_lane": cells[4],
            }
        )
    return profiles


def parse_heuristics() -> list[tuple[str, str]]:
    text = read_text(SOURCE_FILES["decision"])
    rows: list[tuple[str, str]] = []
    in_table = False
    for raw_line in text.splitlines():
        line = raw_line.strip()
        if line == "## Selection Heuristics":
            in_table = True
            continue
        if in_table and line.startswith("## "):
            break
        if not in_table or not line.startswith("|"):
            continue
        cells = [cell.strip() for cell in line.strip("|").split("|")]
        if len(cells) != 2:
            continue
        if cells[0] in {"User Cues", "---"} or set(cells[0]) == {"-"}:
            continue
        rows.append((cells[0], cells[1]))
    return rows


def list_media(folder: Path, limit: int = 80) -> list[Path]:
    if not folder.exists():
        return []
    media_exts = {".jpg", ".jpeg", ".png", ".webp", ".gif"}
    files = [p for p in folder.rglob("*") if p.is_file() and p.suffix.lower() in media_exts]
    return sorted(files)[:limit]


def contact_sheets(root: Path, limit: int = 80) -> list[Path]:
    return list_media(root / "contact_sheets", limit=limit)


def candidate_sheets(root: Path, limit: int = 20) -> list[Path]:
    return list_media(root / "_candidate_review", limit=limit)


def profile_preview_media(profile: dict[str, str]) -> list[Path]:
    profile_id = profile["profile"]
    lane = profile["source_lane"].lower()
    previews: list[Path] = []

    film_contacts = contact_sheets(AESTHETIC_ROOT, limit=20)
    daily_contacts = contact_sheets(DAILY_ROOT, limit=20)
    daily_candidates = candidate_sheets(DAILY_ROOT, limit=10)

    if profile_id in {
        "monumental-cinematic-scale",
        "award-drama-interior-tension",
        "historical-material-realism",
    } or any(token in lane for token in ("dune", "film", "oscar", "historical")):
        previews.extend(film_contacts)
    if profile_id in {
        "restrained-human-realism",
        "warm-commercial-lifestyle",
        "minimal-premium-editorial",
        "high-energy-board-sequence",
    } or "daily" in lane:
        previews.extend(daily_contacts)
    if profile_id in {"lyrical-animation-color", "urban-night-texture", "uncanny-folklore-horror"}:
        previews.extend(film_contacts[:6])
        previews.extend(daily_candidates)
    if not previews:
        previews.extend(film_contacts[:3])
        previews.extend(daily_contacts[:3])

    deduped: list[Path] = []
    seen: set[str] = set()
    for path in previews:
        key = str(path)
        if key not in seen:
            deduped.append(path)
            seen.add(key)
    return deduped[:6]


def frontmatter(**items: object) -> str:
    lines = ["---"]
    for key, value in items.items():
        if isinstance(value, list):
            lines.append(f"{key}:")
            lines.extend(f"  - {item}" for item in value)
        else:
            lines.append(f"{key}: {json.dumps(value, ensure_ascii=False)}")
    lines.append("---")
    return "\n".join(lines) + "\n\n"


def build_home(vault: Path) -> str:
    note = vault / "Home.md"
    preview = media_gallery(
        note,
        contact_sheets(AESTHETIC_ROOT, limit=6) + contact_sheets(DAILY_ROOT, limit=4),
        heading="Visual Preview",
        limit=10,
    )
    return frontmatter(
        tags=["sw", "aesthetic-library", "home"],
        generated_on=date.today().isoformat(),
        sw_layer="obsidian-aesthetic-vault",
    ) + f"""# SW Aesthetic Vault

This vault is the visual browsing and curation layer for SW's aesthetic library. It does not replace the low-token runtime index; it embeds local previews from the existing library so large images are not duplicated.

## Start Here

- [[00_Index/Aesthetic Map|Aesthetic Map]]
- [[00_Index/Profile Router|Profile Router]]
- [[02_Collections/HQ Aesthetic Master Index|HQ Aesthetic Master Index]]
- [[02_Collections/Daily Selected|Daily Selected]]
- [[02_Collections/Oscar and Film Frames|Oscar and Film Frames]]
- [[03_Review/Curation Workflow|Curation Workflow]]

{preview}

## SW Runtime Rule

Normal SW project work should still read only {rel_link(note, SOURCE_FILES["decision"], "Aesthetic_Decision_Index.md")} unless the user explicitly asks to browse, compare, curate, or maintain the aesthetic library.

## Local Library Paths

- HQ references: {rel_link(note, AESTHETIC_ROOT, "01_Research/HQ_Aesthetic_References")}
- Daily selected: {rel_link(note, DAILY_ROOT, "01_Research/Aesthetic_Daily_Selected")}
- Storage config: {rel_link(note, SOURCE_FILES["config"], "Aesthetic_Library_Config.md")}
"""


def build_aesthetic_map(vault: Path, profiles: list[dict[str, str]]) -> str:
    note = vault / "00_Index" / "Aesthetic Map.md"
    preview = media_gallery(
        note,
        contact_sheets(AESTHETIC_ROOT, limit=6) + contact_sheets(DAILY_ROOT, limit=4),
        heading="Visual Entry Preview",
        limit=10,
    )
    profile_links = "\n".join(
        f"- [[01_Profiles/{p['profile']}|{p['profile']}]]: {p['best_for']}"
        for p in profiles
    )
    return frontmatter(
        tags=["sw", "aesthetic-library", "map"],
        generated_on=date.today().isoformat(),
    ) + f"""# Aesthetic Map

## Runtime Layer

- {rel_link(note, SOURCE_FILES["decision"], "Aesthetic_Decision_Index.md")}: compact profile decisions for daily SW work.
- [[00_Index/Profile Router|Profile Router]]: fast profile selection for human browsing.

{preview}

## Profile Notes

{profile_links}

## Collection Notes

- [[02_Collections/HQ Aesthetic Master Index|HQ Aesthetic Master Index]]
- [[02_Collections/Daily Selected|Daily Selected]]
- [[02_Collections/Oscar and Film Frames|Oscar and Film Frames]]
- [[02_Collections/AI Film Workflow Notes|AI Film Workflow Notes]]
- [[02_Collections/Prompt and Motion References|Prompt and Motion References]]

## Curation

- [[03_Review/Curation Workflow|Curation Workflow]]
- [[03_Review/Inbox|Inbox]]
"""


def build_profile_router(vault: Path, profiles: list[dict[str, str]], heuristics: list[tuple[str, str]]) -> str:
    note = vault / "00_Index" / "Profile Router.md"
    rows = [
        "| Profile | Best For | Visual Levers | Avoid | Source Lane |",
        "| --- | --- | --- | --- | --- |",
    ]
    for p in profiles:
        rows.append(
            f"| [[01_Profiles/{p['profile']}|{p['profile']}]] | {p['best_for']} | {p['visual_levers']} | {p['avoid']} | {p['source_lane']} |"
        )
    heuristic_rows = [
        "| User Cue | Default Profile |",
        "| --- | --- |",
    ]
    for cues, profile in heuristics:
        heuristic_rows.append(f"| {cues} | [[01_Profiles/{profile}|{profile}]] |")
    return frontmatter(
        tags=["sw", "aesthetic-library", "router"],
        generated_on=date.today().isoformat(),
    ) + f"""# Profile Router

Use this note when a project has no clear visual style and SW needs a high-taste default. Pick one main profile and at most one fallback.

## Profiles

{chr(10).join(rows)}

## Selection Heuristics

{chr(10).join(heuristic_rows)}
"""


def build_profile_note(vault: Path, profile: dict[str, str]) -> str:
    note = vault / "01_Profiles" / f"{profile['profile']}.md"
    levers = "\n".join(f"- {item}" for item in split_cell(profile["visual_levers"]))
    avoid = "\n".join(f"- {item}" for item in split_cell(profile["avoid"]))
    best_for = "\n".join(f"- {item}" for item in split_cell(profile["best_for"]))
    preview = media_gallery(note, profile_preview_media(profile), heading="Visual Preview", limit=6)
    return frontmatter(
        tags=["sw", "aesthetic-profile", f"profile/{profile['profile']}"],
        profile=profile["profile"],
        source_lane=profile["source_lane"],
        generated_on=date.today().isoformat(),
    ) + f"""# {profile['profile']}

## Use When

{best_for}

{preview}

## Visual Levers

{levers}

## Avoid

{avoid}

## Source Lane

{profile['source_lane']}

## Prompt-Safe Translation

Translate the profile into camera, lighting, composition, material, color, and pacing language. Do not copy exact film frames, named director signatures, logos, characters, typography, or proprietary layouts.

## SW Handoff

```text
aesthetic_profile: {profile['profile']}
visual_levers: {profile['visual_levers']}
reference_lane: {profile['source_lane']}
locked_constraints:
avoid: {profile['avoid']}
next_role:
```
"""


def build_collection_notes(vault: Path) -> dict[Path, str]:
    notes: dict[Path, str] = {}

    master = vault / "02_Collections" / "HQ Aesthetic Master Index.md"
    hq_contact_sheets = contact_sheets(AESTHETIC_ROOT, limit=120)
    contact_links = "\n".join(f"- {rel_link(master, p, p.name)}" for p in hq_contact_sheets) or "- No contact sheets found yet."
    hq_preview = media_gallery(master, hq_contact_sheets, heading="Visual Preview", limit=12)
    notes[master] = frontmatter(
        tags=["sw", "aesthetic-library", "collection", "hq"],
        generated_on=date.today().isoformat(),
    ) + f"""# HQ Aesthetic Master Index

{hq_preview}

## Source Indexes

- {rel_link(master, SOURCE_FILES["master"], "HQ_Aesthetic_Master_Index.md")}
- {rel_link(master, SOURCE_FILES["config"], "Aesthetic_Library_Config.md")}
- {rel_link(master, SOURCE_FILES["queue"], "Top_Tier_Collection_Queue.md")}
- {rel_link(master, SOURCE_FILES["expansion"], "Aesthetic_Expansion_Queue_2026_05_25.md")}
- {rel_link(master, SOURCE_FILES["interactive"], "Interactive_Aesthetic_Browser_Tech_Notes.md")}

## Image Folders

- {rel_link(master, AESTHETIC_ROOT / "images", "HQ images")}
- {rel_link(master, AESTHETIC_ROOT / "contact_sheets", "HQ contact sheets")}

## Contact Sheets

{contact_links}
"""

    daily = vault / "02_Collections" / "Daily Selected.md"
    daily_contact_sheets = contact_sheets(DAILY_ROOT, limit=120)
    daily_preview_paths = daily_contact_sheets + candidate_sheets(DAILY_ROOT, limit=20)
    daily_contact_links = "\n".join(f"- {rel_link(daily, p, p.name)}" for p in daily_contact_sheets) or "- No contact sheets found yet."
    daily_preview = media_gallery(daily, daily_preview_paths, heading="Visual Preview", limit=12)
    notes[daily] = frontmatter(
        tags=["sw", "aesthetic-library", "collection", "daily-selected"],
        generated_on=date.today().isoformat(),
    ) + f"""# Daily Selected

{daily_preview}

## Source Indexes

- {rel_link(daily, SOURCE_FILES["daily"], "Daily_Selected_Index.md")}
- {rel_link(daily, SOURCE_FILES["daily_readme"], "Daily Selected README")}

## Image Folders

- {rel_link(daily, DAILY_ROOT / "images", "Daily images")}
- {rel_link(daily, DAILY_ROOT / "contact_sheets", "Daily contact sheets")}
- {rel_link(daily, DAILY_ROOT / "_candidate_review", "Candidate review")}

## Contact Sheets

{daily_contact_links}
"""

    oscar = vault / "02_Collections" / "Oscar and Film Frames.md"
    oscar_preview = media_gallery(oscar, contact_sheets(AESTHETIC_ROOT, limit=120), heading="Visual Preview", limit=12)
    notes[oscar] = frontmatter(
        tags=["sw", "aesthetic-library", "collection", "film-frames"],
        generated_on=date.today().isoformat(),
    ) + f"""# Oscar and Film Frames

Use these sources to study visual grammar only. Do not reproduce exact frames, protected characters, titles, logos, or unique production designs.

{oscar_preview}

## Sources

- {rel_link(oscar, SOURCE_FILES["oscar"], "Oscar_Best_Picture_Visual_Reference.md")}
- {rel_link(oscar, SOURCE_FILES["oscar_frames"], "Oscar_Frame_Image_Index.md")}
- {rel_link(oscar, AESTHETIC_ROOT / "Oscar_HQ_Frame_Set.md", "Oscar_HQ_Frame_Set.md")}
- {rel_link(oscar, AESTHETIC_ROOT / "Film_HQ_Reference_Set_2026_05_24.md", "Film_HQ_Reference_Set_2026_05_24.md")}
- {rel_link(oscar, AESTHETIC_ROOT / "Open_HQ_Aesthetic_Study_Set.md", "Open_HQ_Aesthetic_Study_Set.md")}
"""

    ai_film = vault / "02_Collections" / "AI Film Workflow Notes.md"
    notes[ai_film] = frontmatter(
        tags=["sw", "aesthetic-library", "collection", "ai-film"],
        generated_on=date.today().isoformat(),
    ) + f"""# AI Film Workflow Notes

Use these notes to improve worldbuilding, frame continuity, anti-AI surface treatment, sound/edit thinking, and image-to-video handoffs.

## Sources

- {rel_link(ai_film, SOURCE_FILES["ai_film_notes"], "AI_Film_Workflow_Reference_Notes.md")}
- {rel_link(ai_film, SOURCE_FILES["ai_film_cases"], "AI_Film_Workflow_Case_Studies.md")}
"""

    prompt = vault / "02_Collections" / "Prompt and Motion References.md"
    notes[prompt] = frontmatter(
        tags=["sw", "aesthetic-library", "collection", "prompt-motion"],
        generated_on=date.today().isoformat(),
    ) + f"""# Prompt and Motion References

These are deep references. Do not load them for ordinary SW startup; use them when prompt quality, AI feel, camera movement, or storyboard boards need refinement.

## Sources

- {rel_link(prompt, SOURCE_FILES["prompt_image"], "Image_Aesthetic_Prompt_Reference.md")}
- {rel_link(prompt, SOURCE_FILES["prompt_motion"], "Video_Motion_Edit_Prompt_Rules.md")}
- {rel_link(prompt, SOURCE_FILES["visual_boards"], "Visual_Development_Board_Rules.md")}
"""

    return notes


def build_review_notes(vault: Path) -> dict[Path, str]:
    workflow = vault / "03_Review" / "Curation Workflow.md"
    inbox = vault / "03_Review" / "Inbox.md"
    notes = {
        workflow: frontmatter(
            tags=["sw", "aesthetic-library", "curation"],
            generated_on=date.today().isoformat(),
        ) + """# Curation Workflow

## Keep

- The image teaches a clear composition, lighting, color, staging, material, rhythm, or typography lesson.
- The reference can be translated into neutral design language.
- The source lane strengthens an existing profile or fills a real gap.

## Remove

- Low resolution without learning value.
- Generic AI surface, plastic skin, random detail, or overused prompt look.
- Duplicates that do not add a new visual lesson.
- Images that rely on protected logos, character likeness, or exact brand/film replication.

## Tagging

- `#profile/restrained-human-realism`
- `#profile/monumental-cinematic-scale`
- `#profile/award-drama-interior-tension`
- `#profile/urban-night-texture`
- `#profile/warm-commercial-lifestyle`
- `#profile/lyrical-animation-color`
- `#profile/minimal-premium-editorial`
- `#profile/historical-material-realism`
- `#profile/uncanny-folklore-horror`
- `#profile/high-energy-board-sequence`
""",
    }
    if not inbox.exists():
        notes[inbox] = frontmatter(
            tags=["sw", "aesthetic-library", "inbox"],
            generated_on=date.today().isoformat(),
        ) + """# Inbox

Drop notes, source links, or candidate image paths here before sorting them into profiles or collection notes.
"""
    return notes


def build_templates(vault: Path) -> dict[Path, str]:
    return {
        vault / "Templates" / "Profile Note.md": """---
tags:
  - sw
  - aesthetic-profile
profile:
source_lane:
---

# {{title}}

## Use When

## Visual Levers

## Avoid

## Prompt-Safe Translation

## Source Lane
""",
        vault / "Templates" / "Frame Study.md": """---
tags:
  - sw
  - frame-study
profile:
source:
---

# {{title}}

## What Works

## Composition

## Light / Color

## Material / Texture

## Prompt-Safe Translation

## Avoid Copying
""",
        vault / "Templates" / "Project Moodboard.md": """---
tags:
  - sw
  - project-moodboard
project:
profile:
---

# {{title}}

## Goal

## Locked Profile

## Reference Notes

## Do

## Avoid
""",
    }


def build_obsidian_config(vault: Path) -> dict[Path, str]:
    return {
        vault / ".obsidian" / "app.json": json.dumps(
            {
                "alwaysUpdateLinks": True,
                "showLineNumber": False,
                "showInlineTitle": True,
                "newFileLocation": "folder",
                "newFileFolderPath": "03_Review",
                "attachmentFolderPath": "Attachments",
            },
            ensure_ascii=False,
            indent=2,
        ),
        vault / ".obsidian" / "appearance.json": json.dumps(
            {
                "accentColor": "#4d7cff",
                "cssTheme": "",
                "enabledCssSnippets": [],
                "baseFontSize": 16,
            },
            ensure_ascii=False,
            indent=2,
        ),
        vault / ".obsidian" / "core-plugins.json": json.dumps(
            [
                "file-explorer",
                "global-search",
                "switcher",
                "graph",
                "backlink",
                "outgoing-link",
                "tag-pane",
                "page-preview",
                "templates",
                "note-composer",
                "command-palette",
                "markdown-importer",
                "properties",
            ],
            ensure_ascii=False,
            indent=2,
        ),
        vault / ".obsidian" / "templates.json": json.dumps(
            {"folder": "Templates", "dateFormat": "YYYY-MM-DD", "timeFormat": "HH:mm"},
            ensure_ascii=False,
            indent=2,
        ),
    }


def build_gitignore(vault: Path) -> str:
    return """# Obsidian local workspace state
.obsidian/workspace.json
.obsidian/workspace-mobile.json
.obsidian/cache/

# Optional local attachments stay local unless intentionally curated.
# The sync script embeds previews from the SW image library; it does not copy
# those images into the vault.
Attachments/
"""


def sync(vault: Path) -> dict[str, object]:
    profiles = parse_profiles()
    heuristics = parse_heuristics()
    changed: list[str] = []

    files: dict[Path, str] = {
        vault / "README.md": build_home(vault),
        vault / "Home.md": build_home(vault),
        vault / "00_Index" / "Aesthetic Map.md": build_aesthetic_map(vault, profiles),
        vault / "00_Index" / "Profile Router.md": build_profile_router(vault, profiles, heuristics),
        vault / ".gitignore": build_gitignore(vault),
    }
    for profile in profiles:
        path = vault / "01_Profiles" / f"{profile['profile']}.md"
        files[path] = build_profile_note(vault, profile)
    files.update(build_collection_notes(vault))
    files.update(build_review_notes(vault))
    files.update(build_templates(vault))
    files.update(build_obsidian_config(vault))

    for path, content in files.items():
        if write_if_changed(path, content):
            changed.append(display_path(path))

    config = {
        "vault": str(vault),
        "source_root": str(AESTHETIC_ROOT),
        "daily_root": str(DAILY_ROOT),
        "generated_on": date.today().isoformat(),
        "runtime_note": "SW normal runtime reads Aesthetic_Decision_Index.md; Obsidian is for human browsing and curation.",
    }
    config_path = vault / "obsidian-vault-config.json"
    if write_if_changed(config_path, json.dumps(config, ensure_ascii=False, indent=2)):
        changed.append(display_path(config_path))

    return {
        "vault": str(vault),
        "profiles": len(profiles),
        "changed": changed,
        "changed_count": len(changed),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Sync SW aesthetic references into an Obsidian vault.")
    parser.add_argument("--vault", type=Path, default=default_vault())
    parser.add_argument("--json", action="store_true", help="Print machine-readable result.")
    args = parser.parse_args()

    result = sync(args.vault.resolve())
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(f"Obsidian aesthetic vault synced: {result['vault']}")
        print(f"Profiles: {result['profiles']}; changed files: {result['changed_count']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
