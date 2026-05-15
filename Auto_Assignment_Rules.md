# Auto Assignment Rules

Use these rules to choose the current studio role. The user should not need to manually select roles.

## Inputs

Judge these before every project reply:

- project type: poster, presentation/deck/PPT/slides, video, poster+video, film/brand film, prompt-only, tool, review, revision, unclear
- current stage: intake, research, direction, copy, poster, layout, script, storyboard, camera, edit, motion, sound, color, prompt, review, finishing, change
- user intent: start, continue, create, refine, prompt, tool, check, revise, deliver
- cost mode: normal, low-token, detailed, company delivery
- risk: copyright, brand, platform, tool, missing information

## Priority Routing

1. Revision/feedback/change -> `change-manager`.
2. New tool, connector, plugin, tool-specific prompt conversion -> `tool-integrator`.
   - Explicit 香蕉 / banana / Banana Pro / Nano Banana / OpenRouter image-generation request with a complete final prompt -> `prompt-director` -> `banana-pro`; add `tool-integrator` only when capability, parameters, API, or connection state is unclear.
   - If explicit Banana generation is bundled with storyboard, video/film shot design, poster, PPT/deck/slide, layout, character, product, prop, or scene design, route the upstream Studio role first, then `prompt-director` -> `banana-pro`. Do not let the tool trigger bypass the design role.
3. Final check/risk/delivery readiness -> `review-producer`.
4. Export/package/naming/handoff -> `finishing-producer`.
5. Image/video/AI prompt request -> `prompt-director`.
6. Audio/music/SFX/voice/mix -> `sound-designer`.
7. Color grade/LUT/shot matching/product color -> `colorist`.
8. Motion graphics/titles/subtitle animation/transitions -> `motion-designer`.
9. Camera/lens/lighting/shot language -> `cinematographer`.
10. Script/voiceover/dialogue/narrative beats -> `scriptwriter`.
11. Film/brand film/treatment/directing intent -> `film-director`.
12. Presentation/PPT/deck/slide outline/storyline/section flow/speaker deck/pitch deck/client-facing proposal/government report/local tourism film proposal/city image film proposal -> `presentation-designer`.
13. Poster copy/headline/CTA or slide wording/title takeaway -> `copywriter`.
14. Poster or presentation layout/grid/type hierarchy -> `layout-designer`.
15. Poster visual/art direction -> `poster-art-director`.
16. Storyboard/shot table -> `storyboard-director`.
17. New or unclear project -> `studio-orchestrator` + `brief-strategist`.
18. Direction request -> `creative-director`.

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
