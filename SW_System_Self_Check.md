# SW System Self-Check

Date: 2026-05-26
Target runtime: V1.12.12

This file records the maintenance diagnosis for entry loss, version mismatch, stale chips, and likely future failure points. It is a working audit, not a user-facing startup file.

## Root Causes Found

1. Version source drift.
   - `VERSION.md` still said `V1.7.5` while active startup/sync/rescue replies already said `V1.7.6`.
   - Result: a conversation that follows `VERSION.md` can conflict with a conversation that follows `SW_Runtime_Index.md` or installed skills.

2. Multiple active surfaces.
   - SW is represented in project docs, user-level skills, plugin-level skills, command files, plugin manifest, README, and old conversation snapshots.
   - Updating only one surface creates inconsistent runtime behavior.

3. Sealed or stale UI chips.
   - Historical chats can replay the old tool/skill chip content even after disk files are fixed.
   - `sw-rescue` exists because normal startup/sync can be trapped by the stale chip that is being used to recover itself.

4. Trigger ownership collisions.
   - Earlier versions let startup and sync share similar aliases.
   - That caused `sw-v1-0` to answer when `sw-update` should have owned the turn.

5. UTF-8 read ambiguity on Windows.
   - PowerShell without explicit UTF-8 can display Chinese markdown as mojibake.
   - The file may be correct while the inspection output appears broken.

6. Local plugin discovery sensitivity.
   - Missing command files, stale `plugin.json`, BOM/encoding issues, or not copying update/rescue entries can make `/` or `@` entries disappear.

7. External tool state.
   - Git proxy, server firewall, relay availability, API keys, and local private config can break execution while SW logic is correct.
   - These must be separated from SW routing bugs during diagnosis.

## Preventive Checks Added

- `tools/sw_consistency_check.py` verifies:
  - root `VERSION.md` runtime version
  - active fixed replies in project docs
  - installed user-level `sw-v1-0`, `sw-update`, `sw-rescue`, `sw-help`, and tool skills
  - plugin command files and `plugin.json`
  - prompt reference files
  - obvious API-key and SW relay-token leakage patterns inside the repo
  - real mojibake/private-use character leaks in repo, user-skill, and plugin text files
  - HQ aesthetic image/video files are not accidentally tracked by Git
  - Obsidian aesthetic vault files and sync script are present

- `tools/sw_consistency_check.py --scope repo` is safe for GitHub Actions because it does not depend on local Codex user/plugin folders.

- `tools/sw_sync_installed.py` updates local user-level and plugin-level SW entries from the repository source.

- `tools/sw_doctor.py` prints the current version, git state, and the selected consistency check result in one compact maintenance pass.

- `tools/sw_bootstrap.py` is the new-computer readiness check: it syncs skills/plugin, runs doctor, checks Banana/Seedance key state, checks URL Relay config/health, checks local Black Background Cutout installation, checks Feishu Docs private config state, syncs/checks the Obsidian aesthetic vault, and reports ready versus needs-config without printing secrets.

- `tools/sync_obsidian_aesthetic_vault.py` creates a Markdown-only Obsidian vault for human browsing/curation without copying heavy images or launching WPS/Word.

- `tools/aesthetic_library_doctor.py` checks portable aesthetic-library roots after library moves or missing-image reports.

- `Examples/Regression_Test_Suite.md` now points maintenance work to this checker before publish.

## Known Risk Register

| Risk | Symptom | Required Response |
| --- | --- | --- |
| Root version drift | `/sw` and `@sw_update` report different versions | Run `python tools/sw_consistency_check.py`, then sync all active surfaces |
| Stale chip | Old conversation keeps returning a previous version | Use `/sw-rescue` or `@sw_rescue`; do not route through startup/update |
| Missing plugin entry | `/sw` shows no command or no result | Check plugin command files and plugin manifest JSON |
| Cross-project partial copy | Other project has startup but no update/rescue | Copy `SW_V1.0.md`, `sw_update.md`, and `sw_rescue.md` together |
| UTF-8 false alarm | Chinese docs look garbled in shell | Re-read with explicit UTF-8 before editing |
| Tool route bypass | Banana/Seedance generates before storyboard/prompt | Enforce upstream Studio role -> `prompt-director` -> tool skill |
| Poster system-text regression | Simple poster edits rebuild hero titles with plain fonts or explain workflow before showing the image | Use chip quick-edit hot path and image-native poster typography; system text only for exact info/editable-layer requests |
| Relay fallback surprise | Third-party temporary URL used without intent | Try SW media uploader first; fallback only on server failure plus confirmation/config |
| Aesthetic library bloat | Normal projects read too many references/images | Use `aesthetic-director` + `Aesthetic_Decision_Index.md` first; inspect images only on explicit moodboard/reference requests |
| Moved image library | Indexes point to missing local images | Set `SW_AESTHETIC_LIBRARY_ROOT` or related variables, then run `python tools/aesthetic_library_doctor.py` |
| Obsidian/WPS popup regression | Library maintenance opens Office/WPS save dialogs | Use the Markdown-only Obsidian vault sync; do not open `.docx`/WPS preview during aesthetic-library work |
| Cloned computer not ready | SW loads but Banana/Seedance/Relay/Feishu state is unclear | Run `python tools/sw_bootstrap.py` and follow its ready/needs-config report |
| Secret leakage | API key appears in repo docs/logs | Stop publish; remove key; rotate if already pushed |

## Maintenance Rule

Before every SW publish:

```powershell
$env:PYTHONUTF8='1'
python .\tools\sw_sync_installed.py
python .\tools\sw_doctor.py
python .\tools\sw_bootstrap.py --no-sync --no-network
```

If it fails, fix the listed surfaces before commit/push. Do not rely on manual grep alone for release readiness.
