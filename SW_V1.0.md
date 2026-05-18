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
SW loaded successfully. Current version: V1.5.4
```

If the user only invokes SW, stop after the required reply and wait for the project request.

If the same user message includes a project request, put the required reply first, then continue using the hot path: `SW_Runtime_Index.md`, `Cost_Governor.md`, and only the selected role skills. Read `AGENTS.md` only when full project rules are needed or files conflict.

If the current project folder contains `.sw/PROJECT.md`, `.sw/RULES.md`, or `.sw/MEMORY.md`, read only the relevant local project memory files before producing project work.

If the same request asks for upstream design work and Banana Pro output, do not jump straight to generation. Produce the responsible Studio role handoff first, convert it through `prompt-director`, then use `banana-pro` only for the selected image/frame.

If the same request enables Historical Accuracy, default scope is the current request/visual chain only. Project-level scope requires explicit wording such as `本项目开启历史检查` or `全程开启历史检查`, and closes with `关闭历史检查`, `不用历史检查`, or `恢复普通模式`.

## Version Sync Is Separate

Do not use this file as the version-sync entry.

For synchronization in historical conversations or other project folders, use:

```text
@sw_update
```

Expected sync reply:

```text
SW version synchronized. Current version: V1.5.4
```

## Minimum Project Folder Package

Every project folder that wants local `@` entries should include both:

- `SW_V1.0.md` for startup
- `sw_update.md` for version synchronization

Recommended:

- `SW_Runtime_Index.md` for low-cost, encoding-safe startup behavior
- `Agent_Skill_Tech_Principles.md` for researched agent/skill handoff, guardrail, and eval rules
- `Studio_Role_Label_Protocol.md` for English-only role traces
- `Production_Pipeline_Map.md` for poster, presentation/deck, video, and film pipeline routing
- `Project_Memory_Rules.md` and `Project_Memory_Templates/.sw/` for long-running project memory

If a project folder has only `SW_V1.0.md`, it may show only the startup entry and not the update entry.
