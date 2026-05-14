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
SW loaded successfully. Current version: V1.2.4
```

If the user only invokes SW, stop after the required reply and wait for the project request.

If the same user message includes a project request, put the required reply first, then continue using `SW_Runtime_Index.md` and `AGENTS.md`.

## Version Sync Is Separate

Do not use this file as the version-sync entry.

For synchronization in historical conversations or other project folders, use:

```text
@sw_update
```

Expected sync reply:

```text
SW version synchronized. Current version: V1.2.4
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

If a project folder has only `SW_V1.0.md`, it may show only the startup entry and not the update entry.

