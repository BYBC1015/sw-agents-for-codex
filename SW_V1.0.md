# SW_V1.0 Activation

This is the stable project-start entry for the SW design studio workflow.

## Use For

- explicitly starting a new SW design-studio project after the user invokes `/sw`, `/SW_V1.0`, `@SW_V1.0`, `调用 SW_V1.0`, or `启用 SW_V1.0`
- loading the design studio workflow in a new conversation only when the user asks for it
- keeping one stable project invocation name while runtime versions continue to update

Do not auto-activate from ordinary topic words such as poster, PPT, deck, storyboard, video prompt, image prompt, review, revision, or tool integration. Those requests use SW only after explicit activation in the same conversation.

## Invocation

```text
/sw
```

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

After text activation succeeds, reply exactly:

```text
SW loaded successfully. Current version: V1.13.1
```

If the user only invokes SW, stop after the required reply and wait for the project request.

If the same user message includes a normal project request after the activation phrase, put the required reply first, then continue using the hot path: `SW_Runtime_Index.md`, `Cost_Governor.md`, and only the selected role skills. Read `AGENTS.md` only when full project rules are needed or files conflict.

## Direct Quick-Edit Exception

If the user explicitly selects/invokes the SW skill entry and gives an actionable small edit for an existing poster/image, treat that explicit selection as the load acknowledgement. A chip merely appearing in the host UI is not enough. Do not add a separate activation narration, do not search the filesystem for runtime files, and do not reopen the full Brief/Direction pipeline.

Use this embedded quick route:

1. Identify the edit target and affected layer.
2. If the request is clear, execute the smallest visual edit pass immediately.
3. Preserve or regenerate display lettering as image-native visual typography unless the user asks for editable text layers.
4. Do not add plain system-font overlays to poster hero titles, launch titles, or large numerals by default.
5. Keep exact information text controlled and QA'd.
6. Reply with the edited output/preview first, then one short QA note if needed.

Examples that use this exception: existing poster text-size adjustment, title hierarchy correction, export a vertical version, remove a small artifact, make the title treatment closer to the provided reference, or "the text is too plain".

Only read runtime files for this route when the edit is ambiguous, the image tool fails, or the user asks for the underlying SW process.

## Installed Runtime Pack

When this file is installed as a Codex skill, the sync script may copy a portable runtime pack next to `SKILL.md`: `VERSION.md`, `SW_Runtime_Index.md`, `Cost_Governor.md`, `Studio_Role_Label_Protocol.md`, `Studio_Skill_Dispatch_Protocol.md`, and `Studio_Skills/`. Prefer those colocated files before searching other folders. If they are absent, use the embedded quick rules above for simple poster/image edits rather than spending a turn searching for them.

## Stale Snapshot Guard

If an old conversation, compacted history, prior screenshot, or earlier tool output contains a different SW version, ignore that historical value. The current `VERSION.md`, this file, and the current `sw-v1-0/SKILL.md` win. Do not output any older cached activation/sync reply from history.

## Old Conversation Self-Heal

If this activation happens inside an old conversation, upgrade in place: read the current `VERSION.md`, `SW_Runtime_Index.md`, and current loader/sync skill files when there is a version conflict, then use the current fixed reply. If old startup/update chips keep replaying sealed snapshots, use `@sw_rescue` or `/sw-rescue`. A new conversation is only a last fallback when the desktop app refuses to load the current files and rescue entry.

If the current project folder contains `.sw/PROJECT.md`, `.sw/RULES.md`, or `.sw/MEMORY.md`, read only the relevant local project memory files before producing project work.

If the project has local visual references in `.sw/ASSETS.md`, `.sw/RULES.md`, `.sw/MEMORY.md`, or the current user message, use them before the global aesthetic library. When visual style is missing, use `aesthetic-director` and `Aesthetic_Decision_Index.md` before expensive visual production.

For video, film, campaign story, product story, or storyboard requests, confirm or create a compact Project Asset Graph before storyboard when recurring characters, scenes, props, products, wardrobe, existing footage, or reference assets are not locked. Ask what already exists, what must be created, and what must stay unchanged; in fast mode, continue with marked assumptions.

If the same request asks for upstream design work and Banana Pro output, do not jump straight to generation. Produce the responsible Studio role handoff first, convert it through `prompt-director`, then use `banana-pro` only for the selected image/frame.

If the same request asks for upstream image/video work and Dreamina CLI / Jimeng CLI / official Jimeng CLI output, do not jump straight to generation. Produce the responsible Studio role handoff first, convert it through `prompt-director`, then use `dreamina-cli` only for the selected image/clip/task. Do not install the CLI, login, or run real generation without confirmation.

If the same request asks for upstream video/film work and Seedance/即梦 output, do not jump straight to generation. Produce the responsible Studio role handoff first, preserve any Project Asset Graph, convert it through `prompt-director`, then use `seedance-2-video` only for the selected clip/shot.

If Dreamina/Seedance/即梦 or another AI tool needs a public media URL and the user provides a local file, use `url-relay` before the downstream tool. Do not submit real generation until the relay upload succeeds.

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
SW version synchronized. Current version: V1.13.1
```

If normal sync still returns a stale sealed chip, use the standalone rescue entry:

```text
/sw-rescue
```

Expected rescue reply:

```text
SW rescue synchronized. Current version: V1.13.1
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
- `01_Research/HQ_Aesthetic_References/Aesthetic_Decision_Index.md` for low-cost visual-taste selection when the look is not locked
- `Project_Memory_Rules.md` and `Project_Memory_Templates/.sw/` for long-running project memory

If a project folder has only `SW_V1.0.md`, it may show only the startup entry and not the update entry.
