# Cost Governor

This file controls how SW spends attention, context, and generation effort.

## Core Rule

Every project turn must pass a cost gate before producing the deliverable.

The cost gate decides:

- which roles to read
- whether a small local `.sw/` project memory file is relevant
- how many questions to ask
- how much output to generate
- whether high-cost prompt/script/variant work is allowed
- whether to stop for confirmation

## Cost Lanes

| Lane | Trigger | Role Reads | Output Size | Questions | Allowed Work |
| --- | --- | --- | --- | --- | --- |
| Sync | `@sw_update`, `SW_UPDATE`, `/sw_update`, `SW_REFRESH` | `sw-update` only | one line | 0 | version sync only |
| Rescue | `/sw-rescue`, `@sw_rescue`, `SW_RESCUE`, `SW_REPAIR`, `SW_FORCE_UPDATE` | `sw-rescue` only | one line | 0 | stale-chip rescue only |
| Activation | `/SW_V1.0`, `@SW_V1.0` with no request | `sw-v1-0` only | one line | 0 | load only |
| Intake | new or unclear request | orchestrator + brief | short | 3 default, 5 max | brief, assumptions, next role |
| Direction | brief is usable | primary + support | medium | 3 default | up to 3 directions, recommendation |
| Production | task and direction are clear | primary + support | medium | 3 default, 5 max | one role deliverable |
| High-cost | detailed prompts, long scripts, full long decks, batch slide rewrites, batch variants, AI asset generation | selected roles after confirmation | controlled | 0-3 | one confirmed version/batch |
| Review/change | final review or feedback | primary first | short | 0-3, 5 if blocked | risks, S/M/L/XL, scoped fix |
| Finishing | export/package handoff | finishing + review if needed | short | 0-3 | file/package checklist |
| Memory | major durable confirmation or explicit "remember/save" request | project memory file only | one line or 1-3 bullets | 0 | suggest or append concise local memory |
| Feature help | `@sw_help`, `/sw_help`, `/sw-help`, feature trigger questions | embedded `sw-help` answer first; `Feature_Trigger_Index.md` only for details/debug | short | 0 | feature list only |
| Historical reminder | clear historical accuracy risk but not confirmed | `Feature_Trigger_Index.md` only | one line added to current route | 0-1 | ask whether to enable, do not load historical role |
| Maintenance-lite | maintain, optimize, quick check, sync confidence | version strings, selected skill validation, plugin JSON, secret scan | short | 0 | find obvious breakage only |
| Maintenance-full | publish/upload, deep regression, release audit, unexplained failure | regression suite plus affected files | medium | 0-2 | broad validation after lite path |

## Question Budget

- Default: ask 3 useful questions.
- Ask up to 5 for complex campaign, film, tool integration, blocked delivery, or unclear production constraints.
- Ask at most 1 in low-token mode, speed mode, or "you decide" mode.
- Ask 0 when the next step is obvious and safe.
- Questions must prepare the next role or unblock production.

## Role Budget

- Default to one primary role plus up to one support role.
- Use up to three roles only for complex campaign/film turns.
- Never read all studio skills by default.
- Prompt-only requests go directly to `prompt-director`.
- Explicit 香蕉 / banana / Banana Pro / Nano Banana / OpenRouter image-generation requests can add `banana-pro` as the image-generation member after `prompt-director`; use `tool-integrator` only when capability, parameters, API, or connection state is unclear. Do not load it for generic image prompts.
- Banana Pro is a post-prompt execution step, not a shortcut around Studio roles. If the request also asks for storyboard, video/film shot design, poster design, PPT/deck/slide layout, character/product/prop design, or scene planning, the responsible Studio role must produce the upstream handoff before `prompt-director` and `banana-pro`.
- `banana-pro` is a tool skill, not a Studio role. It does not count as an extra Studio support role, but generation still uses the high-cost gate when quota, uploads, or final-use assets are involved.
- Explicit 即梦2.0生成 / 即梦生成 / Seedance 2.0 / Ark Seedance video-generation requests can add `seedance-2-video` after `prompt-director`; use `tool-integrator` only when capability, parameters, API, key state, or connection state is unclear. Do not load it for generic video prompts or storyboard work.
- Seedance is a post-prompt execution step, not a shortcut around Studio roles. If the request also asks for script, storyboard, camera, edit, motion, sound, color, scene design, or film treatment, the responsible Studio role must produce the upstream handoff before `prompt-director` and `seedance-2-video`.
- `seedance-2-video` is a tool skill, not a Studio role. It does not count as an extra Studio support role, but real video generation still uses the high-cost gate when quota, public image URLs, long polling, or final-use assets are involved.
- `url-relay` is a tool skill, not a Studio role. It may be loaded before `seedance-2-video` when local media needs a public URL. Relay upload is not model-token cost, but it can expose files publicly and use server bandwidth, so apply the upload/privacy guardrail before private or client assets.
- If URL Relay fails or the SW uploader is unavailable, do not submit high-cost video generation until the media URL is resolved. First report that the SW uploader is unavailable; then use an already-public user URL or a confirmed/configured Litterbox/Catbox fallback only for unreachable/server-side relay failures. Missing token/address or permission errors must stop for config repair. Without a valid path, keep the prompt/payload.
- Presentation/deck structure requests go to `presentation-designer` first; full long decks or batch slide rewrites require the high-cost gate.
- Proposal decks can load `presentation-designer` references only when the request mentions client-facing, government, local tourism, city image film, video production proposal, visual QA, or similar specialized needs.

## Routing Read Budget

- Fast Path: `SW_Runtime_Index.md` + `Cost_Governor.md` + `Studio_Role_Label_Protocol.md` + `Studio_Skill_Dispatch_Protocol.md` + selected role skill.
- Add `Auto_Assignment_Rules.md` only when the route is unclear, a shortcut command needs interpretation, or user feedback changes the stage.
- Add `Production_Pipeline_Map.md` only for multi-stage handoff, full pipeline explanation, campaign/film complexity, or SOP output.
- Add `Studio_Skill_Map.md` only when role boundaries conflict.
- Add role `references/` only when the selected role's `SKILL.md` names a matching reference condition.
- Add `Prompts/Image_Aesthetic_Prompt_Reference.md` only for visual taste, anti-AI look, or filmic image prompt refinement.
- Add `Prompts/Video_Motion_Edit_Prompt_Rules.md` only for one-take, bullet-time, hero-shot, complex movement, edit-technique, or execution-level AI video prompts.
- Add `01_Research/Oscar_Best_Picture_Visual_Reference.md` only when the user asks for Oscar/classic film visual references.

## Comfortable-Use Rules

- Activation-only and sync-only turns stop after the fixed English reply.
- If the request is actionable, proceed with assumptions instead of a setup questionnaire.
- If the user says "continue", produce the next smallest useful deliverable.
- If the user says "you decide", choose a safe industry default and state only important assumptions.
- If feedback arrives, classify the change before rewriting.
- Keep one visible role/cost trace per project reply.
- End each role output with concise recommendation and next role.
- After major durable confirmations, use at most one short memory suggestion line. Do not add it for minor edits, temporary ideas, or rejected directions.
- Historical accuracy scan is low-cost and current-message only. It may add a one-line reminder to the normal route, but it must not load `historical-consultant`, research, browse, or expand until the user confirms.

## Hot Start Gate

- `@sw_help` and the SW Help UI button default answer must come from the embedded short help. Do not use shell/file reads for normal help. Read `Feature_Trigger_Index.md` only when the user asks for detailed trigger words, a specific feature's full rules, troubleshooting, or a help-system audit.
- Activation-only and sync-only turns must stop after the fixed English line. Do not read project files, role maps, or logs unless the same user message contains project work or a diagnostic request.
- Keep startup and sync separate: do not let `sw-v1-0` handle `@sw_update`; route sync aliases to `sw-update` only.
- For SW maintenance, run lite checks first. Escalate to full regression only when lite checks fail, the user asks to upload/publish, or the request says full/deep/regression.
- Do not validate every Studio skill on every small wording patch unless the patch touches role dispatch, skill frontmatter, or plugin packaging.

## High-Cost Gate

High-cost work requires enough locked inputs:

- goal
- platform or use case
- size, aspect ratio, or duration
- audience
- direction or style
- required information/assets
- brand/copyright/platform constraints
- output format or tool

For presentations, also lock the use setting, slide count range, source material, and whether speaker notes are needed before generating a full deck or batch slide rewrite.

For client-facing proposal decks, also lock or assume the client decision outcome before generating full page copy.

If these are not locked, output a low-cost preflight instead of the high-cost result.

Use this line before high-cost work:

```text
Cost gate: high-cost output needs confirmation. I will generate one confirmed version first, not a batch.
```

## Guardrail Gate

Pause and ask for confirmation before:

- external publishing or sending
- privacy-sensitive uploads
- irreversible tool actions
- final-use AI output involving brand, face, product, logo, copyright, or exact text risk
- Banana Pro / banana / OpenRouter image generation that may consume quota, requires `OPENROUTER_API_KEY`, or uploads reference images
- Seedance / 即梦2.0 video generation that may consume quota, requires `ARK_API_KEY` or a local key file, uses public image URLs, or triggers long polling
- unknown tool-specific prompt conversion
- any action that consumes quota without a clear preview

Explicit generation wording such as "use banana to generate one draft" or "use 即梦2.0生成一条草稿" counts as confirmation for one draft asset only. It does not confirm batch generation, private reference uploads, 1080p/final delivery, long unattended polling, or final-use brand/face/product output.

If blocked, produce a preview, risk note, or one-question confirmation instead of executing.

## Project Memory Gate

Project memory is optional and low-token:

- If `.sw/MEMORY.md`, `.sw/RULES.md`, or `.sw/PROJECT.md` exists, read only relevant local files.
- Suggest writing only durable confirmations such as brand tone, locked direction, audience, channel, continuity, asset rules, or client review constraints.
- Suggested wording must stay short: `记忆建议：可写入 MEMORY.md：品牌调性=克制电影感。回复“记住”即可。`
- Write only when the user explicitly says to remember/save/write it.
- Never store API keys, passwords, private contacts, or sensitive asset paths unless the user explicitly asks and confirms the memory is private.

## Historical Accuracy Gate

Default behavior is low false-positive:

- Do not trigger for style-only words: 国风, 古风, 唐风, 宋韵, 东方美学, 敦煌感, 新中式, 仙侠感.
- If clear historical accuracy risk is detected, add this one line: `检测到历史准确性风险。是否开启历史准确性检查？默认不开启。`
- If the project request is otherwise actionable, continue the normal low-cost route with historical checking off by default.
- Load `historical-consultant` only after explicit user confirmation.
- Default enable scope is current request/current visual-output chain only.
- `本项目开启历史检查` or `全程开启历史检查` keeps it on for the current conversation/project until the user says `关闭历史检查`, `不用历史检查`, or `恢复普通模式`.
- Long-term project persistence requires explicit memory approval; do not write a historical rule to `.sw/MEMORY.md` automatically.
- Historical checking is a visual-output gate. When enabled, it applies to poster key visuals, storyboard first frames, Banana outputs, Seedance representative frames/stills when available, reference-image QA, and final still-image review.
- Seedance integration allows video-output visual review when the user provides generated output or representative frames. Do not pretend full automated video QA exists beyond visible frames/stills/assets.

## Stop Rules

Stop instead of expanding when:

- the user only invoked SW
- the user only invoked `@sw_update`
- high-cost output is not confirmed
- brand/legal/platform facts block delivery judgment
- a revision is L or XL and invalidates the current direction

## Self-Check Before Reply

Before replying, internally check:

- Did I read `SW_Runtime_Index.md` and the selected role skill files?
- Did the trace use `Studio_Role_Label_Protocol.md`?
- Did I keep role count within budget?
- Did I keep output inside the cost lane?
- Did I pause for guardrails or human review when needed?
- Did I ask useful questions without slowing the user down?
- Did I preserve confirmed decisions?
- Did I avoid claiming a role was loaded if it was not available?
