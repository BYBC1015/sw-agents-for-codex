# SW Release Rules

This file keeps SW maintenance boring and reliable. It is for Codex-assisted development of the SW framework, not for daily design-project work.

## Goal

Prevent the recurring failure modes:

- startup, update, and rescue entries reporting different versions
- local plugin commands disappearing after partial updates
- user-level skills drifting from repository source
- GitHub receiving a release that has not passed the cheap checks
- API keys, relay tokens, or private config being committed by accident

## Branch Rule

Use a dedicated branch for every meaningful SW maintenance change:

```text
codex/sw-v<version>-<short-topic>
```

Examples:

```text
codex/sw-v1-7-8-release-infra
codex/sw-v1-8-0-new-tool-routing
```

Small wording-only fixes may stay on the current maintenance branch, but anything that changes runtime rules, skills, tools, or installed entries should get its own branch.

## Local Maintenance Flow

1. Make the smallest scoped change.
2. Bump `VERSION.md` only when runtime behavior, skills, tools, prompts, entries, or maintenance infrastructure changed.
3. Update fixed replies in startup, sync, and rescue files.
4. Update `Architecture_Update_Log.md` and README changelog.
5. Run:

```powershell
$env:PYTHONUTF8='1'
python .\tools\sw_sync_installed.py
python .\tools\sw_doctor.py
```

6. If only repository CI is needed:

```powershell
python .\tools\sw_consistency_check.py --scope repo
```

7. Commit only source files. Do not commit local keys, `.env`, generated outputs, payloads, responses, or private relay tokens.

## GitHub CI Rule

GitHub Actions runs repository-only checks. It must not depend on the developer's local Codex plugin folder or user-level skill folder.

CI should fail when:

- `VERSION.md` cannot be parsed
- fixed startup/sync/rescue replies are stale
- required prompt/tool reference files are missing
- obvious API keys or SW relay tokens appear in committed files

Local installed-entry checks remain the job of:

```powershell
python .\tools\sw_doctor.py --scope all
```

## Sync Rule

Use `tools/sw_sync_installed.py` after version bumps or entry changes. It updates:

- user-level `~/.codex/skills/sw-v1-0`
- user-level `~/.codex/skills/sw-update`
- user-level `~/.codex/skills/sw-rescue`
- user-level `~/.codex/skills/sw-help`
- user-level tool skills for Banana Pro, Seedance 2.0, and URL Relay
- local plugin skills and command files
- local plugin manifest version

The script does not store API keys or upload tokens. Tool credentials stay in environment variables or local private config files.

## Token Policy

These rules are meant to save model tokens:

- scripts compare files instead of asking Codex to manually read every path
- CI checks repository state without loading full SW context
- doctor output tells Codex exactly where to repair
- installed sync prevents repeated copy/paste maintenance

Daily SW project usage should not read this file.
