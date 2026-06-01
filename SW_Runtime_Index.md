# SW Runtime Index

This is the compact runtime index for SW_V1.0. Read it before deeper project files only after the user explicitly invokes SW or resumes an already activated SW design-studio project.

## Fixed Replies

Activation reply:

```text
SW loaded successfully. Current version: V1.12.12
```

Sync reply:

```text
SW version synchronized. Current version: V1.12.12
```

Rescue reply:

```text
SW rescue synchronized. Current version: V1.12.12
```

If the user only invokes SW, sync, or rescue, reply with the matching fixed line and stop.

## Explicit Activation Gate

- Do not activate SW from ordinary topic words such as poster, PPT, deck, storyboard, video prompt, image prompt, review, or revision.
- Activate the full SW workflow only when the user explicitly inputs `/sw`, `/SW_V1.0`, `@SW_V1.0`, `调用 SW_V1.0`, `启用 SW_V1.0`, `拉取本项目架构`, or `按本项目架构执行`, or when the current conversation has already completed that activation.
- Standalone project-type aliases such as `/poster`, `/video`, `/ppt`, `/deck`, `/storyboard`, `/prompt-image`, `/prompt-video`, `/review`, `/change`, and `/tool` do not start SW by themselves. Treat them as SW aliases only after explicit activation or when combined with an SW activation phrase in the same message.
- A skill chip merely appearing in the host UI is not activation. It counts only if the user explicitly selects/invokes the SW entry or the current thread is already activated.
- If SW is not activated, handle the user's request using normal Codex behavior and do not show `Studio roles:` traces.

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
- Host UI skill-chip visibility alone is not a load acknowledgement. Use the poster/image quick-edit lane only after explicit SW activation or explicit user selection of the SW entry.
- Sync-only turns use the fixed sync reply only. Read version/log/recovery files only when the user asks for details, mismatch debugging, old-conversation recovery, or cross-folder entry repair.
- Startup and sync are separate routes: `sw-v1-0` owns activation/project start; `sw-update` owns `@sw_update`, `SW_UPDATE`, `/sw_update`, and `SW_REFRESH`. Do not route sync through the startup loader.
- Rescue-only turns use the fixed rescue reply only. `sw-rescue` owns `@sw_rescue`, `/sw-rescue`, `/sw_rescue`, `SW_RESCUE`, `SW_REPAIR`, and `SW_FORCE_UPDATE`; do not route rescue through startup or sync.
- Maintenance starts with lite checks: version consistency, skill validation, plugin JSON, and secret scan. Run full regression only for publish/upload/deep-debug or when lite checks fail.

## Minimal Load Order

Use this order to reduce token use:

Fast Path for activated SW project turns:

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
- If `.sw/ASSETS.md`, `.sw/RULES.md`, `.sw/MEMORY.md`, or the current request includes visual references, prefer those project-local visual cues before the global aesthetic library.
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
- If the user has not specified visual style, use `aesthetic-director` with the compact `Aesthetic_Decision_Index.md`; do not load raw images by default.
- If the user explicitly asks for Obsidian aesthetic browsing, curation, or library maintenance, sync/open the Obsidian aesthetic vault. The vault embeds local preview images from existing contact sheets but does not copy heavy media; normal SW work still uses the compact aesthetic index only.
- Generate one deliverable type per turn by default.
- After the deliverable, optionally add at most one short reply-end nudge when it helps the user remember an existing SW capability. Prefer memory, locking, next-step, risk, or cost nudges. Skip it when there is nothing useful to add.
- For clear historical drama, cultural-heritage, archaeology, ancient craft, intangible-heritage, dynasty-specific artifact, or museum-narrative work, a reply-end nudge may offer historical accuracy checking or the Historical Drama Style Capsule in one line. Do not auto-load `historical-consultant` and do not auto-apply the capsule.
- Prefer the Fast Path after SW is activated. Do not read full routing maps just to answer an obvious activated poster, PPT, video, prompt, review, or change request.
- Do not generate detailed image/video prompts, long scripts, or batch variants until direction and specs are locked.
- Use Chinese for normal project discussion unless fixed English reply text is required.
- After a major durable confirmation, optionally add one short memory suggestion only, for example: `记忆建议：可写入 MEMORY.md：品牌调性=克制电影感。回复“记住”即可。`

## Cost Lanes

- Activation: one fixed line only.
- Sync: one fixed line only.
- Rescue: one fixed line only.
- Intake: brief, assumptions, 3 questions, recommendation.
- Direction: up to 3 directions, recommendation, key risks.
- Compare board: after direction options, storyboard groups, or deck structures when feedback/selection is fuzzy; output only `Keep`, `Remove`, and `Next version`.
- Selected asset packet: before a selected poster visual, deck page visual, storyboard shot, reference frame, local media item, public URL, or generated still is handed to `prompt-director`, URL Relay, Banana, Seedance, Kling, DOCX, or Feishu; output one compact selected-object packet and do not reopen the brief.
- Production: one role deliverable with questions and next role.
- High-cost: confirmation first, then one confirmed version or controlled batch.
- Review/change: concise risk list or S/M/L/XL decision before rewriting.
- Quick edit: existing poster/image, deck page/outline, storyboard group/shot, edit plan, or prompt receives one local output-first fix; route to change-manager first when the change is L/XL.
- Finishing: export/package checklist; do not reopen creative unless blocked.
- Memory suggestion: one short optional line; do not write files unless the user explicitly asks to remember/save it.
- Feature help: `@sw_help` or `/sw_help` or `/sw-help`; use embedded short help first, do not run shell/file reads, read `Feature_Trigger_Index.md` only for detailed triggers or troubleshooting, and do not start a project.

Before high-cost output, use:

```text
Cost gate: high-cost output needs confirmation. I will generate one confirmed version first, not a batch.
```

## Reply-End Nudge

For normal project work, put the requested deliverable first. After it, add at most one light nudge only when it is useful and directly tied to the current output.

Allowed nudge types:

- `记忆建议`: the project shows long-running signals or a durable decision should survive future conversations
- `锁定提醒`: a character, scene, visual style, reference role, aspect ratio, or selected asset should be locked before prompt/tool work
- `下一步建议`: one smallest next action would save time
- `风险提醒`: copyright, logo, exact text, privacy, platform, or tool-cost risk matters
- `成本提醒`: the next requested step would become high-cost

Rules:

- one nudge maximum; if several apply, choose the one that prevents the biggest likely mistake
- no nudge after activation-only, sync-only, rescue-only, or pure help replies
- do not add a nudge if it would slow the answer, repeat obvious text, or distract from the deliverable
- do not read extra files just to create a nudge
- never write memory from a nudge; wait for explicit `记住`, `写入 MEMORY`, or equivalent

## Routing Summary

- New/unclear activated SW request: `studio-orchestrator` + `brief-strategist`.
- Compare Board: after `creative-director` directions, `storyboard-director` storyboard groups, or `presentation-designer` deck structures, use a short comparison when the user needs to choose or feedback is abstract. Keep it to `Keep`, `Remove`, and `Next version`; do not create new directions unless asked.
- Poster quick edit / Quick edit: if the user already has a poster/image, deck page/outline, storyboard group/shot list, edit plan/timeline, or prompt and asks for a small local fix, skip the full pipeline. Ask at most one blocking question and output the revised object first. For poster work, default typography remains image-native: hero titles, launch titles, large numerals, and stylized display lettering should be preserved or regenerated by the image/visual model, not replaced with plain system fonts. For deck/storyboard/edit/prompt work, change only the selected page, section, shot, time span, or parameter. If feedback changes audience, main message, narrative structure, style, or deliverable form, route to `change-manager`.
- Selected Asset Packet: when an upstream role has chosen a concrete object for prompt writing, URL upload, image/video generation, or document publishing, package that object before handoff. Use it for selected poster key visuals, deck page visuals, storyboard shots/groups, reference angle frames, local media files, public URLs, generated images, or selected concept images. Skip it for direct prompt-only requests where the user already supplied the complete final prompt.
- Poster: `brief-strategist` -> `creative-director` -> `aesthetic-director` when look is not locked -> `copywriter` -> `poster-art-director` -> `layout-designer` -> `asset-producer` -> `prompt-director` -> `review-producer` -> `finishing-producer`.
- Presentation/deck/PPT/slides: `brief-strategist` -> `creative-director` -> `aesthetic-director` when deck look is not locked -> `presentation-designer` -> `copywriter` -> `layout-designer` -> `asset-producer` -> `review-producer` -> `finishing-producer`.
- Client-facing proposal, government report, local tourism film proposal, and city image film PPT requests still route to `presentation-designer`; load its references only when needed.
- Video: `brief-strategist` -> `creative-director` -> `aesthetic-director` when visual language is not locked -> `scriptwriter` -> `storyboard-director` -> `cinematographer` -> `edit-director` -> `motion-designer` -> `sound-designer` -> `colorist` -> `review-producer` -> `finishing-producer`.
- Film/brand film: `brief-strategist` -> `creative-director` -> `film-director` -> `aesthetic-director` when look/world grammar is not locked -> `scriptwriter` -> `production-designer` -> `cinematographer` -> `storyboard-director` -> `edit-director` -> `sound-designer` -> `colorist` -> `review-producer` -> `finishing-producer`.
- Aesthetic decision / moodboard selection / "SW decide the look": `aesthetic-director`; read `Aesthetic_Decision_Index.md` first, then only deeper reference indexes if asked.
- Obsidian审美库 / 整理审美库 / 筛选审美图片 / 打开审美资料库: run `tools/sync_obsidian_aesthetic_vault.py`; it targets the active Obsidian vault by default and embeds preview images for human browsing. Do not load it for ordinary project startup.
- Character setting sheet / role reference board: `production-designer` -> `asset-producer` if source/risk matters -> `prompt-director` if generating.
- Scene setting sheet / production-design board: `production-designer` -> `prompt-director` if generating.
- Integrated storyboard sheet / one-image storyboard board: `storyboard-director`; add `cinematographer` only when shot language or continuity is weak; then `prompt-director` if generating.
- Storyboard reference angle frame / 分镜特定角度参考图 / 用 image 或 banana 辅助分镜: `storyboard-director` selects one useful shot/angle -> `cinematographer` only if camera geometry matters -> `prompt-director` -> imagegen or `banana-pro` only for the selected reference still.
- Prompt-only: `prompt-director`; add `tool-integrator` only for a specific or new tool.
- Explicit 香蕉 / banana / Banana Pro / Nano Banana / OpenRouter image generation:
  - If the user already provides a complete final image prompt, use `prompt-director` -> `banana-pro`.
  - If the same request includes storyboard, video, film, poster, PPT/deck/slide, layout, character, product, prop, or scene design work, do not jump directly to Banana Pro. First run the responsible Studio role for the upstream deliverable, then `prompt-director`, then `banana-pro` only for the selected frame/image.
  - Add `tool-integrator` only when capability, parameters, API, or connection state is unclear.
  Treat `banana-pro` like an `imagegen`-style image-generation member after prompt preparation. It includes `scripts/generate_openrouter_image.py`; real generation needs confirmation and `OPENROUTER_API_KEY` from the environment or private `~/.config/banana-pro/openrouter.env`. If the key is missing, run dry-run or output the payload and do not claim an image was generated.
- Explicit 抠图 / 扣图 / 去底 / 去黑底 / 黑底转透明 / 透明底 PNG / `@black-background-cutout`:
  - If the user provides existing local image files, load `black-background-cutout` directly. It is a local pixel-processing tool for black/simple solid backgrounds, not AI generation and not a Studio role.
  - It creates fast transparent PNG previews and may leave slight fringing. Do not present it as finishing-grade, no-fringe, or a solution for AI lettering reuse. For complex photo cutouts or formal delivery, recommend professional cutout/refinement or regenerated transparent assets.
- Explicit 即梦2.0生成 / 即梦生成 / Seedance 2.0 / Ark Seedance / 豆包 Seedance video generation:
  - If the user already provides a complete final video prompt, use `prompt-director` -> `seedance-2-video`.
  - If the same request includes script, storyboard, camera language, edit rhythm, motion, sound, color, scene design, or film treatment work, first run the responsible Studio role, then `prompt-director`, then `seedance-2-video` only for the selected clip/shot.
  - Add `tool-integrator` only when capability, parameters, API, key state, or connection state is unclear.
  Treat `seedance-2-video` as a video-generation execution member after prompt preparation. It includes `scripts/seedance_task.py`; real generation needs confirmation and `ARK_API_KEY` or the local private key file. If the key is missing, run dry-run/payload only and do not claim a video was generated.
- Explicit URL中转 / 公网URL / 上传参考图 / 上传参考视频 / `@url-relay`, or a Seedance request with local image/video files:
  - Use `url-relay` to turn local media into public `http(s)` URLs before the downstream generator.
  - For Seedance local files, route `prompt-director` -> `url-relay` -> `seedance-2-video`.
  - If the configured SW uploader is unreachable or returns a server-side failure, report `SW media uploader unavailable`; then use Litterbox/Catbox only when the user confirms fallback or local private config enables it. Missing token/address or permission errors do not trigger fallback. Otherwise keep the prompt/payload and ask for a public URL.
- Explicit 视觉方案文件 / 视觉导演方案 / Word视觉方案 / DOCX视觉方案 / 分镜视觉方案文件 / `@storyboard-visual-word`:
  - If selected storyboard/scene/concept images and rationale already exist, use `finishing-producer` -> `storyboard-visual-word`.
  - If the request still needs storyboard, scene/character setting, image generation, or image selection, route upstream first, then package the selected visuals into DOCX.
  - Do not expose raw prompts, local paths, generation-result tables, or tool parameters in the formal Word unless the user asks for an internal production appendix.
- Explicit 转到飞书 / 同步到飞书 / 发布到飞书 / 飞书视觉方案 / 飞书分镜 / Lark Docs / `@feishu-docs`:
  - If a visual plan/storyboard Markdown or selected handoff already exists, use `finishing-producer` -> `feishu-docs`.
  - If the request still needs storyboard, scene/character setting, image generation, image selection, or DOCX/Markdown source creation, route upstream first.
  - Without Feishu credentials, render/dry-run only. Real publishing needs local private app config and explicit `--execute`; do not publish private assets or local paths without confirmation.
- Revision: `change-manager` first, then affected role. Midstream boss/client feedback, screen-recording notes, meeting notes, chat logs, screenshot annotations, and oral comments should become a compact `Change Delta Packet` before rewriting, preserving `Keep unchanged` and the smallest affected object.
- Historical accuracy: do not auto-load. Clear risk only adds one reminder line unless the user confirms. Plain enable applies to the current request/visual chain; `本项目开启历史检查` or `全程开启历史检查` applies to the current conversation/project until closed; `关闭历史检查`, `不用历史检查`, or `恢复普通模式` turns it off. If enabled and image/video generation happens, check final visible stills/frames after output when available, not only the prompt.
- Historical Drama Style Capsule: optional look baseline for historical drama, cultural-heritage, archaeology, ancient craft, intangible-heritage, and museum storytelling. It is not historical accuracy checking and does not require `historical-consultant`. Use only after user confirmation or when the look is already locked; keep it once as global `Visual Baseline`, then write per-scene/per-shot deltas.

Default role read budget: one primary plus up to one support role. Use up to three only for campaign or film complexity.

## Selected Asset Packet

Selected Asset Packet is a lightweight selected-object handoff, not a new stage. Use it only after a role has chosen one concrete poster/deck/storyboard/reference/media object and before `prompt-director`, URL Relay, Banana, Seedance, Kling, Storyboard Visual Word, or Feishu consumes it.

```text
Selected Asset Packet:
- Object ID:
- Source stage:
- Asset type:
- Purpose:
- Selected input:
- Reference roles:
- Locked items:
- Avoid:
- Next tool:
- Privacy/cost gate:
```

Rules:

- `Reference roles` must say what each reference does, such as character identity, product shape, scene layout, composition, color, texture, style, first frame, last frame, or edit source. Do not treat all references as global style.
- `Locked items` are preserved by `prompt-director` and downstream tools unless the user explicitly changes them.
- `Avoid` carries copyright, brand, deformation, wrong text, platform, and continuity constraints.
- `Selected input` can be a short description, existing URL, local file label, generated output id, slide id, shot id, or visual-board id. Do not expose private local paths in formal client documents unless the user asks for an internal appendix.
- `Privacy/cost gate` must be explicit before uploading private/client assets, creating public URLs, running paid generation, publishing to Feishu, or starting long polling.

## Tool Skill Loading

Tool skills are not Studio roles. Do not look for `Studio_Skills/banana-pro/SKILL.md`, `Studio_Skills/seedance-2-video/SKILL.md`, `Studio_Skills/url-relay/SKILL.md`, `Studio_Skills/storyboard-visual-word/SKILL.md`, or `Studio_Skills/feishu-docs/SKILL.md`.

When the user explicitly asks for 香蕉 / banana / Banana Pro / Nano Banana / `@banana-pro`, first decide whether upstream Studio work is still needed. Load Banana Pro only after the current upstream deliverable and prompt are ready.

When the user explicitly asks for 即梦2.0生成 / 即梦生成 / Seedance 2.0 / Ark Seedance / `@seedance-2-video`, first decide whether upstream Studio work is still needed. Load Seedance only after the selected clip/shot handoff and final video prompt are ready.

When the user explicitly asks for URL中转 / 公网URL / 上传参考图 / 上传参考视频 / `@url-relay`, or a Seedance request contains local media files, load URL Relay only for the media handoff. Do not let URL Relay bypass the upstream Studio role or `prompt-director`.

When the user explicitly asks for 抠图 / 扣图 / 去底 / 去黑底 / 黑底转透明 / 透明底 PNG / `@black-background-cutout`, load Black Background Cutout only for local image pixel processing. Do not run prompt writing, generation, upload, or full project routing unless the user also asks for redesign.

When the user explicitly asks for 视觉方案文件 / 视觉导演方案 / Word视觉方案 / DOCX视觉方案 / 分镜视觉方案文件 / `@storyboard-visual-word`, load Storyboard Visual Word only after selected visuals and scene rationale are ready. It packages a DOCX handoff; it does not create the full storyboard.

When the user explicitly asks for 转到飞书 / 同步到飞书 / 发布到飞书 / 飞书视觉方案 / 飞书分镜 / Lark Docs / `@feishu-docs`, load Feishu Docs only after the visual plan/storyboard handoff content is ready. It renders or publishes a document handoff; it does not create the full storyboard or generate images.

Default upstream chains:

- storyboard/video/film frame request: `storyboard-director` or `cinematographer` -> Selected Asset Packet -> `prompt-director` -> `banana-pro`
- storyboard reference angle frame: `storyboard-director` -> optional `cinematographer` -> Selected Asset Packet -> `prompt-director` -> imagegen or `banana-pro` for one selected still
- poster visual request: `poster-art-director` or `layout-designer` -> Selected Asset Packet -> `prompt-director` -> `banana-pro`
- PPT/deck/slide visual request: `presentation-designer` or `layout-designer` -> Selected Asset Packet -> `prompt-director` -> `banana-pro`
- direct final prompt request: `prompt-director` -> `banana-pro`
- direct local cutout request: `black-background-cutout`
- Seedance video clip request: `storyboard-director`, `cinematographer`, or `edit-director` if needed -> Selected Asset Packet -> `prompt-director` -> `seedance-2-video`
- Seedance video clip request with local reference files: `storyboard-director`, `cinematographer`, or `edit-director` if needed -> Selected Asset Packet -> `prompt-director` -> `url-relay` -> `seedance-2-video`
- direct final Seedance prompt request: `prompt-director` -> `seedance-2-video`
- direct final Seedance prompt request with local reference files: `prompt-director` -> `url-relay` -> `seedance-2-video`
- visual方案文件 with selected images: `finishing-producer` -> `storyboard-visual-word`
- visual方案文件 still needing visuals: upstream visual role -> optional tool generation/selection -> `finishing-producer` -> `storyboard-visual-word`
- Feishu visual/storyboard handoff already prepared: `finishing-producer` -> `feishu-docs`
- Feishu handoff still needing visuals/source content: upstream visual role -> optional tool generation/selection -> `finishing-producer` -> `feishu-docs`

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

For Black Background Cutout execution, load:

1. the first available Black Background Cutout tool skill path:
   - `black-background-cutout/SKILL.md`
   - `C:\Users\Administrator\.codex\skills\black-background-cutout\SKILL.md`
   - `C:\Users\Administrator\plugins\sw-v1-0\skills\black-background-cutout\SKILL.md`

For Storyboard Visual Word execution, load:

1. `Studio_Skills/finishing-producer/SKILL.md` when delivery naming, file package, or client handoff context matters
2. the first available Storyboard Visual Word tool skill path:
   - `storyboard-visual-word/SKILL.md`
   - `C:\Users\Administrator\.codex\skills\storyboard-visual-word\SKILL.md`
   - `C:\Users\Administrator\plugins\sw-v1-0\skills\storyboard-visual-word\SKILL.md`

For Feishu Docs execution, load:

1. `Studio_Skills/finishing-producer/SKILL.md` when delivery naming, privacy checks, or client handoff context matters
2. the first available Feishu Docs tool skill path:
   - `feishu-docs/SKILL.md`
   - `C:\Users\Administrator\.codex\skills\feishu-docs\SKILL.md`
   - `C:\Users\Administrator\plugins\sw-v1-0\skills\feishu-docs\SKILL.md`

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

Storyboard Visual Word trace:

```text
Studio roles: Finishing Producer / `finishing-producer` (loaded). Cost lane: production.
Tool skill: Storyboard Visual Word / `storyboard-visual-word` (loaded for visual方案文件/DOCX handoff).
```

Feishu Docs trace:

```text
Studio roles: Finishing Producer / `finishing-producer` (loaded). Cost lane: production.
Tool skill: Feishu Docs / `feishu-docs` (loaded for explicit Feishu handoff).
```

Execution rule:

- If `OPENROUTER_API_KEY` is set or the private Banana Pro env file is configured and generation is confirmed, run the Banana Pro script from the loaded skill folder.
- Treat explicit "use banana to generate one draft" as confirmation for one draft image only; still pause for private uploads, final-use brand/face/product assets, or batch generation.
- Default Banana Pro output is `2K`; use `1K` only for explicit fast drafts and `4K` after user confirmation or final review.
- Do not run a separate key-check command every time. Let the Banana runner check the key; after one successful key-readable check or generation in the same conversation, treat the key as available unless the runner reports otherwise.
- If the Banana Pro key is missing, run `--dry-run` or return the payload path/status; do not search for another imaginary executor.
- If `ARK_API_KEY` or the Seedance local private key file is available and video generation is confirmed, run the Seedance script from the loaded skill folder.
- Treat explicit "use 即梦2.0 to generate one draft clip" as confirmation for one draft clip only; still pause for private uploads, final-use brand/face/product assets, 1080p, long polling, or batch generation.
- If Seedance input is local media, use URL Relay first and pass the returned public URL with `--image-url`, or use Seedance runner `--image-file` after the privacy/upload guardrail is satisfied.
- If URL Relay fails, do not submit real Seedance generation. First try the SW media uploader; if it is unreachable/server-failing and confirmed/configured fallback exists, use the temporary relay and say so. Otherwise keep the prompt/payload and ask for a public URL.
- If the Seedance key is missing, run `dry-run` or return the sanitized payload; do not search for another imaginary video executor.
- If the user asks for a visual方案文件, 视觉导演方案, Word视觉方案, DOCX视觉方案, 分镜视觉方案文件, or `@storyboard-visual-word`, load Storyboard Visual Word only after selected storyboard/scene/concept images and concise rationale exist.
- Storyboard Visual Word is a downstream DOCX handoff tool, not a full storyboard generator. If the visuals are not ready, route upstream first; do not fabricate images or Word pages.
- If the user asks to transfer/publish a visual plan or storyboard to Feishu/Lark, load Feishu Docs only after the handoff content exists. Render/dry-run is local; real publishing requires Feishu app credentials plus explicit `--execute`.

## Prompt Quality Rules

- Translate vague words into controllable parameters.
- Image parameters: subject, subject proportion, shot size, composition, lens, lighting, color, material, background, aspect ratio, constraints, negative prompt.
- Video parameters: shot goal, duration, start frame, end frame, camera movement, subject action, transition, sound cue, continuity constraints.
- Read `Prompts/Image_Aesthetic_Prompt_Reference.md` only for stronger visual taste, anti-AI look, or filmic image prompt refinement.
- Read `01_Research/HQ_Aesthetic_References/Aesthetic_Decision_Index.md` only when the visual style is not locked, the user asks SW to decide the look, or project-local visual references need interpretation.
- Read `01_Research/HQ_Aesthetic_References/HQ_Aesthetic_Master_Index.md` only when the user asks for HQ aesthetic references, source lanes, contact sheets, or moodboard calibration.
- Read `01_Research/HQ_Aesthetic_References/Aesthetic_Library_Config.md` and run `tools/aesthetic_library_doctor.py` only for storage relocation, missing-image debugging, or aesthetic-library maintenance.
- Read `Prompts/Video_Motion_Edit_Prompt_Rules.md` only for one-take, bullet-time, hero-shot, complex motion, edit-technique, or Seedance/AI-video execution prompts.
- Read `Prompts/Visual_Development_Board_Rules.md` only for character setting sheets, scene setting sheets, integrated storyboard sheets, or production-design board prompts.
- Read `Prompts/Tool_Official_Prompt_Deltas.md` only when a named tool needs official-case conversion or repeated execution failures require a tool-specific delta. Read only the relevant tool section and keep the universal prompt first.
- Read `01_Research/Oscar_Best_Picture_Visual_Reference.md` only when the user asks for Oscar/classic film visual references; extract grammar only, never copied frames.
- Read `01_Research/Aesthetic_Daily_Selected/Daily_Selected_Index.md` only when the user asks for daily selected references, user-supplied aesthetic materials, moodboards, or today's supplemental visual references; read only the relevant date/contact sheet.
- Separate poster text into two lanes. Display lettering (hero headline, launch title, large numerals, glowing/metal/3D/neon title blocks) is visual art and should preserve image-model/design effects; do not replace it with plain default system fonts. Exact information text (date, price, parameters, small copy, logo, QR, legal text) should usually be added or QA'd in post-production.
- For revisions, change only affected parameters to reduce result drift.
- If review finds must-fix items, `review-producer` should create a compact `Review Delta Packet`; `change-manager` consumes it before rewriting so the fix stays scoped.
- If midstream feedback arrives outside final review, especially from screen recordings, meeting notes, chat logs, screenshot annotations, boss oral comments, or client comments, `change-manager` should create or consume a compact `Change Delta Packet` before rewriting so local comments do not become accidental rebriefs.

## Visual Development Boards

- Character setting sheets lock recurring characters before storyboard/image/video generation. Include a large full-body hero, neutral front/back/profile views, expression studies, detail crops, silhouette study, signature prop, and color palette.
- Scene setting sheets lock recurring locations before storyboard/image/video generation. Include an establishing view, secondary angles, prop/material details, lighting study, and palette.
- Reference angle frames are optional still plates for storyboard assistance. Use them only for a selected scene angle, camera position, or spatial relation; they support the next storyboard board or Seedance first-frame prompt and do not imply batch generation.
- Integrated storyboard sheets are grouped review boards. Default grouping follows 15-second segments; each group must stay <=15 seconds and at most 9 shots. Do not force 9 panels/3x3; choose layout from actual shot count. If a shot cannot land cleanly on the 15-second boundary, first adjust shot durations slightly, otherwise start the next group.
- Full-storyboard triggers such as "生成全部分镜", "完整分镜", "全片分镜", "全量跑分镜", or "按剧本生成所有镜头" use the real script shot count. Supplemental shots are allowed only for narrative function; contact sheets use 3x3 pages with black slots for unused, missing, or failed frames.
- For Banana generation, a request to generate a character sheet or storyboard sheet confirms one draft board only, not a batch.

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
- for maintenance/publish, `tools/sw_consistency_check.py` passes before commit

For complex handoffs, tool integration, eval/debug, or architecture maintenance, apply the OpenAI Agents SDK-inspired pattern from `Agent_Skill_Tech_Principles.md`: compact ownership handoff, blocking guardrails before risky work, lightweight internal trace, and explicit tool-level safety checks. Do not imply a real SDK run unless one was actually used.
