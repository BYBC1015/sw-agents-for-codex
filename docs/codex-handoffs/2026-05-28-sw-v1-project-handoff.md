# SW_V1.0 设计工作室系统项目交接

生成日期：2026-05-28

## Reactivation Prompt

```text
We are continuing from this handoff. Read this document first, inspect the current repo state, verify what still applies, then continue the SW_V1.0 design studio system project without relying on the old Codex chat context.

Important: this is a full project handoff, not a last-task handoff. Treat the project as an evolving design-studio operating system for posters, storyboards, video prompts, AI image/video generation, delivery review, and tool integrations. Preserve the stable invocation name SW_V1.0 while current runtime version may advance.
```

## Project Identity

- Repo/path: `C:\Users\Administrator\Documents\New project`
- Git branch at handoff time: `codex/sw-v1-10-6-feishu-docs`
- Current runtime version: `V1.12.4`
- Stable invocation names: `/sw`, `/SW_V1.0`, `@SW_V1.0`
- Version sync entry: `@sw_update`
- Rescue entry for stale chips/conversations: `/sw-rescue`, `@sw_rescue`
- Project type: personal-to-team design studio automation framework for Codex
- Original goal: build a reusable Codex-driven workflow for daily design work, including posters, video storyboards, final video effect planning, edit plans, prompt writing, revision control, delivery review, and token/cost control.

## Core Intent

This project is not a single deliverable. It is a local SW design-studio runtime that lets the user open a new Codex conversation, invoke SW, paste a client/boss/self brief, and have Codex run the appropriate design workflow with minimal friction.

The user repeatedly clarified these principles:

- New chat equals new design project.
- The user does not want to fill templates manually.
- Codex should read the project rules, identify the task type, ask only a few high-value questions, then produce useful work directly in the chat unless files are requested.
- The architecture should behave like a small design studio, with roles/skills for brief, research, creative direction, poster, storyboard, cinematography, editing, sound, review, delivery, and tool integration.
- Prompt quality matters. Vague words like "closer" or "farther" are not enough; image/video prompts need precise framing, lens, camera distance, light, material, texture, motion, timing, and negative constraints.
- Cost control matters. Do low-cost judgment and structure first; delay long-form, batch variation, image generation, video generation, and heavy tool runs until direction and acceptance criteria are clear.
- Versioning matters. Every architecture change must update version numbers and change logs in the same turn.
- Historical conversations may cache stale skill behavior, so the system needs update/rescue routes.

## Current Architecture Snapshot

The project has evolved into a user-level and project-local skill/plugin ecosystem:

- `AGENTS.md`: main Codex operating rulebook for new design conversations.
- `SW_V1.0.md`: stable invocation protocol.
- `sw_update.md`: sync current version into stale chats or installs.
- `sw_rescue.md`: stronger rescue path for stale skill chips or old cached runtime.
- `VERSION.md`: current version, version rules, bump policy, version history.
- `Architecture_Update_Log.md`: detailed change log with reason, impact, cost, and compatibility notes.
- `SW_Runtime_Index.md`: compact runtime index for lower-cost startup.
- `Stage_Runbook.md`: stage entry/output/exit conditions.
- `Project_Control_Rules.md`: command shortcuts, quality gates, user-interaction style, platform defaults.
- `Cost_Governor.md`: cost lane rules and high-cost gates.
- `Studio_Skill_Map.md`, `Studio_Skill_Dispatch_Protocol.md`, `Studio_Role_Label_Protocol.md`: role dispatch and visible role trace rules.
- `Auto_Assignment_Rules.md`: automatic role assignment by project type and stage.
- `Production_Pipeline_Map.md`: poster/video/film/prompt/finishing pipelines.
- `Tool_Registry.md`, `AI_Tool_Integration_Rules.md`, `AI_Tool_Prompt_Profiles.md`: tool integration, prompt conversion, future tool registration.
- `Prompts/`: prompt rules and reference layers.
- `Studio_Skills/`: project-local Studio role skills.
- `banana-pro/`, `seedance-2-video/`, `url-relay/`, `storyboard-visual-word/`, `feishu-docs/`, `kling-api/`: explicit downstream tool skills/integrations.
- `Obsidian_Aesthetic_Vault/` and `01_Research/HQ_Aesthetic_References/`: local aesthetic browsing and compact decision index.

## Version History That Matters

The current version log in `README.md` and `VERSION.md` is the source of truth. The most relevant recent changes are:

- `V1.12.4`: official prompt delta layer for Seedance/Jimeng, Kling, Banana Pro/Gemini image, OpenAI image, loaded only when needed; fixed review-feedback loop through `Review Delta Packet`.
- `V1.12.3`: storyboard reference angle frame rule: one selected still can lock camera/geometry/lighting before batch generation.
- `V1.12.2`: Obsidian aesthetic browsing image embedding and storyboard grouping rule: 15s is max duration, 9-grid is upper limit, not target.
- `V1.12.0`: Markdown-only Obsidian Aesthetic Vault.
- `V1.11.0`: `feishu-docs` explicit handoff tool.
- `V1.10.5`: bootstrap/install infrastructure for new computers.
- `V1.10.4`: poster image-native typography rule.
- `V1.10.3`: poster quick-edit fast route.
- `V1.9.1`: Banana Pro backend through OpenRouter Gemini image model.
- `V1.9.0`: `storyboard-visual-word` DOCX visual handoff.
- `V1.8.0`: visual development board workflow.
- `V1.7.0`: URL Relay for local media to public URL.
- `V1.6.0`: Seedance 2.0 video generation layer.
- `V1.4.0`: project-local `.sw/` memory layer.
- `V1.1.0`: expansion into full poster/video/film design studio roles.

## User Preferences And Operating Style

- Reply should be practical and production-oriented, not a teaching lecture.
- For projects, default to working inside the chat; create files when useful for handoff, archive, delivery, or team use.
- Ask at most 3 key questions per stage. Prefer reasonable assumptions when safe.
- For design work, do not produce generic or "AI-looking" output. User values cinematic taste, real texture, strong references, and professional self-checking.
- For video/storyboards, do not over-explain every method unless asked; give concrete scripts, shot lists, image/video prompts, contact sheets, review notes, and next steps.
- For prompt writing, be precise about distance, shot size, lens/camera language, light direction, color, material, texture, environment, motion, timing, and negative constraints.
- For revisions, classify change scope first. Do not casually rebuild the whole project.
- For high-cost tools, confirm scope and use smallest useful output first unless user explicitly asks to proceed.
- For exact text/logo/QR/legal/copyright-sensitive outputs, warn and route to safer editable/QA layers.

## Current Git / Workspace State

At handoff time the repo has many existing modified and untracked files. Do not revert them unless explicitly instructed.

Observed branch:

```text
codex/sw-v1-10-6-feishu-docs
```

Observed changed areas include:

- Modified architecture/runtime files such as `AGENTS.md`, `README.md`, `VERSION.md`, `SW_Runtime_Index.md`, `SW_V1.0.md`, `Stage_Runbook.md`, `Project_Control_Rules.md`, `Cost_Governor.md`, `Tool_Registry.md`.
- Modified prompt and role files under `Prompts/` and `Studio_Skills/`.
- Modified install/sync/check scripts under `tools/`.
- Untracked or newer areas: `Obsidian_Aesthetic_Vault/`, `Prompts/Tool_Official_Prompt_Deltas.md`, `feishu-docs/`, `kling-api/`, `outputs/`, `tools/sync_obsidian_aesthetic_vault.py`.

Before committing or publishing, inspect the diff carefully and separate intentional architecture updates from generated/local artifacts.

## Major Work Already Completed

1. Built the initial design project template:
   - `00_Brief`
   - `01_Research`
   - `02_Direction`
   - `03_Poster`
   - `04_Storyboard`
   - `05_EditPlan`
   - `06_FinalReview`
   - `99_Archive`

2. Converted it from a folder template into a callable SW runtime:
   - Stable invocation name `SW_V1.0`.
   - English success reply to avoid Chinese encoding issues.
   - Startup files usable in new conversations and other project folders.

3. Added version and update discipline:
   - Automatic version bump rule.
   - `Architecture_Update_Log.md`.
   - `@sw_update`.
   - Rescue strategy for stale chips and historical conversations.

4. Added studio-role architecture:
   - Brief strategist, research scout, creative director, poster art director, storyboard director, cinematographer, production designer, prompt director, edit director, sound designer, review producer, finishing producer, change manager, tool integrator, and others.
   - Role dispatch, role labels, handoff/guardrail ideas, and quality gates.

5. Added tool layers:
   - Banana Pro image generation.
   - Seedance 2.0 video generation.
   - URL Relay for local media.
   - Storyboard Visual Word.
   - Feishu Docs.
   - Kling API area.
   - Tool registry and prompt profiles.

6. Added aesthetic/reference layers:
   - Oscar Best Picture visual reference notes.
   - HQ aesthetic decision index.
   - Daily selected aesthetic index.
   - Obsidian Aesthetic Vault for local browsing without copying large media.

7. Added maintenance and portability:
   - `INSTALL_SW.md`.
   - `tools/sw_bootstrap.py`.
   - `tools/sw_sync_installed.py`.
   - `tools/sw_consistency_check.py`.
   - `tools/sw_doctor.py`.
   - Release checks and CI-style validation.

## Important Files To Inspect First

For a fresh continuation, inspect in this order:

1. `README.md`
2. `VERSION.md`
3. `SW_Runtime_Index.md`
4. `AGENTS.md`
5. `SW_V1.0.md`
6. `sw_update.md`
7. `sw_rescue.md`
8. `Architecture_Update_Log.md`
9. `Stage_Runbook.md`
10. `Cost_Governor.md`
11. `Studio_Skill_Dispatch_Protocol.md`
12. `Tool_Registry.md`
13. `Prompts/Tool_Official_Prompt_Deltas.md`
14. `tools/sw_consistency_check.py`
15. `tools/sw_sync_installed.py`

## Known Risks

- Version drift: project files, user-level skills, and plugin files can fall out of sync.
- Stale conversation behavior: older Codex chats may replay old fixed replies or old skill snapshots.
- Encoding issues on Windows: earlier project history includes mojibake concerns; preserve UTF-8 without BOM unless a specific file requires otherwise.
- Cost creep: the system has many roles and tools; startup must stay compact and only load detailed references when needed.
- Tool overreach: Banana/Seedance/Kling/Feishu/URL Relay must not bypass upstream planning, prompt-director handoff, or high-cost confirmation rules.
- Large local artifacts: aesthetic vaults, generated images, outputs, and tool payloads can bloat repo or accidentally become tracked.
- Secret handling: API keys and relay tokens must remain in local private config or environment variables, never tracked or printed.
- Poster typography: current rule favors image-native display typography for hero/visual text; exact small/legal text still needs editable or QA-controlled handling.
- Review loop: final review must hand must-fix feedback to change-manager as scoped delta, not trigger full rewrite by default.

## Open Decisions

- Whether to commit the current `V1.12.4` state and how to split commits/PRs.
- Whether untracked `feishu-docs/`, `kling-api/`, `Obsidian_Aesthetic_Vault/`, and `Prompts/Tool_Official_Prompt_Deltas.md` are intended to be tracked or partially ignored.
- Whether to publish this as a personal plugin, a GitHub repo, or keep it as local skills.
- Whether to run full consistency checks after handoff and before archive.
- Whether to prune or archive generated `outputs/` and local media indexes.
- Pending user decision: whether the Terracotta Warriors storyboard prompt structure should become a formal reusable template. Current leaning: keep it recorded as a high-quality historical-drama storyboard prompt baseline, but do not make it a default SW storyboard format yet. Key value: global visual/style baseline, conditional object locks, material/light/emotional-distance control, and per-shot deltas. Main risk: template bloat and slower normal storyboard runs if over-standardized.

## Suggested Next Steps

1. Inspect `git status` and group changed files into: runtime architecture, tool integrations, generated artifacts, local-only assets.
2. Run the SW consistency check if appropriate:
   ```powershell
   python tools\sw_consistency_check.py
   ```
3. Verify user-level installed skills and plugin sync:
   ```powershell
   python tools\sw_sync_installed.py
   ```
4. Decide what belongs in git versus local-only ignore rules.
5. Update `Architecture_Update_Log.md` and `VERSION.md` if any architecture file changes.
6. If publishing, run release checks and prepare a clean commit/PR.
7. After the project is safely committed or handed off, this old Codex conversation can be archived.

## Do Not Touch Without Explicit Instruction

- Do not reset or revert the dirty worktree.
- Do not delete local generated assets, aesthetic vault files, API configs, or tool outputs without a backup and explicit scope.
- Do not print or commit secrets.
- Do not change stable invocation name `SW_V1.0`.
- Do not collapse startup into a huge always-load rule file; preserve hot paths and progressive disclosure.
- Do not convert every project into file-heavy output by default; the user prefers chat-first execution unless files are useful.

## Handoff Status

This handoff captures the full SW design-studio system project, not just the last task. It should be safe to start a fresh Codex conversation from this file, inspect the repository, then continue architecture maintenance, release cleanup, or new tool integration.
