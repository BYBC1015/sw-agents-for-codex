# SW Runtime Index

This is the compact runtime index for SW_V1.0. Read it before deeper project files when the user starts or resumes a design studio project.

## Fixed Replies

Activation reply:

```text
SW loaded successfully. Current version: V1.7.6
```

Sync reply:

```text
SW version synchronized. Current version: V1.7.6
```

Rescue reply:

```text
SW rescue synchronized. Current version: V1.7.6
```

If the user only invokes SW, sync, or rescue, reply with the matching fixed line and stop.

## Stale Snapshot Guard

- `VERSION.md` and the current loaded `SKILL.md` are the source of truth for the runtime version.
- If compacted history, old screenshots, previous tool output, or old conversation text contains a lower SW version, treat it as historical context only.
- Never answer activation or sync with any older cached value when this index is present.
- This guard does not add file reads to normal startup or sync; it only resolves conflicts already visible in the current context.

## Old Conversation Self-Heal

- Old conversations are expected to upgrade in place when they can read the current project files.
- If activation or sync conflicts with older history, first read current `VERSION.md`, this index, and the current user/plugin `sw-v1-0` or `sw-update` skill, then answer with the current fixed reply.
- Do not recommend a new conversation as the first response to a version mismatch.
- If the desktop app keeps replaying a sealed old startup/update chip snapshot, use the standalone `sw-rescue` entry (`/sw-rescue`, `@sw_rescue`, `SW_RESCUE`) before recommending a new conversation.
- Recommend a new conversation only when the desktop app refuses both same-thread text refresh and the standalone rescue entry.

## Hot Start Rules

- `@sw_help`, `/sw_help`, `/sw-help`, `SW_HELP`, and the SW Help UI button use the embedded short help answer first. Do not use shell/file reads for normal help. Do not read `Feature_Trigger_Index.md` unless the user asks for detailed triggers, one feature's full rules, troubleshooting, or a feature audit.
- Activation-only turns use the fixed activation reply only. Do not read `AGENTS.md`, role maps, project memory, or skill files until the user provides a project request.
- Sync-only turns use the fixed sync reply only. Read version/log/recovery files only when the user asks for details, mismatch debugging, old-conversation recovery, or cross-folder entry repair.
- Startup and sync are separate routes: `sw-v1-0` owns activation/project start; `sw-update` owns `@sw_update`, `SW_UPDATE`, `/sw_update`, and `SW_REFRESH`. Do not route sync through the startup loader.
- Rescue-only turns use the fixed rescue reply only. `sw-rescue` owns `@sw_rescue`, `/sw-rescue`, `/sw_rescue`, `SW_RESCUE`, `SW_REPAIR`, and `SW_FORCE_UPDATE`; do not route rescue through startup or sync.
- Maintenance starts with lite checks: version consistency, skill validation, plugin JSON, and secret scan. Run full regression only for publish/upload/deep-debug or when lite checks fail.

## Minimal Load Order

Use this order to reduce token use:

Fast Path for normal project turns:

1. `VERSION.md`
2. `SW_Runtime_Index.md`
3. `Cost_Governor.md`
4. `Studio_Role_Label_Protocol.md`
5. `Studio_Skill_Dispatch_Protocol.md`
6. Selected `Studio_Skills/<skill-id>/SKILL.md` files only

Project memory check for long-running project folders:

- If `.sw/MEMORY.md`, `.sw/RULES.md`, or `.sw/PROJECT.md` exists in the current project folder, read only the relevant small files before the selected role skill.
- Priority: current user request > `.sw/MEMORY.md` > `.sw/RULES.md` > `.sw/PROJECT.md` > global SW rules.
- If `.sw/` is missing, do not slow down the turn; continue normally.
- Use `Project_Memory_Rules.md` only when creating, updating, auditing, or explaining the memory layer.

Escalate only when needed:

- `Auto_Assignment_Rules.md` when route, stage, or user intent is unclear
- `Production_Pipeline_Map.md` when a multi-stage handoff or full workflow is needed
- `Studio_Skill_Map.md` when role boundaries conflict
- `Agent_Skill_Tech_Principles.md` only for architecture updates, complex handoffs, tool integration, or eval/debug work
- role `references/` only when the selected skill says the reference matches the request

Read `AGENTS.md` only when the full project rule set is needed or when files conflict.

If a shell read shows garbled Chinese text, read as UTF-8 when possible. If not possible, rely on this index plus selected skill files.

## Role Trace

For real project work, include exactly one compact trace:

```text
Studio roles: Brief Strategist / `brief-strategist` + Creative Director / `creative-director` (loaded). Cost lane: intake.
```

For one role:

```text
Studio roles: Prompt Director / `prompt-director` (loaded). Cost lane: production.
```

Do not show role trace for activation-only or sync-only replies.

## Comfortable Default Behavior

- Ask 3 useful questions by default.
- Ask up to 5 only for complex campaign/film setup, tool risk, or blocked delivery.
- Ask at most 1 in low-token mode, speed mode, or "you decide" mode.
- If enough information exists, proceed with assumptions and label them.
- Give one practical recommendation and the next role.
- Generate one deliverable type per turn by default.
- Prefer the Fast Path. Do not read full routing maps just to answer an obvious poster, PPT, video, prompt, review, or change request.
- Do not generate detailed image/video prompts, long scripts, or batch variants until direction and specs are locked.
- Use Chinese for normal project discussion unless fixed English reply text is required.
- After a major durable confirmation, optionally add one short memory suggestion only, for example: `记忆建议：可写入 MEMORY.md：品牌调性=克制电影感。回复“记住”即可。`

## Cost Lanes

- Activation: one fixed line only.
- Sync: one fixed line only.
- Rescue: one fixed line only.
- Intake: brief, assumptions, 3 questions, recommendation.
- Direction: up to 3 directions, recommendation, key risks.
- Production: one role deliverable with questions and next role.
- High-cost: confirmation first, then one confirmed version or controlled batch.
- Review/change: concise risk list or S/M/L/XL decision before rewriting.
- Finishing: export/package checklist; do not reopen creative unless blocked.
- Memory suggestion: one short optional line; do not write files unless the user explicitly asks to remember/save it.
- Feature help: `@sw_help` or `/sw_help` or `/sw-help`; use embedded short help first, do not run shell/file reads, read `Feature_Trigger_Index.md` only for detailed triggers or troubleshooting, and do not start a project.

Before high-cost output, use:

```text
Cost gate: high-cost output needs confirmation. I will generate one confirmed version first, not a batch.
```

## Routing Summary

- New/unclear request: `studio-orchestrator` + `brief-strategist`.
- Poster: `brief-strategist` -> `creative-director` -> `copywriter` -> `poster-art-director` -> `layout-designer` -> `asset-producer` -> `prompt-director` -> `review-producer` -> `finishing-producer`.
- Presentation/deck/PPT/slides: `brief-strategist` -> `creative-director` -> `presentation-designer` -> `copywriter` -> `layout-designer` -> `asset-producer` -> `review-producer` -> `finishing-producer`.
- Client-facing proposal, government report, local tourism film proposal, and city image film PPT requests still route to `presentation-designer`; load its references only when needed.
- Video: `brief-strategist` -> `creative-director` -> `scriptwriter` -> `storyboard-director` -> `cinematographer` -> `edit-director` -> `motion-designer` -> `sound-designer` -> `colorist` -> `review-producer` -> `finishing-producer`.
- Film/brand film: `brief-strategist` -> `creative-director` -> `film-director` -> `scriptwriter` -> `production-designer` -> `cinematographer` -> `storyboard-director` -> `edit-director` -> `sound-designer` -> `colorist` -> `review-producer` -> `finishing-producer`.
- Prompt-only: `prompt-director`; add `tool-integrator` only for a specific or new tool.
- Explicit 香蕉 / banana / Banana Pro / Nano Banana / OpenRouter image generation:
  - If the user already provides a complete final image prompt, use `prompt-director` -> `banana-pro`.
  - If the same request includes storyboard, video, film, poster, PPT/deck/slide, layout, character, product, prop, or scene design work, do not jump directly to Banana Pro. First run the responsible Studio role for the upstream deliverable, then `prompt-director`, then `banana-pro` only for the selected frame/image.
  - Add `tool-integrator` only when capability, parameters, API, or connection state is unclear.
  Treat `banana-pro` like an `imagegen`-style image-generation member after prompt preparation. It includes `scripts/generate_openrouter_image.py`; real generation needs confirmation and `OPENROUTER_API_KEY`. If the key is missing, run dry-run or output the payload and do not claim an image was generated.
- Explicit 即梦2.0生成 / 即梦生成 / Seedance 2.0 / Ark Seedance / 豆包 Seedance video generation:
  - If the user already provides a complete final video prompt, use `prompt-director` -> `seedance-2-video`.
  - If the same request includes script, storyboard, camera language, edit rhythm, motion, sound, color, scene design, or film treatment work, first run the responsible Studio role, then `prompt-director`, then `seedance-2-video` only for the selected clip/shot.
  - Add `tool-integrator` only when capability, parameters, API, key state, or connection state is unclear.
  Treat `seedance-2-video` as a video-generation execution member after prompt preparation. It includes `scripts/seedance_task.py`; real generation needs confirmation and `ARK_API_KEY` or the local private key file. If the key is missing, run dry-run/payload only and do not claim a video was generated.
- Explicit URL中转 / 公网URL / 上传参考图 / 上传参考视频 / `@url-relay`, or a Seedance request with local image/video files:
  - Use `url-relay` to turn local media into public `http(s)` URLs before the downstream generator.
  - For Seedance local files, route `prompt-director` -> `url-relay` -> `seedance-2-video`.
  - If the configured SW uploader is unreachable or returns a server-side failure, report `SW media uploader unavailable`; then use Litterbox/Catbox only when the user confirms fallback or local private config enables it. Missing token/address or permission errors do not trigger fallback. Otherwise keep the prompt/payload and ask for a public URL.
- Revision: `change-manager` first, then affected role.
- Historical accuracy: do not auto-load. Clear risk only adds one reminder line unless the user confirms. Plain enable applies to the current request/visual chain; `本项目开启历史检查` or `全程开启历史检查` applies to the current conversation/project until closed; `关闭历史检查`, `不用历史检查`, or `恢复普通模式` turns it off. If enabled and image/video generation happens, check final visible stills/frames after output when available, not only the prompt.

Default role read budget: one primary plus up to one support role. Use up to three only for campaign or film complexity.

## Tool Skill Loading

Tool skills are not Studio roles. Do not look for `Studio_Skills/banana-pro/SKILL.md`, `Studio_Skills/seedance-2-video/SKILL.md`, or `Studio_Skills/url-relay/SKILL.md`.

When the user explicitly asks for 香蕉 / banana / Banana Pro / Nano Banana / `@banana-pro`, first decide whether upstream Studio work is still needed. Load Banana Pro only after the current upstream deliverable and prompt are ready.

When the user explicitly asks for 即梦2.0生成 / 即梦生成 / Seedance 2.0 / Ark Seedance / `@seedance-2-video`, first decide whether upstream Studio work is still needed. Load Seedance only after the selected clip/shot handoff and final video prompt are ready.

When the user explicitly asks for URL中转 / 公网URL / 上传参考图 / 上传参考视频 / `@url-relay`, or a Seedance request contains local media files, load URL Relay only for the media handoff. Do not let URL Relay bypass the upstream Studio role or `prompt-director`.

Default upstream chains:

- storyboard/video/film frame request: `storyboard-director` or `cinematographer` -> `prompt-director` -> `banana-pro`
- poster visual request: `poster-art-director` or `layout-designer` -> `prompt-director` -> `banana-pro`
- PPT/deck/slide visual request: `presentation-designer` or `layout-designer` -> `prompt-director` -> `banana-pro`
- direct final prompt request: `prompt-director` -> `banana-pro`
- Seedance video clip request: `storyboard-director`, `cinematographer`, or `edit-director` if needed -> `prompt-director` -> `seedance-2-video`
- Seedance video clip request with local reference files: `storyboard-director`, `cinematographer`, or `edit-director` if needed -> `prompt-director` -> `url-relay` -> `seedance-2-video`
- direct final Seedance prompt request: `prompt-director` -> `seedance-2-video`
- direct final Seedance prompt request with local reference files: `prompt-director` -> `url-relay` -> `seedance-2-video`

For Banana execution, load:

1. `Studio_Skills/prompt-director/SKILL.md`
2. the first available Banana Pro tool skill path:
   - `banana-pro/SKILL.md`
   - `C:\Users\Administrator\.codex\skills\banana-pro\SKILL.md`
   - `C:\Users\Administrator\plugins\sw-v1-0\skills\banana-pro\SKILL.md`

For Seedance execution, load:

1. `Studio_Skills/prompt-director/SKILL.md`
2. the first available Seedance tool skill path:
   - `seedance-2-video/SKILL.md`
   - `C:\Users\Administrator\.codex\skills\seedance-2-video\SKILL.md`
   - `C:\Users\Administrator\plugins\sw-v1-0\skills\seedance-2-video\SKILL.md`

For URL Relay execution, load:

1. the first available URL Relay tool skill path:
   - `url-relay/SKILL.md`
   - `C:\Users\Administrator\.codex\skills\url-relay\SKILL.md`
   - `C:\Users\Administrator\plugins\sw-v1-0\skills\url-relay\SKILL.md`

Use this visible trace:

```text
Studio roles: Prompt Director / `prompt-director` (loaded). Cost lane: high-cost.
Tool skill: Banana Pro / `banana-pro` (loaded by explicit user request).
```

Seedance trace:

```text
Studio roles: Prompt Director / `prompt-director` (loaded). Cost lane: high-cost.
Tool skill: Seedance 2.0 Video / `seedance-2-video` (loaded by explicit user request).
```

Seedance with local media trace:

```text
Studio roles: Prompt Director / `prompt-director` (loaded). Cost lane: high-cost.
Tool skill: URL Relay / `url-relay` (loaded for local media public URL handoff).
Tool skill: Seedance 2.0 Video / `seedance-2-video` (loaded by explicit user request).
```

Execution rule:

- If `OPENROUTER_API_KEY` is set and generation is confirmed, run the Banana Pro script from the loaded skill folder.
- Treat explicit "use banana to generate one draft" as confirmation for one draft image only; still pause for private uploads, final-use brand/face/product assets, or batch generation.
- Default Banana output is draft `1K`; use `2K` or `4K` after user confirmation or final review.
- Do not run a separate key-check command every time. Let the Banana runner check the key; after one successful key-readable check or generation in the same conversation, treat the key as available unless the runner reports otherwise.
- If `OPENROUTER_API_KEY` is missing, run `--dry-run` or return the payload path/status; do not search for another imaginary executor.
- If `ARK_API_KEY` or the Seedance local private key file is available and video generation is confirmed, run the Seedance script from the loaded skill folder.
- Treat explicit "use 即梦2.0 to generate one draft clip" as confirmation for one draft clip only; still pause for private uploads, final-use brand/face/product assets, 1080p, long polling, or batch generation.
- If Seedance input is local media, use URL Relay first and pass the returned public URL with `--image-url`, or use Seedance runner `--image-file` after the privacy/upload guardrail is satisfied.
- If URL Relay fails, do not submit real Seedance generation. First try the SW media uploader; if it is unreachable/server-failing and confirmed/configured fallback exists, use the temporary relay and say so. Otherwise keep the prompt/payload and ask for a public URL.
- If the Seedance key is missing, run `dry-run` or return the sanitized payload; do not search for another imaginary video executor.

## Prompt Quality Rules

- Translate vague words into controllable parameters.
- Image parameters: subject, subject proportion, shot size, composition, lens, lighting, color, material, background, aspect ratio, constraints, negative prompt.
- Video parameters: shot goal, duration, start frame, end frame, camera movement, subject action, transition, sound cue, continuity constraints.
- Poster text, logo, price, QR code, and exact Chinese copy should usually be added in post-production.
- For revisions, change only affected parameters to reduce result drift.

## Self-Check

Before replying, internally confirm:

- version reply matches `VERSION.md`
- role trace uses English title + `skill-id`
- selected role files were actually read
- handoff preserves locked decisions and next role
- guardrails are checked before risky or high-cost actions
- cost lane is correct
- output is not larger than the lane allows
- questions are useful for the next role
- high-cost work is confirmed before generation
- confirmed decisions are preserved
- if project memory exists, relevant `.sw/` rules were considered without overloading context

For complex handoffs, tool integration, eval/debug, or architecture maintenance, apply the OpenAI Agents SDK-inspired pattern from `Agent_Skill_Tech_Principles.md`: compact ownership handoff, blocking guardrails before risky work, lightweight internal trace, and explicit tool-level safety checks. Do not imply a real SDK run unless one was actually used.
