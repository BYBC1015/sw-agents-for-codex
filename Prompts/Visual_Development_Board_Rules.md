# Visual Development Board Rules

Use this reference only when the user asks for Project Asset Graphs, character sheets, character setting images, scene setting images, production-design boards, one-page storyboard boards, storyboard contact sheets, or Storyboard Animatic Sheets for AI-video execution. Do not load it for normal brief, direction, copy, poster, or simple prompt work.

## Purpose

SW should support five visual-development board types:

1. Project Asset Graph: maps existing and to-create project assets before storyboard so character, scene, prop, wardrobe, product, and source-reference continuity is explicit.
2. Character Setting Sheet: locks a character before storyboard, image generation, or video generation.
3. Scene Setting Sheet: locks a location, set, props, lighting, material language, and color continuity.
4. Integrated Storyboard Sheet: groups sequential shots into one board so the user can review flow and continuity quickly.
5. Storyboard Animatic Sheet: a high-information storyboard blueprint for AI video execution. It combines panel artwork with a director strip so Seedance/Jimeng can follow the storyboard instead of re-inventing coverage.

These boards are production references. They are not final posters and should not ask the image model to create accurate long text. Use clean labels only when useful; exact titles, Chinese copy, logo, and final typography belong in post-production.

## Routing

- Project Asset Graph request, project start with unlocked recurring assets, or storyboard request with unclear asset continuity: `production-designer`; add `asset-producer` only when asset source/risk matters; then `storyboard-director`.
- Character setting request: `production-designer` + `asset-producer` if asset source/risk matters, then `prompt-director` if prompt/image generation is requested.
- Scene setting request: `production-designer`, then `prompt-director` if prompt/image generation is requested.
- Integrated storyboard request: `storyboard-director`; add `cinematographer` only when shot language is weak or cinematic continuity matters; then `prompt-director` if prompt/image generation is requested.
- Storyboard animatic sheet request, or a storyboard intended to drive one Seedance/AI-video sequence: `storyboard-director`; add `cinematographer` only when lens/camera continuity is weak; then `prompt-director` to write the GPT Image 2 / image skill board prompt.
- If the user also asks to generate with Banana Pro, the chain is upstream role -> `prompt-director` -> `banana-pro`.
- If the user also asks to generate video with Seedance, lock or create the selected storyboard animatic sheet first, then `prompt-director` -> `url-relay` if local reference media exists -> `seedance-2-video`.

## Project Asset Graph

Use this when a video, film, campaign story, storyboard, product story, or AI-video project needs recurring asset continuity but the asset system is not locked yet.

It is a low-cost text/board handoff before storyboard. It should not become a full character sheet, scene sheet, or generated visual board unless the user asks or generation needs that expansion.

Low-cost handoff before storyboard:

```text
Project Asset Graph:
- Asset source mode: existing / generate / mixed / unknown
- Existing assets:
- Assets to create:
- Character nodes:
- Scene/location nodes:
- Prop/product/wardrobe nodes:
- Continuity locks:
- Forbidden drift:
- Storyboard handoff:
- Open questions:
```

Rules:

- Ask proactively at project start or when the user asks for a storyboard: what assets already exist, what must be created, and what must stay locked.
- If the user says fast, "you decide", or provides too little context, create a draft graph with assumptions and continue.
- Use stable ids for graph nodes; those ids should appear later in shot tables, storyboard panels, and Selected Asset Packets.
- Use full Character Setting Sheet or Scene Setting Sheet only for nodes that need visual locking or generation.

## Character Setting Sheet

Use this when the project needs recurring characters, actors, mascots, brand characters, stylized figures, film characters, campaign spokespeople, or stable human/creature identity across multiple frames.

Recommended sheet layout:

- white or warm-white studio board, no busy background
- left column: name, alias, role, personality, emotional tone, core theme, must-keep traits
- large full-body hero pose on the left or left-center
- neutral turnarounds: front, back, profile
- expression studies: 4-6 head crops with distinct but controlled expressions
- detail crops: face/hair, hands, clothing fabric, shoes, key prop, accessory, logo-free object detail
- silhouette study: 3-5 small black silhouettes or pose thumbnails
- color palette: 5-8 swatches with restrained labels
- notes area: 3-6 short production notes, not long prose

Prompt constraints:

- keep one consistent face, age, body type, hair, wardrobe, and signature prop
- use full-body neutral views for turnarounds; avoid dynamic poses in the technical views
- avoid crowding the info column into the character body
- avoid exact large readable text; labels may be simple placeholders
- no copied celebrities, copyrighted characters, brand logos, or private likeness without authorization
- output can be "raw clean sheet" first, with optional labels added in post

Low-cost handoff before image generation:

```text
Character Sheet Handoff:
- Character:
- Role:
- Must-keep features:
- Wardrobe:
- Signature prop:
- Expression range:
- Detail crops:
- Color palette:
- Sheet format:
- Risk:
```

## Scene Setting Sheet

Use this when the project needs recurring locations, film worlds, product environments, city/tourism scenes, historical/period spaces, interiors, or stylized sets.

Recommended sheet layout:

- one establishing wide view
- 2-4 secondary angles: entrance, reverse angle, close detail, practical shooting angle
- material/detail crops: wall, floor, window, signage-free props, furniture, texture, weathering
- light study: day/night, warm/cool, practical lights, shadow direction
- prop set: 3-8 key props with source/risk notes
- color/material palette
- optional floor/path diagram only if blocking matters

Prompt constraints:

- lock location geometry, material, weather, time of day, and color temperature
- avoid invented brand signage and unreadable fake text
- keep spaces usable for future storyboard panels; do not overdecorate
- if historical accuracy is enabled, include period/civilization constraints and check the generated result after output

Low-cost handoff before image generation:

```text
Scene Sheet Handoff:
- Location:
- Function in story:
- Establishing view:
- Secondary angles:
- Key props:
- Material/light:
- Palette:
- Continuity locks:
- Risk:
```

## Integrated Storyboard Sheet

Use this when the user wants a one-image storyboard, a contact-sheet storyboard, or a reviewable storyboard board instead of separate generated frames.

If multiple storyboard groups, board layouts, or shot-order options need selection before image prompting, use a lightweight Compare Board first:

```text
Compare Board:
- Keep:
- Remove:
- Next version:
```

Do not turn Compare Board into another storyboard table or batch board prompt. It only decides what survives into the next selected group.

## Storyboard Animatic Sheet

Use this when the storyboard will become the source of truth for Seedance/Jimeng/AI-video execution, especially for a 10-20 second sequence where one video-generation task must imply multiple cuts, burst inserts, choreography, spatial continuity, or a strong final payoff.

This is stricter than an ordinary integrated storyboard sheet. The output should be a designed one-image production blueprint, usually generated through GPT Image 2 / the default image skill. The sheet must carry enough information that the later video prompt can say "follow the storyboard exactly" without re-explaining the whole world.

### Scope

- Default dense-sequence scope: 15 seconds, 16:9, about 12-20 panels when the concept needs burst cuts or micro-actions.
- Use the real shot/beat count. Do not force 20 panels when the sequence is simple, and do not force 9 panels when a dense animatic needs more micro-beats.
- Ordinary review boards still use the normal integrated storyboard rules. Use this animatic template only when the board is intended to drive AI-video execution or the user explicitly asks for this high-density storyboard-sheet style.
- The storyboard image may show panel labels, shot tags, and director-strip labels outside the panel artwork. Do not rely on accurate long body text; the text blocks are production-notation placeholders.

### Required Information Density

Before writing the image prompt, prepare these fields:

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
- Style lock:
- Effect lock:
- Environment lock:
- Spatial continuity lock:
- Director strip tracks:
- Panel headers:
- Camera + lens plan:
- Action path:
- Rhythm track:
- Escalation map:
- State track:
- Style track:
- Sequence/grid:
```

### GPT Image 2 / Image Skill Board Prompt Shape

Use this structure when converting the blueprint into the board prompt:

```text
Create a 16:9 image.

[PROJECT CARD]
Create a compact designed masthead, not a table.
TITLE:
META LINE:
PRIORITY:
MICRO BRIEF:

[CONTINUITY HEADER]
SEQUENCE ID:
REFERENCE PRIORITY: [reference 1 controls identity / reference 2 controls environment geometry / storyboard controls staging, motion, geography, continuity, cut rhythm, and effect logic.]

[SCENE PACKET]
PREMISE:
LOCATION:
START -> END:
ACTION CHAIN:
PROP / EFFECT STATE:
MUST READ:

[CHARACTER SANITIZATION]
C1:
Remove contradictory traits, invisible psychology, excessive costume detail, and backstory that cannot appear in a panel.

[IDENTITY CONSISTENCY]
[State what the character/product reference controls, what the storyboard controls, and what must not change.]

[STORYBOARD PURITY]
Panel images are visual-only rough sketches or production panels. Put panel numbers, beat names, and lens tags in the header strip outside each panel image. No captions, subtitles, logos, watermarks, UI, ghost poses, duplicate bodies, or technical overlays inside panels.

[MASTER SHOT RULE]
P01 shows the full playable geography and stable travel direction.

[EMOTIONAL ARC]
[State the visible emotional/energy progression through stance, gaze, action, light, rhythm, or final stillness.]

[STYLE LOCKS]
STYLE LOCK:
EFFECT LOCK:
ENVIRONMENT LOCK:

[SPATIAL CONTINUITY LOCK]
[List the wide/anchor panels that share the same layout, screen direction, foreground/background, and allowed changes.]

[DIRECTOR STRIP]
Bottom animatic track board aligned to panel columns. Tracks: BEAT LINE, CAMERA PATH, ACTION PATH, RHYTHM TRACK, ESCALATION MAP, STATE TRACK, STYLE TRACK. Use shot chips, thin lines, rhythm blocks, small intensity bars, one-to-three-word labels. No seconds or timestamps.
RHYTHM TRACK format: `RHY P##: [hold|slow reveal|build|burst|impact|pause|recover|final hit] / [short block|medium block|long block] / [clean beat|match beat|smash beat|held beat|whip beat]`.
ESCALATION MAP format: `ESC P##: [L1 calm|L2 tension|L3 rise|L4 surge|L5 peak] / [flat|rise|spike|drop|release|unresolved]`.
PANEL HEADERS:
CAMERA + LENS PLAN:
ACTION PATH:
RHYTHM TRACK:
ESCALATION MAP:
STATE TRACK:
STYLE TRACK:

[SEQUENCE]
Grid: [panel count and layout]; panel artwork stays [chosen board style] while the director strip makes the sequence readable through camera path, action path, rhythm, escalation, state, and style tracks.
```

### Director Strip Requirements

The director strip is mandatory for this template. It turns a static storyboard into an animatic control layer:

- `BEAT LINE`: the narrative job of each panel.
- `CAMERA PATH`: camera direction, hold/push/whip/orbit/track relation, or stable camera state.
- `ACTION PATH`: subject or effect trajectory across the panel sequence.
- `RHYTHM TRACK`: hold/build/burst/pause/impact/final-hit density using short/medium/long blocks.
- `ESCALATION MAP`: intensity curve from calm to peak, drop, release, or unresolved state.
- `STATE TRACK`: what the scene is currently doing, such as still, ignition, build, fragment, pause, decision, impact, awe.
- `STYLE TRACK`: per-panel visual grammar, such as grounded, spark, sweep, detail, crash, intimate, halo, slice, ripple.

### Handoff To Seedance

After the animatic sheet is generated or selected, package it before Seedance:

```text
Selected Asset Packet:
- Object ID: [sequence-id]-animatic-sheet
- Source stage: Storyboard Animatic Sheet
- Asset type: storyboard blueprint / AI-video motion source
- Purpose: Seedance/Jimeng sequence execution
- Selected input: storyboard sheet image + optional character sheet + optional environment reference
- Reference roles: storyboard sheet = motion source + structure; character sheet = identity; environment reference = structure/style
- Locked items: panel order, panel beats, character identity, environment geography, effect logic, final payoff
- Avoid: alternative coverage, extra characters, redesigned subject, new location, copied labels/text, logo/watermark
- Next tool: prompt-director -> seedance-2-video
- Privacy/cost gate:
```

## Full Storyboard Generation

Use this when the user explicitly asks for "生成全部分镜", "完整分镜", "全片分镜", "全量跑分镜", or "按剧本生成所有镜头".

Rules:

- First confirm the real core shot count from the script or storyboard table.
- Generate according to the real story structure. Do not force the story to become 9, 18, 27, or another multiple of 9.
- Supplemental shots are allowed when they improve storytelling: establishing space, emotional transition, character reaction, prop insert, action bridge, or rhythm pause.
- Supplemental shots must be labeled separately, such as `07A`, `12B`, or `S01`, and listed in a supplemental-shot table.
- Do not add weak filler images only to fill a 3x3 page.
- Full storyboard frames remain one shot per image. Contact sheets are only review pages.
- Contact sheets use 3x3 pages by default. Empty slots stay black.
- 8 useful frames may become 9 only if the extra frame has a clear narrative job; otherwise the 9th slot stays black.
- 12 useful frames become two 3x3 pages: page 1 has shots 1-9, page 2 has shots 10-12 plus black slots unless useful supplemental shots are justified.
- Missing or failed frames also use black slots and must be listed as `missing` or `failed`.

Required status outputs:

```text
Full Storyboard Status:
- Core shots:
- Supplemental shots:
- Generated frames:
- Missing/failed:
- Contact sheets:
```

## Reference Angle Frame

Use this when the storyboard needs one specific scene angle, camera position, or spatial relation clarified before generating a full storyboard board.

Rules:

- A reference angle frame is one still image for one selected shot or angle, not a full storyboard.
- Use it to lock scene geometry, character scale, prop placement, lens height, foreground/background relationship, lighting direction, or camera angle.
- It can be generated with Banana Pro or a generic image tool after `storyboard-director` and, when useful, `cinematographer` define the shot intent.
- It returns to storyboard planning as a reference plate for the integrated storyboard sheet, Seedance first frame, or later visual方案文件.
- Do not generate reference frames for every shot unless the user explicitly confirms batch generation.

Low-cost handoff before image generation:

```text
Reference Angle Frame Handoff:
- Group:
- Shot:
- Purpose:
- Scene/setting:
- Camera angle:
- Lens/height:
- Subject scale:
- Foreground/background:
- Lighting/palette:
- Continuity locks:
- Tool:
```

Grouping rules:

- one storyboard group equals one image board
- default group target is a 15-second segment
- one group duration must not exceed 15 seconds
- one group contains at most 9 shots, but 9 shots is only the upper limit, not a goal
- do not force a 3x3 board; choose the layout from the actual shot count
- if a shot lands awkwardly across the 15-second boundary, first adjust nearby shot durations slightly to keep the group natural and under 15 seconds
- if the story beat cannot be adjusted cleanly, start the next group instead of splitting the shot awkwardly
- if shot count exceeds 9 before 15 seconds, start the next group
- for a 30-second script, usually produce two storyboard boards: Group A about 0-15s and Group B about 15-30s, with exact shot timing allowed to shift slightly for rhythm
- do not batch-generate all groups unless the user confirms; start with one selected group

Recommended board layout:

- 1-2 shots: large cinematic cells or split-screen board
- 3-4 shots: 2x2 board
- 5-6 shots: 2x3 board
- 7-9 shots: 3x3 board
- consistent character, wardrobe, location, time of day, color, and prop continuity across panels
- each panel has shot number, short duration, shot size, camera angle, and action note
- arrows or small motion marks may indicate camera/subject movement
- use rough sketch, monochrome board, or clean production sketch when the purpose is planning
- use more polished ad-film stills only when the user asks for presentation-ready storyboard art

Storyboard table before image prompt:

```text
Storyboard Board Group:
- Group:
- Time range:
- Total duration:
- Board layout:
- Continuity locks:

| Shot | Time | Duration | Frame | Action | Camera | Transition | Note |
| --- | --- | --- | --- | --- | --- | --- | --- |
```

Before generating a storyboard image, ask only the missing questions that can change the board:

- If duration or platform/ratio is unknown, ask 1 question.
- If character, product, or reference continuity is missing, ask 1-2 questions.
- If the user says "you decide" or "fast", make practical defaults and state them briefly.
- Do not ask about every panel when the script already implies the flow.

Integrated storyboard image prompt must include:

- board type: integrated storyboard sheet / contact sheet / 3x3 storyboard board
- exact number of panels
- shot numbers and short labels as visual placeholders only
- each panel's frame content and camera language
- continuity locks: character, clothing, prop, environment, palette, lighting
- board style: rough pencil, grayscale concept board, clean ad storyboard, or polished production still board
- negative constraints: no extra panels, no inconsistent character, no wrong product, no large unreadable text, no logo, no watermark

## Cost And Comfort Rules

- Planning a character sheet, scene sheet, or storyboard board is medium-cost.
- Generating a detailed image prompt for one board is high-cost but allowed after the board handoff is locked.
- Real Banana/Seedance generation is a tool high-cost step and needs explicit generation wording or confirmation.
- "Use banana to generate the character sheet" confirms one draft sheet only.
- "Use banana to generate the storyboard" confirms one storyboard group only, not all groups.
- For long scripts, produce the group table first and ask which group to generate.
