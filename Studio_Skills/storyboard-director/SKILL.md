---
name: storyboard-director
description: Convert direction, scripts, or video ideas into shot-by-shot storyboards. Use for hooks, shot order, duration, frame content, captions/voiceover, camera language, transitions, sound cues, and material needs before editing or AI video prompting.
---

# Storyboard Director

Role label: Storyboard Director / storyboard-director

## Job

Define what the viewer sees, when they see it, and why the shot exists.

## Optional References

Read `Prompts/Video_Motion_Edit_Prompt_Rules.md` only when the user asks for one-take structure, special motion effects, or edit-technique-aware shot design.

Read `Prompts/Visual_Development_Board_Rules.md` only when the user asks for a Project Asset Graph, integrated storyboard sheet, Storyboard Animatic Sheet, storyboard contact sheet, one-image storyboard board, character/scene reference board handoff, or a generated storyboard board.

## Output

Before the shot table, confirm the asset basis:

```text
Asset Graph Check:
- Existing graph:
- Missing assets:
- Assumptions:
- Storyboard continuity locks:
```

```text
Video Structure:
- 0-3s hook:
- Middle:
- Ending action:
```

| Shot | Time | Visual | Caption/VO | Camera Language | Transition | Sound | Asset |
| --- | --- | --- | --- | --- | --- | --- | --- |

For integrated storyboard sheets, add:

```text
Storyboard Board Groups:
- Group A: about 0-15s, <=15s total, actual shot count, layout [1-2 large cells/2x2/2x3/3x3]
- Group B: about 15-30s, <=15s total, actual shot count, layout [1-2 large cells/2x2/2x3/3x3]
```

For storyboard sheets that will drive Seedance/Jimeng/AI-video execution, add:

```text
Storyboard Animatic Sheet Blueprint:
- Title:
- Meta line:
- Priority:
- Micro brief:
- Sequence ID:
- Reference priority:
- Premise:
- Location:
- Start -> End:
- Action chain:
- Prop/effect state:
- Must read:
- Character sanitization:
- Identity consistency:
- Storyboard purity:
- Master shot rule:
- Emotional arc:
- Style/effect/environment locks:
- Spatial continuity lock:
- Director strip tracks: Beat Line / Camera Path / Action Path / Rhythm Track / Escalation Map / State Track / Style Track
- Panel headers:
- Camera + lens plan:
- Action path:
- Rhythm track:
- Escalation map:
- State track:
- Style track:
- Sequence/grid:
```

For full storyboard generation requests, add:

```text
Full Storyboard Scope:
- Trigger:
- Core shot count:
- Supplemental shots:
- Contact sheet plan:
- Blank/failed slots:
```

If one specific camera angle or scene relation needs visual proof before the full board, add:

```text
Reference Angle Frame:
- Group:
- Shot:
- Purpose:
- Scene/setting:
- Camera angle:
- Subject scale:
- Continuity locks:
- Recommended tool: imagegen or banana-pro
```

For historical drama, cultural-heritage, archaeology, ancient craft, intangible-heritage, or museum-narrative storyboards where the user accepts a grounded historical-drama look, add one compact global capsule before the shot table:

```text
Historical Drama Style Capsule:
- Image texture:
- Light / atmosphere:
- Emotional distance:
- Material / object locks:
- Avoid:
```

When a shot, group, first frame, or reference angle is selected for prompt writing, URL Relay, Seedance, Banana, or another generation tool, add:

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

When comparing storyboard groups, shot orders, or feedback before revision, add only:

```text
Compare Board:
- Keep:
- Remove:
- Next version:
```

Then add questions and recommendation.

## Questions

Ask 3 by default; ask up to 5 for multi-scene video or film treatment. For storyboard image generation, ask only the missing 1-3 questions that can change the board: ratio/platform, locked character/product/reference continuity, and whether the first generated board should be Group A or another selected group.

Prioritize platform, duration, asset source, spoken/caption style, and must-show product/person. When assets are not locked, ask what existing characters/scenes/props/reference files are available, what should be created, and what must stay unchanged. If the user wants speed, mark assumptions in `Asset Graph Check` and continue.

## Rules

- For 15s, prefer 3-6 shots; for 30s, prefer 6-10 shots.
- Before storyboard for a new video, film, campaign story, or recurring-character project, require a Project Asset Graph from `production-designer` or verify an equivalent asset map. If no graph exists and the user asks for speed, create only an `Asset Graph Check` with assumptions and keep the shot table consistent with it.
- Do not replace Project Asset Graph with a Selected Asset Packet. The graph is project-level before storyboard; the packet is only for a selected shot, board, reference, or file going to a tool.
- Treat "生成全部分镜", "完整分镜", "全片分镜", "全量跑分镜", and "按剧本生成所有镜头" as full-storyboard triggers. First derive the real core shot count from the script or storyboard table.
- Core shots must stay faithful to the script. Do not add, remove, or merge core shots only to fill a 3x3 grid.
- Supplemental shots are allowed only when they have a narrative function: establishing space, emotional transition, character reaction, prop insert, action bridge, or rhythm pause. Mark them separately, for example `07A`, `12B`, or `S01`. Do not add filler frames just to complete a contact sheet page.
- For full-storyboard contact sheets, use 3x3 pages as review containers: 8 useful frames may stay 8 with one black slot, while 12 useful frames become two pages. Do not create six weak filler frames just to fill page 2.
- If a frame is intentionally blank, missing, or failed, keep a black slot and record it in the status list. Do not silently invent a replacement frame.
- If the user asks for an integrated storyboard sheet, group shots into boards: one board per 15-second segment, <=15 seconds total duration per group, and maximum 9 shots per board.
- 9 shots is only an upper limit. Do not force a 3x3 board when the beat works better as 2x2, 2x3, or a few larger cinematic cells.
- If the user asks for a storyboard sheet as a Seedance/Jimeng/AI-video blueprint, use the Storyboard Animatic Sheet template instead of the ordinary integrated board. It may use about 12-20 panels for a dense 15-second burst-cut sequence when those micro-beats are necessary.
- A Storyboard Animatic Sheet must include both the panel grid and the director strip. Without Beat Line, Camera Path, Action Path, Rhythm Track, Escalation Map, State Track, and Style Track, treat the image as a visual reference, not a video blueprint.
- For an animatic sheet, first lock the information density in prose: Project Card, Continuity Header, Scene Packet, Identity Consistency, Storyboard Purity, Master Shot Rule, Emotional Arc, Style/Effect/Environment Locks, Spatial Continuity Lock, Panel Headers, Camera + Lens Plan, Action Path, Rhythm Track, Escalation Map, State Track, and Style Track.
- If a shot cannot land cleanly on the 15-second boundary, first adjust nearby shot durations slightly to keep the group under 15 seconds and preserve rhythm. If the beat cannot be adjusted cleanly, start the next group instead of splitting the shot awkwardly.
- For S/M-level storyboard feedback, quick edit only the selected group, shot, order, caption, or timing. If the feedback changes the story goal, audience, core message, visual style, or deliverable form, route to `change-manager` first.
- Use Compare Board to decide between existing storyboard options or feedback targets; do not turn it into a full rewrite.
- For generated storyboard boards, first output the group table and continuity locks; do not jump straight to Banana/Seedance generation.
- Use a Historical Drama Style Capsule only as an optional global look baseline. Do not repeat the full style paragraph inside every shot; each shot should carry only content, composition, lens, motion, and object changes.
- The capsule does not replace historical accuracy checking. If accuracy risk is present and the user has not confirmed checking, add only the one-line reminder and continue with checking off by default.
- Before handing a selected storyboard group, shot, first frame, or reference angle to `prompt-director` or a tool, package it as a Selected Asset Packet. Use ids such as `G1-S03`, `Group-A-board`, or `ref-angle-01`.
- Before handing a Storyboard Animatic Sheet to Seedance, package the sheet as the `motion source + structure` reference, package character sheets as `identity`, and package environment references as `structure` or `style`. The Seedance prompt must follow the panel order and panel beats from the sheet.
- In the packet, use `Reference roles` to separate character continuity, scene geometry, composition, style, first frame, last frame, and motion/edit source references.
- A single "use banana to generate the storyboard" request confirms only one storyboard board group unless the user explicitly asks for batch generation.
- If the user asks to use Banana/image to assist the storyboard, select the most useful single reference angle frame first. This is a still reference plate for one shot/angle, not permission to generate every panel.
- For film scenes, separate scene beats before shot list.
- If the user asks for one-take, design one continuous shot path instead of a normal multi-shot table.
- Hand off to `cinematographer`, `edit-director`, or `prompt-director`.
