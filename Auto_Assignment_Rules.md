# Auto Assignment Rules

Use these rules to choose the current studio role only after SW has been explicitly activated. The user should not need to manually select roles after activation.

## Inputs

Judge these before every activated SW project reply:

- project type: poster, presentation/deck/PPT/slides, video, poster+video, film/brand film, prompt-only, tool, review, revision, unclear
- current stage: intake, research, direction, copy, poster, layout, script, storyboard, camera, edit, motion, sound, color, prompt, review, finishing, change
- user intent: start, continue, create, refine, prompt, tool, check, revise, deliver
- cost mode: normal, low-token, detailed, company delivery
- risk: copyright, brand, platform, tool, missing information
- aesthetic auto-selection: use when visual style is missing, SW should decide the look, or project-local references need interpretation
- feature risk: Banana explicit generation, Dreamina/Jimeng CLI generation, Kling CLI/MCP generation, Seedance/即梦 explicit video generation, historical accuracy reminder, project memory

## Priority Routing

Dreamina/Jimeng official CLI override:

- Official Dreamina/Jimeng CLI triggers include Dreamina CLI, Jimeng CLI, official Jimeng CLI, `dreamina`, `@dreamina-cli`, 即梦官方 CLI, 即梦生成图片, 即梦生成视频, and wording that explicitly means the official local CLI rather than Ark Seedance API.
- A complete final Dreamina/Jimeng CLI prompt routes `prompt-director` -> `dreamina-cli`; add `tool-integrator` only when installed state, login state, capability, model support, parameters, or connection state is unclear.
- If the same request also asks for script, storyboard, camera, edit rhythm, motion, sound, color, poster, PPT/deck/slide, layout, character, product, prop, or scene design, route the upstream Studio role first, then `prompt-director`, then `dreamina-cli`. Do not let the tool trigger bypass the design role.
- If local image/video/audio references are involved, inspect current CLI help before deciding whether local files are supported. If public URLs are required, insert `url-relay`; stop before real generation if install, login, upload permission, paid generation, batch generation, or long polling is not confirmed.
- Keep `seedance-2-video` for Ark Seedance API / Seedance 2.0 requests. Ambiguous 即梦 wording should not silently switch to the official CLI unless the user names the CLI route.

Kling official CLI/MCP override:

- Official Kling CLI/MCP triggers include Kling CLI, 可灵 MCP, `kling-cli`, `@kling-cli`, 可灵官方 CLI, 可灵文生图, 可灵图生图, 可灵文生视频, 可灵图生视频, and wording that explicitly means the OAuth/MCP local CLI route rather than the API Key/legacy AK/SK API.
- A complete final Kling CLI/MCP prompt routes `prompt-director` -> `kling-cli`; add `tool-integrator` only when installed state, OAuth login state, capability, model support, parameters, or MCP tool availability is unclear.
- If the same request also asks for script, storyboard, camera, edit rhythm, motion, sound, color, poster, PPT/deck/slide, layout, character, product, prop, or scene design, route the upstream Studio role first, then `prompt-director`, then `kling-cli`. Do not let the tool trigger bypass the design role.
- Before real generation, inspect `kling who_am_i` and, when needed, `kling tool_list` or `kling <command> --help`; do not hardcode models or parameters. Stop before install, login/relogin, private upload, paid generation, batch generation, final output, or long polling unless confirmed.
- Keep `kling-api` for explicit API Key or legacy AK/SK official API requests. Do not silently switch between `kling-cli` and `kling-api`.
- For Kling API video work, use Kling 3.0 for ordinary generation and Kling 3.0 Omni for reference-video generation or base-video edits. Read the current tool skill before constructing payloads; the current API and legacy `/v1` schemas differ.
- Explicit Hermes collaboration/setup routes to `hermes-bridge`, a local tool bridge rather than a Studio role. Use the existing runtime and shared Kling runner; do not start another agent or copy private credentials as part of a file handoff.

0. Rescue-only commands (`/sw-rescue`, `@sw_rescue`, `SW_RESCUE`, `SW_REPAIR`, `SW_FORCE_UPDATE`) -> use `sw-rescue`, reply with the fixed rescue line, and do not start a project.
0. `@sw_help`, `/sw_help`, feature trigger questions -> use the embedded `sw-help` short answer first; read `Feature_Trigger_Index.md` only for detailed triggers/debug; do not start a project.
1. Historical accuracy:
   - Clear risk but no user confirmation -> add the one-line reminder, continue the normal low-cost route, and do not load `historical-consultant`.
   - User confirms historical checking -> `historical-consultant` first, then affected visual role, then `prompt-director` if generating, then final image QA via `historical-consultant` or `review-producer`.
   - Plain `开启历史检查` applies to the current request/visual chain. `本项目开启历史检查` or `全程开启历史检查` applies to the current conversation/project until closed.
   - `关闭历史检查`, `不用历史检查`, or `恢复普通模式` disables current project-level historical checking. If the setting was saved in `.sw/MEMORY.md`, require explicit memory update/delete to persist the closure.
   - For video, check storyboard first frames, still references, visual assets, generated images, and representative Seedance output frames when available. Do not claim full automated video QA beyond visible frames/stills.
2. Existing object quick edit:
   - If the user provides or refers to an existing poster/image and asks to modify, repair, export variants, improve title treatment, match a reference, or says the output is too plain, route to Poster Quick Edit instead of the full poster pipeline.
   - Use `poster-art-director` or `layout-designer` for the affected visual decision; add `prompt-director` and an image-generation/editing tool only when visual rendering is needed.
   - If the user refers to an existing deck page/outline, storyboard group/shot list, edit plan/timeline, or prompt and asks for a local S/M-level fix, route directly to `presentation-designer`, `storyboard-director`, `edit-director`, or `prompt-director` for quick edit.
   - Ask at most one blocking question. Prefer image/output first, then no more than three short notes.
   - Display lettering (hero title, launch title, big numerals, glowing/metal/3D/neon title blocks) should keep or regain image-model/design effects. Do not downgrade it to plain system fonts.
   - If feedback changes audience, core message, narrative structure, visual style, project goal, or deliverable form, route to `change-manager`.
3. Compare request / abstract selection feedback after directions, storyboard groups, or deck structures -> current primary role outputs Compare Board only.
4. Revision/feedback/change, including screen recordings, meeting notes, chat logs, screenshot annotations, boss oral comments, or client comments -> `change-manager`.
5. New tool, connector, plugin, tool-specific prompt conversion -> `tool-integrator`.
   - If an upstream role has selected a concrete poster/deck/storyboard/reference/media object for prompt writing, URL upload, generation, DOCX, or Feishu, insert a Selected Asset Packet before `prompt-director` or the explicit tool. Do not treat it as a separate Studio role.
   - Explicit 香蕉 / banana / Banana Pro / Nano Banana / OpenRouter image-generation request with a complete final prompt -> `prompt-director` -> `banana-pro`; add `tool-integrator` only when capability, parameters, API, or connection state is unclear.
   - If explicit Banana generation is bundled with storyboard, video/film shot design, poster, PPT/deck/slide, layout, character, product, prop, or scene design, route the upstream Studio role first, then `prompt-director` -> `banana-pro`. Do not let the tool trigger bypass the design role.
   - Explicit Kling CLI / 可灵 MCP / `kling-cli` / `@kling-cli` image or video generation request with a complete final prompt -> `prompt-director` -> `kling-cli`; add `tool-integrator` only when install state, OAuth login state, capability, model support, parameters, or MCP availability is unclear.
   - If explicit Kling CLI/MCP generation is bundled with script, storyboard, video/film shot design, camera, edit rhythm, motion, sound, color, scene design, film treatment, poster, PPT/deck/slide, layout, character, product, prop, or scene design, route the upstream Studio role first, then `prompt-director` -> `kling-cli`. Do not let the tool trigger bypass the design role.
   - Explicit 即梦2.0生成 / 即梦生成 / Seedance 2.0 / Ark Seedance video-generation request with a complete final prompt -> `prompt-director` -> `seedance-2-video`; add `tool-integrator` only when capability, parameters, API, key state, or connection state is unclear.
   - If explicit Seedance generation is bundled with script, storyboard, video/film shot design, camera, edit rhythm, motion, sound, color, scene design, or film treatment, route the upstream Studio role first, then `prompt-director` -> `seedance-2-video`. Do not let the tool trigger bypass the design role.
   - If explicit Seedance generation says to follow a storyboard, first route to `production-designer` for Project Asset Graph when continuity assets are not locked, then route to `storyboard-director` for a Storyboard Animatic Sheet or verify an equivalent panel-beat handoff exists. Then package it as a Selected Asset Packet before `prompt-director` writes the storyboard + character + environment + panel beats execution prompt.
   - If explicit Seedance generation uses local image/video files instead of public URLs, insert `url-relay` between `prompt-director` and `seedance-2-video`; use SW media uploader first, then only a confirmed/configured temporary fallback, and stop before real generation if no public URL is available.
   - Explicit URL中转 / 公网URL / 上传参考图 / 上传参考视频 / `@url-relay` -> `url-relay`; if a downstream generation tool is named, return to that tool after the relay URL is ready.
   - Explicit 视觉方案文件 / 视觉导演方案 / Word视觉方案 / DOCX视觉方案 / 分镜视觉方案文件 / `@storyboard-visual-word` with selected images and rationale -> `finishing-producer` -> `storyboard-visual-word`; if storyboard/scene visuals still need creation or selection, route the upstream Studio role first.
6. Final check/risk/delivery readiness -> `review-producer`.
7. Export/package/naming/handoff -> `finishing-producer`.
8. Unspecified visual style, moodboard decision, taste calibration, global aesthetic library use, "SW decide the look", or user-provided visual reference interpretation -> `aesthetic-director`.
9. Project Asset Graph, new storyboard start with unlocked continuity assets, character setting sheet, role reference board, scene setting sheet, production-design board -> `production-designer`; add `asset-producer` only when source/risk/asset priority matters.
10. Integrated storyboard sheet, one-image storyboard board, storyboard contact sheet, or Storyboard Animatic Sheet -> `storyboard-director`; add `cinematographer` only when camera continuity is weak.
11. Image/video/AI prompt request -> `prompt-director`.
12. Audio/music/SFX/voice/mix -> `sound-designer`.
13. Color grade/LUT/shot matching/product color -> `colorist`.
14. Motion graphics/titles/subtitle animation/transitions -> `motion-designer`.
15. Camera/lens/lighting/shot language -> `cinematographer`.
16. Script/voiceover/dialogue/narrative beats -> `scriptwriter`.
17. Film/brand film/treatment/directing intent -> `film-director`.
18. Presentation/PPT/deck/slide outline/storyline/section flow/speaker deck/pitch deck/client-facing proposal/government report/local tourism film proposal/city image film proposal -> `presentation-designer`.
19. Poster copy/headline/CTA or slide wording/title takeaway -> `copywriter`.
20. Poster or presentation layout/grid/type hierarchy -> `layout-designer`.
21. Poster visual/art direction -> `poster-art-director`.
22. Storyboard/shot table -> `storyboard-director`.
23. New or unclear project -> `studio-orchestrator` + `brief-strategist`.
24. Direction request -> `creative-director`.

## Project Type Defaults

Poster:

```text
brief-strategist -> creative-director -> aesthetic-director when look is not locked -> copywriter -> poster-art-director -> layout-designer -> asset-producer -> prompt-director -> review-producer -> finishing-producer
```

Presentation/deck:

```text
brief-strategist -> creative-director -> aesthetic-director when deck look is not locked -> presentation-designer -> copywriter -> layout-designer -> asset-producer -> review-producer -> finishing-producer
```

Video:

```text
brief-strategist -> creative-director -> aesthetic-director when visual language is not locked -> scriptwriter -> production-designer for Project Asset Graph when continuity assets are not locked -> storyboard-director -> cinematographer -> edit-director -> motion-designer -> sound-designer -> colorist -> review-producer -> finishing-producer
```

Film / brand film:

```text
brief-strategist -> creative-director -> film-director -> aesthetic-director when look/world grammar is not locked -> scriptwriter -> production-designer for Project Asset Graph -> cinematographer -> storyboard-director -> edit-director -> sound-designer -> colorist -> review-producer -> finishing-producer
```

Prompt-only:

```text
prompt-director -> tool-integrator if needed -> review-producer if final-use
```

## Support Role Rules

- New project: `studio-orchestrator` + `brief-strategist`.
- Direction after brief: `creative-director` + relevant next production role.
- Visual direction when the look is not locked: primary `aesthetic-director`, support the next production role only if an immediate handoff is needed.
- Poster production: primary `poster-art-director`, support `copywriter` or `layout-designer`.
- Presentation/deck production: primary `presentation-designer` for structure/storyline/client-facing proposal logic; support `research-scout`, `copywriter`, `layout-designer`, `asset-producer`, or `review-producer` depending on request.
- Video production: primary `storyboard-director`, support `scriptwriter` or `cinematographer`; if recurring characters, scenes, props, products, wardrobe, existing footage, or reference assets are not locked, first route `production-designer` for Project Asset Graph.
- Character/scene setting sheet: primary `production-designer`, support `asset-producer` only when source, copyright, or asset priority matters.
- Project Asset Graph: primary `production-designer`, support `asset-producer` only when asset source, copyright, client-provided files, or generation priority matters.
- Integrated storyboard sheet: primary `storyboard-director`, support `cinematographer` only when camera language or continuity needs strengthening.
- Storyboard Animatic Sheet for Seedance/Jimeng: primary `storyboard-director`, support `cinematographer` only when lens/camera path continuity needs strengthening.
- Edit production: primary `edit-director`, support `motion-designer`, `sound-designer`, or `colorist` depending on request.
- Film production: primary depends on stage; support can be `film-director`, `scriptwriter`, `production-designer`, or `cinematographer`.
- Prompt production: primary `prompt-director`, support `tool-integrator` only when specific tool behavior matters.

## Low-Token Mode

Use primary role only unless a support role is required to avoid wrong output.

Output:

```text
Conclusion:
Assumptions:
Recommendation:
One question:
```
