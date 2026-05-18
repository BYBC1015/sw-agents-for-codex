# Auto Assignment Rules

Use these rules to choose the current studio role. The user should not need to manually select roles.

## Inputs

Judge these before every project reply:

- project type: poster, presentation/deck/PPT/slides, video, poster+video, film/brand film, prompt-only, tool, review, revision, unclear
- current stage: intake, research, direction, copy, poster, layout, script, storyboard, camera, edit, motion, sound, color, prompt, review, finishing, change
- user intent: start, continue, create, refine, prompt, tool, check, revise, deliver
- cost mode: normal, low-token, detailed, company delivery
- risk: copyright, brand, platform, tool, missing information
- feature risk: Banana explicit generation, Seedance/即梦 explicit video generation, historical accuracy reminder, project memory

## Priority Routing

0. `@sw_help`, `/sw_help`, feature trigger questions -> use the embedded `sw-help` short answer first; read `Feature_Trigger_Index.md` only for detailed triggers/debug; do not start a project.
1. Historical accuracy:
   - Clear risk but no user confirmation -> add the one-line reminder, continue the normal low-cost route, and do not load `historical-consultant`.
   - User confirms historical checking -> `historical-consultant` first, then affected visual role, then `prompt-director` if generating, then final image QA via `historical-consultant` or `review-producer`.
   - Plain `开启历史检查` applies to the current request/visual chain. `本项目开启历史检查` or `全程开启历史检查` applies to the current conversation/project until closed.
   - `关闭历史检查`, `不用历史检查`, or `恢复普通模式` disables current project-level historical checking. If the setting was saved in `.sw/MEMORY.md`, require explicit memory update/delete to persist the closure.
   - For video, check storyboard first frames, still references, visual assets, generated images, and representative Seedance output frames when available. Do not claim full automated video QA beyond visible frames/stills.
2. Revision/feedback/change -> `change-manager`.
3. New tool, connector, plugin, tool-specific prompt conversion -> `tool-integrator`.
   - Explicit 香蕉 / banana / Banana Pro / Nano Banana / OpenRouter image-generation request with a complete final prompt -> `prompt-director` -> `banana-pro`; add `tool-integrator` only when capability, parameters, API, or connection state is unclear.
   - If explicit Banana generation is bundled with storyboard, video/film shot design, poster, PPT/deck/slide, layout, character, product, prop, or scene design, route the upstream Studio role first, then `prompt-director` -> `banana-pro`. Do not let the tool trigger bypass the design role.
   - Explicit 即梦2.0生成 / 即梦生成 / Seedance 2.0 / Ark Seedance video-generation request with a complete final prompt -> `prompt-director` -> `seedance-2-video`; add `tool-integrator` only when capability, parameters, API, key state, or connection state is unclear.
   - If explicit Seedance generation is bundled with script, storyboard, video/film shot design, camera, edit rhythm, motion, sound, color, scene design, or film treatment, route the upstream Studio role first, then `prompt-director` -> `seedance-2-video`. Do not let the tool trigger bypass the design role.
4. Final check/risk/delivery readiness -> `review-producer`.
5. Export/package/naming/handoff -> `finishing-producer`.
6. Image/video/AI prompt request -> `prompt-director`.
7. Audio/music/SFX/voice/mix -> `sound-designer`.
8. Color grade/LUT/shot matching/product color -> `colorist`.
9. Motion graphics/titles/subtitle animation/transitions -> `motion-designer`.
10. Camera/lens/lighting/shot language -> `cinematographer`.
11. Script/voiceover/dialogue/narrative beats -> `scriptwriter`.
12. Film/brand film/treatment/directing intent -> `film-director`.
13. Presentation/PPT/deck/slide outline/storyline/section flow/speaker deck/pitch deck/client-facing proposal/government report/local tourism film proposal/city image film proposal -> `presentation-designer`.
14. Poster copy/headline/CTA or slide wording/title takeaway -> `copywriter`.
15. Poster or presentation layout/grid/type hierarchy -> `layout-designer`.
16. Poster visual/art direction -> `poster-art-director`.
17. Storyboard/shot table -> `storyboard-director`.
18. New or unclear project -> `studio-orchestrator` + `brief-strategist`.
19. Direction request -> `creative-director`.

## Project Type Defaults

Poster:

```text
brief-strategist -> creative-director -> copywriter -> poster-art-director -> layout-designer -> asset-producer -> prompt-director -> review-producer -> finishing-producer
```

Presentation/deck:

```text
brief-strategist -> creative-director -> presentation-designer -> copywriter -> layout-designer -> asset-producer -> review-producer -> finishing-producer
```

Video:

```text
brief-strategist -> creative-director -> scriptwriter -> storyboard-director -> cinematographer -> edit-director -> motion-designer -> sound-designer -> colorist -> review-producer -> finishing-producer
```

Film / brand film:

```text
brief-strategist -> creative-director -> film-director -> scriptwriter -> production-designer -> cinematographer -> storyboard-director -> edit-director -> sound-designer -> colorist -> review-producer -> finishing-producer
```

Prompt-only:

```text
prompt-director -> tool-integrator if needed -> review-producer if final-use
```

## Support Role Rules

- New project: `studio-orchestrator` + `brief-strategist`.
- Direction after brief: `creative-director` + relevant next production role.
- Poster production: primary `poster-art-director`, support `copywriter` or `layout-designer`.
- Presentation/deck production: primary `presentation-designer` for structure/storyline/client-facing proposal logic; support `research-scout`, `copywriter`, `layout-designer`, `asset-producer`, or `review-producer` depending on request.
- Video production: primary `storyboard-director`, support `scriptwriter` or `cinematographer`.
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
