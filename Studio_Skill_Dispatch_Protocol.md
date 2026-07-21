# Studio Skill Dispatch Protocol

This protocol makes each studio skill an executable role, not a decorative label.

## When It Applies

Apply this protocol only after SW has been explicitly activated in the current conversation. Do not apply it just because the user mentions a design topic. Once activated, use it for project work such as:

- brief, research, direction
- presentation, PPT, deck, slides
- poster, layout, copy
- video, film, script, storyboard
- edit, motion, sound, color
- AI image/video prompts
- tool integration
- review, change, finishing

Do not apply it when the user only invokes `/SW_V1.0`, `@SW_V1.0`, `/sw`, or only invokes `@sw_update`. Do not apply it before explicit SW activation.

## Dispatch Steps

Use the Fast Path unless the request needs deeper routing.

Fast Path:

1. Read `SW_Runtime_Index.md`.
2. Read `Cost_Governor.md`.
3. Read `Studio_Role_Label_Protocol.md`.
4. Use the routing summary in `SW_Runtime_Index.md` to choose the obvious role.
5. If the current long-running project has `.sw/` memory files, read only the relevant `MEMORY.md`, `RULES.md`, or `PROJECT.md`.
6. Read selected `Studio_Skills/<skill-id>/SKILL.md` before producing the deliverable.
7. Show one role trace using the label protocol.
8. Produce only the current role's deliverable, plus questions and recommendation for the next step.

Escalate to full routing only when needed:

- request type or stage is unclear
- route conflicts with current project state
- user asks for full workflow, status, audit, SOP, or company handoff
- complex campaign, film, tool integration, eval/debug, or architecture maintenance
- visual style is missing and project-local references or global aesthetic defaults need arbitration
- stage transition depends on a chain decision
- a selected skill references optional files that are relevant to the request

Full routing adds only the necessary files:

1. Read `Auto_Assignment_Rules.md` for route resolution.
2. Read `Production_Pipeline_Map.md` for multi-stage handoff or full pipeline decisions.
3. Read `Studio_Skill_Map.md` for role boundary conflicts.
4. Read `Agent_Skill_Tech_Principles.md` only for architecture updates, complex handoffs, tool integration, or eval/debug work.

## Skill Count

- Default: 1 primary role plus up to 1 support role.
- Low-token mode: primary role only unless a support role is required for safety or tool correctness.
- Complex campaign/film: up to 3 roles when needed.
- Never load all studio roles by default.

## Required Trace

```text
Studio roles: English Title / `skill-id` + English Title / `skill-id` (loaded). Cost lane: production.
```

If only one role is needed:

```text
Studio roles: English Title / `skill-id` (loaded). Cost lane: review/change.
```

If a selected skill file is missing:

```text
Studio roles: English Title / `skill-id` (file missing, fallback rules used). Cost lane: intake.
```

External tool skills are shown separately only when explicitly loaded:

```text
Tool skill: Banana Pro / `banana-pro` (loaded by explicit user request).
```

```text
Tool skill: Dreamina CLI / `dreamina-cli` (loaded by explicit user request).
```

```text
Tool skill: Seedance 2.0 Video / `seedance-2-video` (loaded by explicit user request).
```

```text
Tool skill: URL Relay / `url-relay` (loaded for local media public URL handoff).
```

```text
Tool skill: Black Background Cutout / `black-background-cutout` (loaded for explicit cutout request).
```

```text
Tool skill: Storyboard Visual Word / `storyboard-visual-word` (loaded for visual方案文件/DOCX handoff).
```

Do not put external tool skills inside the `Studio roles:` trace. For Banana Pro, the correct trace is:

```text
Studio roles: Prompt Director / `prompt-director` (loaded). Cost lane: high-cost.
Tool skill: Banana Pro / `banana-pro` (loaded by explicit user request).
```

Never combine Banana Pro, Dreamina CLI, Seedance, URL Relay, or Black Background Cutout into the Studio role trace.
Never combine Storyboard Visual Word into the Studio role trace.

## Tool No-Bypass Rule

External tool skills must not replace upstream Studio roles.

## Compare Board Rule

Compare Board is a lightweight selection object, not a new full stage. Use it after creative directions, storyboard groups, or deck structures when the user needs comparison or feedback is abstract. Output only:

```text
Compare Board:
- Keep:
- Remove:
- Next version:
```

Do not add new concepts, extra directions, batch rewrites, or long rationale inside the Compare Board unless the user explicitly asks.

## Project Asset Graph Rule

Project Asset Graph is a compact project-level continuity map before storyboard. Use it at project start or when the user asks for a storyboard if recurring characters, scenes, props, products, wardrobe, existing footage, or reference assets are not locked.

```text
Project Asset Graph:
- Asset source mode:
- Existing assets:
- Assets to create:
- Character nodes:
- Scene/location nodes:
- Prop/product/wardrobe nodes:
- Continuity locks:
- Storyboard handoff:
```

Route to `production-designer` first, then `storyboard-director`. If the user wants speed, write assumptions and continue. Do not treat this as a Selected Asset Packet; that packet is only for one chosen item going to prompt writing, URL relay, generation, DOCX, or Feishu.

## Selected Asset Packet Rule

Selected Asset Packet is a selected-object handoff, not a new role or stage. Use it when an upstream role has chosen one concrete object for prompt writing, URL upload, image/video generation, DOCX packaging, or Feishu publishing.

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

- The upstream role owns selection; `prompt-director` and tool skills consume the packet.
- Use it for selected poster key visuals, deck page visuals, storyboard shots/groups, reference angle frames, local media files, public URLs, generated images, or selected concept images.
- Skip it for direct final-prompt requests where the user already supplied the complete prompt.
- `Reference roles` must define how each reference is used: character identity, product shape, scene layout, composition, style, texture, color, first frame, last frame, or edit source.
- `Locked items` and `Avoid` survive downstream prompt conversion unless the user explicitly changes them.
- Resolve `Privacy/cost gate` before public URL upload, paid generation, Feishu publishing, or long polling.
- Formal client handoffs should not expose local paths, raw prompts, tool parameters, or generation tables unless the user asks for an internal appendix.

## Quick Edit Rule

For S/M-level changes to an existing poster/image, deck page or outline, storyboard group or shot, edit-plan segment, or prompt, route to the affected role and output the revised object first. Ask at most one blocking question.

If feedback changes audience, core message, narrative structure, visual style, project goal, or deliverable form, route to `change-manager` before rewriting. Midstream boss/client feedback, screen-recording notes, meeting notes, chat logs, screenshot annotations, and oral comments can be compressed into a `Change Delta Packet` so `Keep unchanged` survives the handoff.

## Aesthetic Decision Rule

When the user has not specified the visual style, or asks SW to choose the best look, load `aesthetic-director` before expensive visual production, prompt writing, Banana generation, Seedance generation, storyboard boards, or deck polish. Read only `Aesthetic_Decision_Index.md` by default. Project-local `.sw` visual references and user-supplied reference images override the global library.

## Historical Accuracy No-Bypass Rule

Historical accuracy is confirmation-gated and visual-output focused.

- Clear historical risk without confirmation only adds: `检测到历史准确性风险。是否开启历史准确性检查？默认不开启。`
- Clear historical drama, cultural-heritage, archaeology, ancient craft, intangible-heritage, dynasty-specific artifact, or museum-narrative work may instead add one broader nudge: `检测到历史/文博题材。可开启历史准确性检查，或使用历史剧胶片风格胶囊；默认不开启。`
- The Historical Drama Style Capsule is a look/prompt baseline, not an accuracy gate and not a new role. It can be used by `storyboard-director` or `prompt-director` only after user confirmation or when the visual style is already locked.
- If the project request is otherwise actionable, continue the normal route with historical checking off by default.
- Do not load `historical-consultant` for style-only words such as 国风, 古风, 唐风, 宋韵, 东方美学, 敦煌感, 新中式, or 仙侠感.
- Plain `开启历史检查` applies to the current request/current visual-output chain. Project-level scope requires `本项目开启历史检查` or `全程开启历史检查`.
- `关闭历史检查`, `不用历史检查`, or `恢复普通模式` disables current project-level historical checking. Permanent memory changes require explicit memory update/delete.
- After the user confirms historical checking, route `historical-consultant` before visual production when period/civilization decisions affect clothing, architecture, props, patterns, or scene world.
- If image generation is requested, route: `historical-consultant` -> affected Studio role -> `prompt-director` -> explicit tool skill if any -> `review-producer` or `historical-consultant` image QA.
- For video projects, historical checking applies to storyboard first frames, still references, visual assets, generated images, and representative Seedance output frames when available. Do not claim full automated video QA; review visible frames/stills and user-provided output.

For Banana Pro:

- If the user asks for a direct image from an already complete prompt, route `prompt-director` -> `banana-pro`.
- If the user asks for storyboard, video, film, poster, PPT/deck/slide, layout, character, product, prop, or scene design and also says to use Banana, first route the upstream Studio role that owns the design decision, then `prompt-director`, then `banana-pro`.
- Only the selected frame/image is generated by default. Batch storyboards, multiple slides, and full variant sets require explicit batch confirmation.
- The visible trace may show the current upstream role and `prompt-director` as Studio roles, while Banana remains a separate Tool skill.

Example for a storyboard first-frame request:

```text
Studio roles: Storyboard Director / `storyboard-director` + Prompt Director / `prompt-director` (loaded). Cost lane: high-cost.
Tool skill: Banana Pro / `banana-pro` (loaded by explicit user request).
```

For Dreamina CLI:

- If the user asks for direct Dreamina CLI / Jimeng CLI / official Jimeng CLI / `dreamina` generation from an already complete prompt, route `prompt-director` -> `dreamina-cli`.
- If the user asks for script, storyboard, camera, edit, motion, sound, color, scene design, film treatment, poster, PPT/deck/slide, layout, character, product, prop, or production design and also says to use Dreamina/Jimeng CLI, first route the upstream Studio role that owns the design decision, then `prompt-director`, then `dreamina-cli`.
- Only the selected image, clip, or task is generated by default. Batch outputs, private uploads, install/login/relogin, 4K/1080p finals, final-use brand/face/product assets, and long polling require explicit confirmation.
- The current CLI is the source of truth. Inspect `dreamina -h` and the relevant `dreamina <subcommand> -h` before real use; do not hardcode supported models or parameters.
- If `dreamina` is missing or login is missing, produce help/preflight or prompt-only handoff. Do not claim a real image or video was generated.

Example for a selected Dreamina CLI video-shot request:

```text
Studio roles: Storyboard Director / `storyboard-director` + Prompt Director / `prompt-director` (loaded). Cost lane: high-cost.
Tool skill: Dreamina CLI / `dreamina-cli` (loaded by explicit user request).
```

For Seedance 2.0 Video:

- If the user asks for a direct Seedance/即梦 video from an already complete prompt, route `prompt-director` -> `seedance-2-video`.
- If the user asks for script, storyboard, camera, edit, motion, sound, color, scene design, film treatment, or production design and also says to use Seedance/即梦, first route the upstream Studio role that owns the design decision, then `prompt-director`, then `seedance-2-video`.
- Only the selected clip/shot is generated by default. Batch shots, multiple aspect ratios, 1080p finals, and long polling require explicit confirmation.
- If the selected Seedance input is a local image/video file, route `prompt-director` -> `url-relay` -> `seedance-2-video`. Relay upload must succeed before real generation.
- Missing `ARK_API_KEY` or local Seedance key means dry-run/payload only. Do not claim a real video was generated.

Example for a selected video-shot request:

```text
Studio roles: Storyboard Director / `storyboard-director` + Prompt Director / `prompt-director` (loaded). Cost lane: high-cost.
Tool skill: Seedance 2.0 Video / `seedance-2-video` (loaded by explicit user request).
```

Example for a selected video-shot request with local media:

```text
Studio roles: Storyboard Director / `storyboard-director` + Prompt Director / `prompt-director` (loaded). Cost lane: high-cost.
Tool skill: URL Relay / `url-relay` (loaded for local media public URL handoff).
Tool skill: Seedance 2.0 Video / `seedance-2-video` (loaded by explicit user request).
```

For Storyboard Visual Word:

- If the user asks for a visual方案文件, 视觉导演方案, Word视觉方案, DOCX视觉方案, 分镜视觉方案文件, or `@storyboard-visual-word`, load it only after selected storyboard/scene/concept images and concise visual-setting rationale exist.
- If the request still needs storyboard design, scene/character setting, image generation, or visual selection, first route the upstream Studio role and any explicit generation tool. Then package the selected visuals into DOCX.
- Do not include prompt bodies, local image paths, generation-result tables, or Midjourney/Banana/Seedance parameters in the formal Word unless the user explicitly asks for an internal production appendix.

Example for a visual director Word handoff:

```text
Studio roles: Finishing Producer / `finishing-producer` (loaded). Cost lane: production.
Tool skill: Storyboard Visual Word / `storyboard-visual-word` (loaded for visual方案文件/DOCX handoff).
```

## Questions And Suggestions

- Each invoked project role should include 3 useful questions by default.
- Use up to 5 questions for complex setup, film, campaign, tool risk, or blocked delivery.
- Use at most 1 question in low-token or "you decide" mode.
- Questions must support the next role or unblock execution.
- Every role should include a concise recommendation and next role.
- After major durable confirmations, add at most one short project-memory suggestion line. Do not expand the memory system unless the user asks.
- After the deliverable, add at most one reply-end nudge only when useful. Nudge types are memory, lock, next step, risk, or cost. The nudge must be one short line and must not add extra reads, new workflow stages, or multiple reminders.

## Handoff Packet

Keep this internally whenever one role hands off to another:

```text
from_role:
to_role:
project_type:
current_stage:
locked_decisions:
assumptions:
deliverable_done:
risks:
open_questions:
next_action:
cost_lane:
```

Show it only when the user asks for status, audit, or handoff notes.

## Agents SDK-Inspired Routing Rules

Use the OpenAI Agents SDK pattern as an internal routing discipline:

- a handoff means the next role owns the next answer
- the handoff reason must be short and tied to the next deliverable
- blocking guardrails run before expensive generation, tool use, uploads, publishing, or irreversible actions
- final output review belongs to the final deliverable/review role, not every intermediate role
- internal trace should record selected role, handoff reason, checked guardrails, and cost lane

Do not over-apply this pattern:

- do not create extra roles just because a handoff is possible
- do not expose debug trace unless the user asks
- do not claim a real SDK trace, guardrail, or agent run unless an actual SDK/tool integration was used
- do not treat role-level guardrails as enough for external tools; tool integrations need their own checks

## No Pretend Calls

Do not say a role was loaded unless its `SKILL.md` file was available and read.

For `banana-pro`, do not search for `Studio_Skills/banana-pro/SKILL.md`; it is not a Studio role. Load it as a tool skill from the first available path:

1. `banana-pro/SKILL.md` in the current project folder
2. `C:\Users\Administrator\.codex\skills\banana-pro\SKILL.md`
3. `C:\Users\Administrator\plugins\sw-v1-0\skills\banana-pro\SKILL.md`

For `dreamina-cli`, do not search for `Studio_Skills/dreamina-cli/SKILL.md`; it is not a Studio role. Load it as a tool skill from the first available path:

1. `dreamina-cli/SKILL.md` in the current project folder
2. `C:\Users\Administrator\.codex\skills\dreamina-cli\SKILL.md`
3. `C:\Users\Administrator\plugins\sw-v1-0\skills\dreamina-cli\SKILL.md`

For `seedance-2-video`, do not search for `Studio_Skills/seedance-2-video/SKILL.md`; it is not a Studio role. Load it as a tool skill from the first available path:

1. `seedance-2-video/SKILL.md` in the current project folder
2. `C:\Users\Administrator\.codex\skills\seedance-2-video\SKILL.md`
3. `C:\Users\Administrator\plugins\sw-v1-0\skills\seedance-2-video\SKILL.md`

For `url-relay`, do not search for `Studio_Skills/url-relay/SKILL.md`; it is not a Studio role. Load it as a tool skill from the first available path:

1. `url-relay/SKILL.md` in the current project folder
2. `C:\Users\Administrator\.codex\skills\url-relay\SKILL.md`
3. `C:\Users\Administrator\plugins\sw-v1-0\skills\url-relay\SKILL.md`

For `black-background-cutout`, do not search for `Studio_Skills/black-background-cutout/SKILL.md`; it is not a Studio role. Load it as a tool skill from the first available path:

1. `black-background-cutout/SKILL.md` in the current project folder
2. `C:\Users\Administrator\.codex\skills\black-background-cutout\SKILL.md`
3. `C:\Users\Administrator\plugins\sw-v1-0\skills\black-background-cutout\SKILL.md`

For `storyboard-visual-word`, do not search for `Studio_Skills/storyboard-visual-word/SKILL.md`; it is not a Studio role. Load it as a tool skill from the first available path:

1. `storyboard-visual-word/SKILL.md` in the current project folder
2. `C:\Users\Administrator\.codex\skills\storyboard-visual-word\SKILL.md`
3. `C:\Users\Administrator\plugins\sw-v1-0\skills\storyboard-visual-word\SKILL.md`

If a historical conversation cannot read the latest local files, tell the user to run `@sw_update` or start a new conversation.

## Token Control

- Dreamina CLI token/control supplement:
  - `dreamina-cli` loads only when the user explicitly asks for Dreamina CLI, Jimeng CLI, official Jimeng CLI, `dreamina`, `@dreamina-cli`, 即梦官方 CLI, 即梦生成图片, 即梦生成视频, or official Jimeng/Dreamina CLI generation.
  - It is a post-prompt image/video generation member; route `prompt-director` -> `dreamina-cli` for explicit final-prompt requests.
  - If the request includes upstream design work, do not let `dreamina-cli` skip the relevant Studio role; generate only after the selected prompt handoff is ready.
  - Do not run Dreamina CLI installer, login/relogin, real generation, private upload, batch generation, 4K/1080p/final output, or long unattended polling without confirmation.
  - Inspect `dreamina -h` and the relevant `dreamina <subcommand> -h` before real use; if the CLI is missing or login is missing, stop at help/preflight or prompt-only handoff.

- never paste full skill contents into the answer
- never paste full project memory files into the answer
- never show the full pipeline unless the user asks for structure
- produce one deliverable type per turn
- high-cost prompts/scripts/batches require confirmation
- prompt-only requests skip full workflow and go directly to `prompt-director`
- `banana-pro` loads only when the user explicitly asks for 香蕉, banana, Banana Pro, Nano Banana, OpenRouter image generation, `@banana-pro`, or this image-generation member
- `banana-pro` is a post-prompt image-generation member, similar to `imagegen`; route `prompt-director` -> `banana-pro` for explicit generation requests
- if the request includes upstream design work, do not let `banana-pro` skip the relevant Studio role; generate only after the selected prompt handoff is ready
- `seedance-2-video` loads only when the user explicitly asks for 即梦2.0生成, 即梦生成, Seedance 2.0, Ark Seedance, 豆包 Seedance, `@seedance-2-video`, or this video-generation member
- `seedance-2-video` is a post-prompt video-generation member; route `prompt-director` -> `seedance-2-video` for explicit generation requests
- if the request includes upstream video/film design work, do not let `seedance-2-video` skip the relevant Studio role; generate only after the selected clip/shot prompt is ready
- `url-relay` loads only when the user explicitly asks for URL中转, 公网URL, 上传参考图/视频, `@url-relay`, or a downstream tool such as Seedance needs a public URL but the user provided a local file
- `url-relay` is a public URL handoff member; route it after prompt/design handoff and before the downstream tool
- `black-background-cutout` loads only when the user explicitly asks for 抠图, 扣图, 去底, 去黑底, 黑底转透明, 透明底 PNG, or `@black-background-cutout`
- `black-background-cutout` is a local pixel-processing member for existing images. It does not use prompt writing, image generation, upload, or full project routing, and it must warn that quick cutouts may have slight fringing.
- if relay upload fails, do not spend generation credits until a public URL exists. First report that the SW media uploader is unavailable; then use an already-public URL or a confirmed/configured Litterbox/Catbox fallback only for unreachable/server-side relay failures. Missing token/address or permission errors stop for config repair. Otherwise keep the prompt/payload and ask for a public URL.
- `storyboard-visual-word` loads only when the user explicitly asks for 视觉方案文件, 视觉导演方案, Word视觉方案, DOCX视觉方案, 分镜视觉方案文件, or `@storyboard-visual-word`
- `storyboard-visual-word` is a downstream DOCX handoff member; route it after selected visuals and scene rationale are ready, not during ordinary storyboard planning
- preserve locked decisions and pass only the useful handoff packet to the next role
- project memory suggestions are optional one-liners and require explicit user approval before writing
