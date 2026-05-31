# Visual Development Board Rules

Use this reference only when the user asks for character sheets, character setting images, scene setting images, production-design boards, one-page storyboard boards, or storyboard contact sheets. Do not load it for normal brief, direction, copy, poster, or simple prompt work.

## Purpose

SW should support three visual-development board types:

1. Character Setting Sheet: locks a character before storyboard, image generation, or video generation.
2. Scene Setting Sheet: locks a location, set, props, lighting, material language, and color continuity.
3. Integrated Storyboard Sheet: groups sequential shots into one board so the user can review flow and continuity quickly.

These boards are production references. They are not final posters and should not ask the image model to create accurate long text. Use clean labels only when useful; exact titles, Chinese copy, logo, and final typography belong in post-production.

## Routing

- Character setting request: `production-designer` + `asset-producer` if asset source/risk matters, then `prompt-director` if prompt/image generation is requested.
- Scene setting request: `production-designer`, then `prompt-director` if prompt/image generation is requested.
- Integrated storyboard request: `storyboard-director`; add `cinematographer` only when shot language is weak or cinematic continuity matters; then `prompt-director` if prompt/image generation is requested.
- If the user also asks to generate with Banana Pro, the chain is upstream role -> `prompt-director` -> `banana-pro`.
- If the user also asks to generate video with Seedance, lock the selected storyboard group first, then `prompt-director` -> `url-relay` if local reference media exists -> `seedance-2-video`.

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
