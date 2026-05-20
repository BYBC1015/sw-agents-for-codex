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

Grouping rules:

- one storyboard group equals one image board
- default group duration is 15 seconds
- one group contains at most 9 shots
- if total shot duration exceeds 15 seconds, start the next group
- if shot count exceeds 9 before 15 seconds, start the next group
- for a 30-second script, usually produce two storyboard boards: Group A 0-15s and Group B 15-30s
- do not batch-generate all groups unless the user confirms; start with one selected group

Recommended board layout:

- 3x3 grid for up to 9 shots, or 2x3 grid for 4-6 shots
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
