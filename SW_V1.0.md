# SW_V1.0 Activation

This is the stable project-start entry for the SW design studio workflow.

## Use For

- starting a new poster, presentation/PPT/deck, video, storyboard, edit-plan, prompt, review, revision, or tool-integration project
- loading the design studio workflow in a new conversation
- keeping one stable project invocation name while runtime versions continue to update

## Invocation

```text
/SW_V1.0
```

```text
@SW_V1.0
```

Text fallbacks:

```text
/sw_v1.0
/sw-v1-0
@sw-v1-0
call SW_V1.0
activate SW_V1.0
```

## Required Reply

After activation succeeds, reply exactly:

```text
SW loaded successfully. Current version: V1.9.1
```

If the user only invokes SW, stop after the required reply and wait for the project request.

If the same user message includes a project request, put the required reply first, then continue using the hot path: `SW_Runtime_Index.md`, `Cost_Governor.md`, and only the selected role skills. Read `AGENTS.md` only when full project rules are needed or files conflict.

## Stale Snapshot Guard

If an old conversation, compacted history, prior screenshot, or earlier tool output contains a different SW version, ignore that historical value. The current `VERSION.md`, this file, and the current `sw-v1-0/SKILL.md` win. Do not output any older cached activation/sync reply from history.

## Old Conversation Self-Heal

If this activation happens inside an old conversation, upgrade in place: read the current `VERSION.md`, `SW_Runtime_Index.md`, and current loader/sync skill files when there is a version conflict, then use the current fixed reply. If old startup/update chips keep replaying sealed snapshots, use `@sw_rescue` or `/sw-rescue`. A new conversation is only a last fallback when the desktop app refuses to load the current files and rescue entry.

If the current project folder contains `.sw/PROJECT.md`, `.sw/RULES.md`, or `.sw/MEMORY.md`, read only the relevant local project memory files before producing project work.

If the same request asks for upstream design work and Banana Pro output, do not jump straight to generation. Produce the responsible Studio role handoff first, convert it through `prompt-director`, then use `banana-pro` only for the selected image/frame.

If the same request asks for upstream video/film work and Seedance/即梦 output, do not jump straight to generation. Produce the responsible Studio role handoff first, convert it through `prompt-director`, then use `seedance-2-video` only for the selected clip/shot.

If Seedance/即梦 or another AI tool needs a public media URL and the user provides a local file, use `url-relay` before the downstream tool. Do not submit real generation until the relay upload succeeds.

If the same request asks for a visual方案文件, 视觉导演方案, Word视觉方案, DOCX视觉方案, or 分镜视觉方案文件, treat it as a downstream handoff. Do not let `storyboard-visual-word` replace storyboard, scene design, image generation, or image selection. Package the DOCX only after selected visuals and concise scene rationale exist.

If the same request enables Historical Accuracy, default scope is the current request/visual chain only. Project-level scope requires explicit wording such as `本项目开启历史检查` or `全程开启历史检查`, and closes with `关闭历史检查`, `不用历史检查`, or `恢复普通模式`.

## Version Sync Is Separate

Do not use this file as the version-sync entry.

For synchronization in historical conversations or other project folders, use:

```text
@sw_update
```

Expected sync reply:

```text
SW version synchronized. Current version: V1.9.1
```

If normal sync still returns a stale sealed chip, use the standalone rescue entry:

```text
/sw-rescue
```

Expected rescue reply:

```text
SW rescue synchronized. Current version: V1.9.1
```

## Minimum Project Folder Package

Every project folder that wants local `@` entries should include both:

- `SW_V1.0.md` for startup
- `sw_update.md` for version synchronization
- `sw_rescue.md` or `/sw-rescue` entry for stale-chip rescue when the host UI caches old startup/sync skills

Recommended:

- `SW_Runtime_Index.md` for low-cost, encoding-safe startup behavior
- `Agent_Skill_Tech_Principles.md` for researched agent/skill handoff, guardrail, and eval rules
- `Studio_Role_Label_Protocol.md` for English-only role traces
- `Production_Pipeline_Map.md` for poster, presentation/deck, video, and film pipeline routing
- `Project_Memory_Rules.md` and `Project_Memory_Templates/.sw/` for long-running project memory

If a project folder has only `SW_V1.0.md`, it may show only the startup entry and not the update entry.
