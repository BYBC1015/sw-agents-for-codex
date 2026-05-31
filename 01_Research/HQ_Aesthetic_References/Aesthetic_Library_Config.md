# Aesthetic Library Config

Last updated: 2026-05-27

This file defines how SW locates the local aesthetic image library without hard-coding one disk path.

## Goal

The Git repository should stay lightweight. Tracked files store indexes, source links, profile rules, and scripts. Heavy images and contact sheets stay local-only and can move to another drive later.

## Default Roots

If no environment variable is set, SW uses repository-relative locations:

```text
01_Research/HQ_Aesthetic_References/
01_Research/Aesthetic_Daily_Selected/
01_Research/Aesthetic_Reference_Archive/
01_Research/Oscar_Frame_References/
```

## Portable Root Variables

Use these optional environment variables when moving the library:

| Variable | Purpose |
| --- | --- |
| `SW_AESTHETIC_LIBRARY_ROOT` | Main HQ library root. Expected to contain `images/` and `contact_sheets/`. |
| `SW_AESTHETIC_DAILY_ROOT` | Daily Selected root. Expected to contain `images/`, `contact_sheets/`, and optional `_candidate_review/`. |
| `SW_AESTHETIC_SOURCE_ROOT` | High-level source preview root. Expected to contain `images/` and `contact_sheets/`. |
| `SW_OSCAR_FRAME_ROOT` | Older Oscar frame reference root. Expected to contain `images/` and `contact_sheets/`. |
| `SW_OBSIDIAN_AESTHETIC_VAULT` | Optional Obsidian vault path. If unset, the sync script uses the currently open Obsidian vault when available; otherwise it uses `Obsidian_Aesthetic_Vault/` in the repository root. |

## Path Rule

- Keep tracked indexes in the SW repository.
- Keep image paths in indexes as logical/repository-relative paths when possible.
- Never commit absolute personal disk paths.
- If a library moves to another drive, set the variable above or create a local junction/symlink outside Git.
- Do not store API keys, upload tokens, client secrets, or private client file paths in this config.

## Doctor Command

Run the doctor after moving the library:

```powershell
python tools/aesthetic_library_doctor.py
```

The doctor reports which root is active, whether expected image/contact-sheet folders exist, approximate storage size, and which optional roots are missing.

## Obsidian Vault

The Obsidian layer is a Markdown-only browsing and curation layer. It embeds local preview images from existing contact sheets while keeping indexes and folder links available; it does not copy heavy images into the vault.

Sync or rebuild it with:

```powershell
python tools/sync_obsidian_aesthetic_vault.py
```

If you do not already have an Obsidian vault open, open this folder in Obsidian:

```text
Obsidian_Aesthetic_Vault/
```

If the vault moves to another drive, either open that vault in Obsidian and rerun the sync command, set `SW_OBSIDIAN_AESTHETIC_VAULT`, or pass `--vault <path>` explicitly.

## SW Runtime Rule

Normal project work should not run the doctor or load the Obsidian vault. Use them only for maintenance, relocation, missing-image debugging, visual browsing, curation, or when a user asks where the library lives.
