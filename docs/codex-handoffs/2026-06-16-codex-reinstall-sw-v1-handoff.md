# Codex Reinstall Handoff - SW_V1.0 Project

Date: 2026-06-16

## Project Location

- Project folder: `C:\Users\Administrator\Documents\New project`
- Handoff file: `C:\Users\Administrator\Documents\New project\docs\codex-handoffs\2026-06-16-codex-reinstall-sw-v1-handoff.md`
- Git branch: `codex/sw-v1-12-14-storyboard-animatic-seedance`
- Current HEAD: `56594f1 Update SW runtime to V1.12.13`
- Current runtime version in files: `V1.12.17`
- Stable SW invocation name: `SW_V1.0`
- Stable user entries: `/sw`, `/SW_V1.0`, `@SW_V1.0`

This is the local SW Agents for Codex project. It contains the SW_V1.0 design studio framework, local role skills, prompt rules, tool skills, bootstrap scripts, install/doctor scripts, and documentation for reinstalling or syncing SW into Codex.

## Current Goal

Prepare a detailed handoff before reinstalling Codex so a fresh Codex session can continue from the current project state without relying on old conversation history.

Primary continuity goal after reinstall:

1. Reopen this project folder.
2. Inspect this handoff first.
3. Verify the repo state still matches the notes below.
4. Run the SW install/bootstrap flow from the repo.
5. Confirm `/sw` replies with `SW loaded successfully. Current version: V1.12.17`.

## Important Current State

The project is not clean. There are many modified tracked files and several untracked files. Do not assume the last Git commit contains the current working version.

The working tree includes local changes for runtime versions after the current HEAD commit:

- `V1.12.14`: Storyboard Animatic Sheet and Seedance storyboard execution prompt path.
- `V1.12.15`: Architecture pull instruction repair and Seedance storyboard prompt deduplication.
- `V1.12.16`: Public GitHub README/docs/collaboration polish.
- `V1.12.17`: Project Asset Graph before storyboard for video/film/campaign/product/storyboard continuity.

The current files report `V1.12.17`, while the latest commit is still `V1.12.13`. This means the post-`V1.12.13` work must be preserved via the working tree, a commit, or a full folder backup before any destructive reinstall or cleanup.

## What Was Already Checked

Inspected key project files:

- `VERSION.md`
- `README.md`
- `INSTALL_SW.md`
- `docs/REPOSITORY_MAP.md`
- `docs/codex-handoffs/2026-06-07-sw-v1-12-13-project-experience.md`
- root file/folder listing
- Git status, diff stat, recent log, and changed-file list

Created this new handoff:

- `docs/codex-handoffs/2026-06-16-codex-reinstall-sw-v1-handoff.md`

No Codex local state was archived, pruned, deleted, moved, or reinstalled during this handoff creation.

## Checks Already Run

From `C:\Users\Administrator\Documents\New project`:

```powershell
git status --short --branch
```

Result: branch is `codex/sw-v1-12-14-storyboard-animatic-seedance`; working tree has modified and untracked files.

```powershell
git diff --stat
```

Result: 37 tracked files changed, about 738 insertions and 306 deletions. There is also a warning that `sw_help.md` CRLF will be replaced by LF when Git touches it.

```powershell
git diff --check
```

Result: no whitespace errors reported; only the `sw_help.md` line-ending warning.

```powershell
python .\tools\sw_consistency_check.py --scope repo
```

Result: `SW consistency check passed for V1.12.17 (scope=repo).`

```powershell
python .\tools\sw_doctor.py --scope all
```

Result: `SW doctor passed.` It also ran `sw_consistency_check.py --scope all`, which passed for `V1.12.17`.

## Git Working Tree Summary

Tracked modified files reported by Git:

```text
.gitignore
AGENTS.md
AI_Tool_Integration_Rules.md
AI_Tool_Prompt_Profiles.md
Architecture_Update_Log.md
Auto_Assignment_Rules.md
Command_Aliases.md
Cost_Governor.md
Examples/Regression_Test_Suite.md
Feature_Trigger_Index.md
Legacy_Conversation_Recovery.md
PULL_ARCHITECTURE.md
Production_Pipeline_Map.md
Project_Minimal_Entry_Pack.md
Prompts/Prompt_Spec_Rules.md
Prompts/Tool_Official_Prompt_Deltas.md
Prompts/Video_Motion_Edit_Prompt_Rules.md
Prompts/Visual_Development_Board_Rules.md
README.md
SW_Runtime_Index.md
SW_System_Self_Check.md
SW_V1.0.md
Stage_Runbook.md
Start_New_Project.md
Studio_Skill_Dispatch_Protocol.md
Studio_Skill_Map.md
Studio_Skills/production-designer/SKILL.md
Studio_Skills/prompt-director/SKILL.md
Studio_Skills/storyboard-director/SKILL.md
Token_Budget.md
Tool_Registry.md
VERSION.md
seedance-2-video/SKILL.md
sw_help.md
sw_rescue.md
sw_update.md
tools/sw_sync_installed.py
```

Untracked files/folders reported by Git:

```text
.github/ISSUE_TEMPLATE/
.github/pull_request_template.md
CONTRIBUTING.md
SECURITY.md
docs/REPOSITORY_MAP.md
docs/SHOWCASE.md
docs/assets/
docs/codex-handoffs/2026-06-07-sw-v1-12-13-project-experience.md
docs/codex-handoffs/2026-06-16-codex-reinstall-sw-v1-handoff.md
```

These untracked files are part of the current project experience and should not be ignored during reinstall handoff. The new handoff file itself is also untracked until staged or committed.

## Main Project Structure

Core entry and runtime files:

- `AGENTS.md`: root Codex instructions and explicit SW activation gate.
- `SW_V1.0.md`: stable SW invocation entry.
- `SW_Runtime_Index.md`: compact runtime index loaded before deeper files.
- `Cost_Governor.md`: cost lanes and high-cost gates.
- `Stage_Runbook.md`: workflow stage rules.
- `Studio_Skill_Dispatch_Protocol.md`: current role-skill dispatch rules.
- `VERSION.md`: current runtime version and update log.
- `INSTALL_SW.md`: reinstall/bootstrap instructions.

Studio role skills:

- `Studio_Skills/brief-strategist/`
- `Studio_Skills/storyboard-director/`
- `Studio_Skills/production-designer/`
- `Studio_Skills/prompt-director/`
- `Studio_Skills/review-producer/`
- plus other specialist roles for decks, layout, film, edit, sound, history, tools, and delivery.

Tool skills:

- `banana-pro/`: OpenRouter/Banana Pro image generation wrapper.
- `seedance-2-video/`: Seedance 2.0 / Ark video generation wrapper.
- `url-relay/`: public URL relay for local media.
- `black-background-cutout/`: local simple-background cutout.
- `storyboard-visual-word/`: DOCX visual director handoff.
- `feishu-docs/`: Feishu/Lark Docs render or publish workflow.
- `kling-api/`: Kling API integration.

Maintenance scripts:

- `tools/sw_bootstrap.py`: reinstall/sync local Codex skills and plugin entries.
- `tools/sw_consistency_check.py`: repo/install consistency checks.
- `tools/sw_doctor.py`: broader local health check.
- `tools/sw_sync_installed.py`: sync installed local skills/plugin from repo.

Documentation:

- `README.md`: public project overview and quick start.
- `docs/REPOSITORY_MAP.md`: map of key folders and files.
- `docs/SHOWCASE.md`: storyboard showcase and examples.
- `docs/codex-handoffs/`: session and reinstall handoffs.

## Current Runtime Rules To Preserve

Key behavior that must survive reinstall:

- SW is explicit-only. Ordinary design words such as poster, PPT, storyboard, image prompt, or video prompt must not start the full SW framework unless the user explicitly enters `/sw`, `/SW_V1.0`, `@SW_V1.0`, `调用 SW_V1.0`, `启用 SW_V1.0`, `拉取本项目架构`, or `按本项目架构执行`.
- `/sw` should reply first with: `SW loaded successfully. Current version: V1.12.17`.
- `@sw_update` and related sync aliases are handled by the sync entry, not the full SW startup.
- `/sw-rescue` and related rescue aliases are handled by the rescue entry, not the full SW startup.
- Normal SW project work uses Fast Path first: `SW_Runtime_Index.md` -> `Cost_Governor.md` -> `Studio_Skill_Dispatch_Protocol.md` -> selected `Studio_Skills/<skill>/SKILL.md`.
- After explicit SW startup, project replies should include a lightweight English-only role/cost trace.
- High-cost actions such as real AI image/video generation, uploads, publishing, or batch outputs require explicit user confirmation.
- API keys and upload tokens must stay in local private config, never in the repo, prompts, handoff files, or logs.
- Project Asset Graph is now required before storyboard for video/film/campaign/product-story/storyboard continuity routes unless fast mode makes explicit default assumptions.

## Private Config And Secrets

The repo does not store real API keys. After Codex reinstall, optional tool capabilities may need local private setup again.

Private paths and variables referenced by the project:

- Banana Pro real image generation: `OPENROUTER_API_KEY` or `~\.config\banana-pro\openrouter.env`
- Seedance real video generation: `ARK_API_KEY` or local private Seedance config
- URL Relay: private uploader token and relay config outside repo
- Feishu Docs publish: `~\.config\sw-feishu\config.json`, `FEISHU_APP_ID`, or `FEISHU_APP_SECRET`

Missing keys do not break the SW core framework. They only keep those tools in dry-run, payload-only, or needs-config mode.

## Known Warnings And Risks

- Working tree is dirty and contains important current changes. Do not run destructive Git commands such as reset/checkout-clean unless the changes have been intentionally committed, stashed, or backed up.
- Current branch name still mentions `V1.12.14`, but files are at `V1.12.17`. Treat file contents and `VERSION.md` as the runtime source of truth.
- HEAD commit is `V1.12.13`; do not assume a fresh clone from GitHub has `V1.12.17` unless these changes were committed and pushed first.
- `git diff --check` reports only a line-ending warning for `sw_help.md`; no whitespace errors were reported.
- Old PowerShell output may display Chinese as mojibake. That does not automatically mean files are corrupted. Prefer UTF-8-aware reads and avoid broad encoding rewrites unless a real file integrity check fails.
- `outputs/`, `banana_outputs/`, generated payloads, responses, local caches, and private configs should remain out of the repo.

## Open Decisions

Before or immediately after reinstall, decide:

1. Whether to commit the current `V1.12.14` to `V1.12.17` working tree changes.
2. Whether to push the branch or keep this as a local-only project folder.
3. Whether optional tool credentials should be restored now or only when each tool is needed.
4. Whether to use the current branch name or create a new branch named closer to `V1.12.17`.
5. Whether to keep old handoff files as historical context or archive them later.

## Recommended Reinstall Recovery Steps

1. Open the project folder: `C:\Users\Administrator\Documents\New project`.
2. Read this handoff first.
3. Check current repo state:

```powershell
git status --short --branch
```

4. Confirm version files still say `V1.12.17`:

```powershell
Get-Content .\VERSION.md
```

5. Run bootstrap from the repo root after Codex reinstall:

```powershell
python .\tools\sw_bootstrap.py
```

If Windows uses the Python launcher:

```powershell
py -3 .\tools\sw_bootstrap.py
```

6. Run health checks:

```powershell
python .\tools\sw_consistency_check.py --scope all
python .\tools\sw_doctor.py --scope all
git diff --check
```

7. In a fresh Codex chat, use `/sw`. Expected first reply:

```text
SW loaded successfully. Current version: V1.12.17
```

8. If old chips or old conversations show stale versions, use:

```text
/sw-rescue
```

Expected current rescue version should also be `V1.12.17`.

## Next 7 Concrete Steps For New Codex Session

1. Read this handoff and summarize the current project state before editing anything.
2. Run `git status --short --branch` and confirm whether the dirty working tree still matches this handoff.
3. Run `python .\tools\sw_consistency_check.py --scope all`.
4. Run `python .\tools\sw_doctor.py --scope all`.
5. Run `python .\tools\sw_bootstrap.py` only after confirming reinstall/sync is desired.
6. Test `/sw`, `@sw_update`, `/sw-rescue`, and `@sw_help` behavior in Codex.
7. If all checks pass, decide whether to commit the current `V1.12.17` state and include this handoff in that commit.

## Do Not Touch Without Explicit Approval

- Do not delete or reset the dirty working tree.
- Do not remove untracked documentation or `.github` templates.
- Do not print, copy, or commit private API keys or upload tokens.
- Do not run broad encoding rewrites just because terminal output is garbled.
- Do not treat ordinary design requests as SW startup unless the user explicitly invokes SW.
- Do not perform real paid image/video generation, upload, Feishu publish, or batch external actions without explicit user confirmation.

## Reactivation Prompt For Fresh Codex Chat

Paste this into a new Codex chat after reinstall:

```text
We are continuing from this handoff. Read this document first, inspect the current repo/project state, verify what still applies, and continue from the next steps without assuming the old chat context is available.

请读取这个完整项目交接文档，并从它接管 SW_V1.0 设计工作室系统项目：

C:\Users\Administrator\Documents\New project\docs\codex-handoffs\2026-06-16-codex-reinstall-sw-v1-handoff.md

这是完整项目交接，不是局部任务状态。先只读取理解项目，不要改文件。读完后先汇报：当前项目是什么、已有系统结构、关键风险、下一步建议。
```
