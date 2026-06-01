# SW V1.12.12 Session Handoff

Date: 2026-06-01

## Repo / Path / Branch

- Repo path: `C:\Users\Administrator\Documents\New project`
- Active branch: `codex/sw-v1-12-10-explicit-activation`
- Upstream: `origin/codex/sw-v1-12-10-explicit-activation`
- Latest pushed commit on this branch: `46efd72 Update SW runtime to V1.12.10`
- Current local runtime version: `V1.12.12`
- Current worktree state: dirty, with local uncommitted `V1.12.11` and `V1.12.12` changes.

## Current Goal

Prepare a complete handoff before archiving Codex history so a fresh Codex chat can continue SW_V1.0 maintenance without relying on old conversation context.

Immediate next goal after this handoff: review the uncommitted `V1.12.12` changes, then commit and push them on an appropriate branch or continue from the existing branch.

## Completed In This Session / Recent Work

1. Read and evaluated the full SW project handoff from:
   `C:\Users\Administrator\Documents\New project\docs\codex-handoffs\2026-05-28-sw-v1-project-handoff.md`

2. Earlier completed and pushed `V1.12.10` on branch `codex/sw-v1-12-10-explicit-activation`:
   - SW now starts only from explicit activation such as `/sw`, `/SW_V1.0`, `@SW_V1.0`, `调用 SW_V1.0`, `拉取本项目架构`, or `按本项目架构执行`.
   - Ordinary terms such as poster, PPT, storyboard, prompt, review, or revision no longer activate the full SW framework by themselves.
   - Installed user skill and local plugin copies were synced.
   - Push required bypassing a broken global Git proxy with:
     `git -c http.proxy= -c https.proxy= push -u origin codex/sw-v1-12-10-explicit-activation`

3. Added `V1.12.11` locally:
   - Added lightweight historical/cultural-heritage project nudge.
   - Added optional `Historical Drama Style Capsule`.
   - Historical accuracy remains confirmation-gated through `historical-consultant`.
   - Style capsule is not a new module and not an accuracy check.
   - Rule: keep the style capsule once as global `Visual Baseline`; write only per-scene/per-shot deltas.

4. User reported that another Codex chat landed `V1.12.12`, and local files confirm it:
   - Full-storyboard triggers: `生成全部分镜`, `完整分镜`, `全片分镜`, `全量跑分镜`, `按剧本生成所有镜头`.
   - Real script/storyboard shot count is authoritative.
   - Supplemental shots are allowed only when they serve a narrative function: establishing, transition, reaction, prop insert, action bridge, or rhythm pause.
   - Supplemental shots must be marked separately, e.g. `07A`, `12B`, `S01`.
   - Contact sheets use 3x3 pages.
   - Empty, missing, or failed slots stay black; do not force weak filler images to fill a page.
   - Installed user skill and plugin copies were reportedly synced in the other chat.

5. Evaluated a Terracotta Warriors storyboard Markdown file:
   `F:\WX\xwechat_files\wxid_4iwynk85ctkc22_1ab8\msg\file\2026-06\千年铭迹_兵马俑_分镜_仅景别焦段内容构图.md`
   - It has 7 scenes, 50 shots, about 260 seconds.
   - Every shot has `Shot Size`, `Camera Lens`, `Duration`, `Dialogue`, `Content`, `Composition`, and `Image Style Prompt`.
   - Key learning: global visual baseline + conditional object locks + per-shot deltas reduce AI-looking historical drama output.

6. Recorded a pending decision in the older handoff:
   `docs/codex-handoffs/2026-05-28-sw-v1-project-handoff.md`
   - Pending decision: whether the Terracotta Warriors storyboard prompt structure should become a formal reusable template.
   - Current leaning: record it as a high-quality historical-drama baseline, but do not make it the default SW storyboard format yet.

## Files Touched

Current modified files:

- `AGENTS.md`
- `Architecture_Update_Log.md`
- `Command_Aliases.md`
- `Cost_Governor.md`
- `Examples/Regression_Test_Suite.md`
- `Feature_Trigger_Index.md`
- `Legacy_Conversation_Recovery.md`
- `Production_Pipeline_Map.md`
- `Project_Control_Rules.md`
- `Project_Minimal_Entry_Pack.md`
- `Prompts/Prompt_Spec_Rules.md`
- `Prompts/Visual_Development_Board_Rules.md`
- `README.md`
- `SW_Runtime_Index.md`
- `SW_System_Self_Check.md`
- `SW_V1.0.md`
- `Stage_Runbook.md`
- `Start_New_Project.md`
- `Studio_Skill_Dispatch_Protocol.md`
- `Studio_Skills/prompt-director/SKILL.md`
- `Studio_Skills/storyboard-director/SKILL.md`
- `VERSION.md`
- `docs/codex-handoffs/2026-05-28-sw-v1-project-handoff.md`
- `sw_rescue.md`
- `sw_update.md`
- this handoff file

Key `V1.12.11` / `V1.12.12` locations:

- `VERSION.md`
- `Architecture_Update_Log.md`
- `SW_Runtime_Index.md`
- `Studio_Skills/storyboard-director/SKILL.md`
- `Studio_Skills/prompt-director/SKILL.md`
- `Prompts/Prompt_Spec_Rules.md`
- `Prompts/Visual_Development_Board_Rules.md`
- `Cost_Governor.md`
- `Production_Pipeline_Map.md`
- `README.md`

## Files Investigated

- `docs/codex-handoffs/2026-05-28-sw-v1-project-handoff.md`
- `Change_Log.md`
- `Obsidian_Aesthetic_Vault\03_Review\Inbox.md`
- `F:\WX\xwechat_files\wxid_4iwynk85ctkc22_1ab8\msg\file\2026-06\千年铭迹_兵马俑_分镜_仅景别焦段内容构图.md`
- Core SW runtime/routing files listed above.

## Commands / Checks Already Run

Repository state and inspection:

```powershell
git status --short --branch
git diff --name-only
git diff --name-status
git diff --stat
git log --oneline -5 --decorate
rg -n "Current runtime version|V1\.12\.12|V1\.12\.11|Full Storyboard|生成全部分镜|Historical Drama Style Capsule|历史剧胶片风格胶囊" ...
```

Sync and validation:

```powershell
python tools\sw_sync_installed.py
python tools\sw_consistency_check.py
python tools\sw_doctor.py
git diff --check
```

Latest check results:

- `python tools\sw_consistency_check.py` passed for `V1.12.12` with `scope=all`.
- `python tools\sw_doctor.py` passed for `V1.12.12`.
- `git diff --check` reported no whitespace errors, but did print a README CRLF warning.

Earlier push:

```powershell
git -c http.proxy= -c https.proxy= push -u origin codex/sw-v1-12-10-explicit-activation
```

## Known Errors / Warnings / Failing Checks

- No current failing SW consistency or doctor checks.
- `git diff --check` warning:
  `warning: in the working copy of 'README.md', CRLF will be replaced by LF the next time Git touches it`
- Earlier push initially failed because global Git proxy `proxy.example.com:26854` returned `Proxy CONNECT aborted`. It succeeded with one-command proxy bypass. The global proxy config was not changed.
- Branch name still says `sw-v1-12-10-explicit-activation`, but the local runtime is now `V1.12.12`. This is not functionally wrong, but may be confusing when creating the next PR.
- Some older files/history contain mojibake text. Do not do broad encoding rewrites unless explicitly requested; only fix scoped text when it affects current behavior.
- Worktree is dirty. Do not assume local changes are committed or pushed.

## Open Decisions

- Whether to commit `V1.12.11` and `V1.12.12` together as one patch commit, or split them into separate commits.
- Whether to continue using branch `codex/sw-v1-12-10-explicit-activation` or create a new branch such as `codex/sw-v1-12-12-storyboard-rules`.
- Whether the Terracotta Warriors storyboard prompt structure should become a formal reusable template. Current recorded leaning: keep as a high-quality historical-drama storyboard prompt baseline, not a default SW storyboard format.
- Whether `Historical Drama Style Capsule` should later get a dedicated compact reference file. Current implementation keeps it embedded in prompt/storyboard rules to avoid new default reads.
- Whether to update the older `2026-05-28` handoff more broadly. Current change only adds one pending decision.
- Whether to run broader release checks before PR; latest lite checks pass.

## Constraints / User Preferences

- User prefers lightweight framework behavior. Avoid framework bloat and unnecessary Markdown reads.
- Explicit SW activation is mandatory. Ordinary design words must not start SW.
- User likes reply-end suggestions/reminders, but only one light suggestion when useful.
- Do not auto-enable historical checking. Remind only; user must confirm.
- Historical accuracy and historical drama style are separate:
  - `historical-consultant` checks correctness.
  - `Historical Drama Style Capsule` improves visual groundedness / reduces AI feel.
- For full storyboard generation, do not force nine-grid filler frames. Use true story shot count and black slots for empty/missing/failed frames.
- For black-background cutout, treat it only as a quick cutout tool; it may have slight fringing and is not a solution for AI typography reuse.
- For AI poster display lettering, do not downgrade visual title effects into plain system fonts unless the user explicitly wants editable/plain text.
- User prefers pragmatic, concise communication and does not want long explanations unless needed.

## Do Not Touch Areas

- Do not run `git reset --hard`, `git checkout --`, or revert user/other-chat changes without explicit instruction.
- Do not delete local generated assets, aesthetic vault files, API configs, tool outputs, or ignored media.
- Do not print, move, or commit secrets/API keys/relay tokens.
- Do not change stable invocation name `SW_V1.0`.
- Do not make SW auto-activate from ordinary project terms.
- Do not convert every storyboard into the historical-drama template by default.
- Do not add new modules or heavy reference files unless the user confirms the value outweighs read cost.

## Next Concrete Steps

1. Review the current diff for `V1.12.11` and `V1.12.12`, especially `README.md` because Git reports a CRLF-to-LF warning.
2. Decide whether to split commits:
   - Commit A: historical drama style capsule / historical-cultural nudge.
   - Commit B: full-storyboard generation and 3x3 black-slot rules.
   Or make one combined `Update SW runtime to V1.12.12` commit.
3. If committing, run:
   ```powershell
   python tools\sw_consistency_check.py
   python tools\sw_doctor.py
   git diff --check
   ```
4. Stage only intended files. Include this handoff file if the user wants it committed.
5. Commit with a clear message, likely:
   `Update SW runtime to V1.12.12`
6. Push. If the old proxy error recurs, use:
   ```powershell
   git -c http.proxy= -c https.proxy= push
   ```
7. Open or update the PR. Existing PR URL pattern from prior push:
   `https://github.com/BYBC1015/sw-agents-for-codex/pull/new/codex/sw-v1-12-10-explicit-activation`

## Reactivation Prompt For Fresh Codex Chat

Paste this into a fresh Codex chat:

```text
请读取这个完整项目交接文档，并从它接管 SW_V1.0 设计工作室系统项目：

C:\Users\Administrator\Documents\New project\docs\codex-handoffs\2026-06-01-sw-v1-12-12-session-handoff.md

这是完整项目交接，不是局部任务状态。先只读理解项目，不要改文件。

读完后先汇报：
- 当前项目是什么
- 已有系统结构
- 已完成和未提交的关键改动
- 关键风险
- open decisions
- 下一步建议

汇报前可以只读检查 repo 状态，但不要修改文件、不要提交、不要推送。
项目路径：C:\Users\Administrator\Documents\New project
```
