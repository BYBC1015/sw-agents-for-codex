# Production Pipeline Map

This file maps project types to studio skills from concept to delivery after SW has been explicitly activated. Do not use it to auto-start SW from ordinary design-topic wording.

## Cost Principle

Do not run the whole pipeline at once. Use the map to choose the current primary role and next likely handoff.

Default role budget:

- normal project: 1 primary + up to 1 support role
- complex campaign or film: up to 3 roles when needed
- low-token mode: primary role only unless unsafe

## Optional Historical Accuracy Gate

Use only after explicit user confirmation. It is not part of every workflow.

When enabled, insert `historical-consultant` before the affected visual decision and again after image/video generation or final still review when needed:

```text
historical-consultant -> affected visual role -> prompt-director if generating -> explicit tool if any -> historical frame/image QA / review-producer
```

This gate protects final visual output quality: poster key visuals, storyboard first frames, scene/prop/wardrobe references, Banana-generated images, representative Seedance frames/stills when available, and final still images. It does not claim full automated video QA beyond visible frames/stills.

## Poster Full Workflow

```text
studio-orchestrator
-> brief-strategist
-> research-scout (optional)
-> creative-director
-> aesthetic-director (when visual style is not locked)
-> copywriter
-> poster-art-director
-> layout-designer
-> asset-producer
-> Selected Asset Packet (only when a concrete visual is selected for prompt/tool handoff)
-> prompt-director (only for selected AI assets)
-> review-producer
-> finishing-producer
```

Key gates:

- brief locked before directions
- direction locked before layout/prompt detail
- aesthetic profile locked or assumed before expensive key visual generation
- display lettering (hero titles, launch titles, big numerals, glowing/metal/3D/neon title blocks) stays part of the visual system and should preserve image/design effects
- exact information text/logo/QR handled in post-production and QA
- review before delivery

## Poster Quick Edit Workflow

Use this when an existing poster/image is already present and the user asks for a local fix, export variant, title treatment improvement, or reference-based tweak.

```text
poster-art-director or layout-designer
-> prompt-director or image tool only if visual rendering is needed
-> review-producer only for final QA
```

Key gates:

- no full brief/direction restart unless the user changes the goal
- at most one blocking question
- output edited visual/preview first, then no more than three notes
- preserve or improve display lettering effects; do not replace with plain system fonts

## Compare Board / Quick Edit Workflow

Use Compare Board after directions, storyboard groups, or deck structures when the user needs selection or feedback is still abstract.

```text
current primary role
-> Compare Board
-> affected role only if the next version is clear
```

Output only:

```text
Compare Board:
- Keep:
- Remove:
- Next version:
```

For S/M-level quick edits to an existing deck page/outline, storyboard group/shot, edit-plan segment, or prompt:

```text
affected role
-> review-producer only if delivery risk changes
```

Key gates:

- at most one blocking question
- output the revised object first
- preserve locked brief, direction, style, and keep-unchanged items
- route to `change-manager` if feedback changes audience, core message, narrative structure, visual style, project goal, or deliverable form

## Selected Asset Packet Workflow

Use this when a concrete upstream object has been selected and the next step is prompt writing, URL upload, generation, DOCX packaging, or Feishu publishing.

```text
current upstream role or asset-producer
-> Selected Asset Packet
-> prompt-director or selected explicit tool
```

Output only:

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

Key gates:

- package only the selected object, not the whole project
- use stable ids such as `poster-hero-v1`, `deck-p08-visual`, `G1-S03`, `ref-angle-01`, or the generated output id when available
- define reference roles explicitly: character, product, scene, composition, style, texture, color, first frame, last frame, or edit source
- preserve locked items through `prompt-director` and downstream tools
- resolve privacy/cost before public upload, paid generation, long polling, or external publishing

## Presentation / Deck Workflow

```text
studio-orchestrator
-> brief-strategist
-> research-scout (optional)
-> creative-director
-> aesthetic-director (when deck look is not locked)
-> presentation-designer
-> copywriter
-> layout-designer
-> asset-producer
-> review-producer
-> finishing-producer
```

Key gates:

- purpose and audience locked before slide structure
- client decision outcome locked before proposal detail
- visual profile chosen before detailed slide polish or AI imagery
- slide storyline locked before visual polish
- slide roles and title takeaways locked before detailed copy/layout
- client-facing proposal decks may load `presentation-designer` references only when the subject requires them
- use editable placeholders/layouts when PPTX or template handoff matters
- check logic, hierarchy, readability, brand consistency, speaker flow, accessibility, and export format
- AI image prompts are optional and only for selected visuals; use a Selected Asset Packet before handing a slide visual to `prompt-director` or a tool

## Video Full Workflow

```text
studio-orchestrator
-> brief-strategist
-> research-scout (optional)
-> creative-director
-> aesthetic-director (when visual language is not locked)
-> scriptwriter
-> storyboard-director
-> cinematographer
-> production-designer (when scene/world matters)
-> edit-director
-> motion-designer
-> sound-designer
-> colorist
-> asset-producer
-> Selected Asset Packet (only when a concrete shot/reference/media item is selected)
-> prompt-director (only for selected AI shots/assets)
-> review-producer
-> finishing-producer
```

Key gates:

- structure before shot list
- aesthetic profile before storyboard image prompts or reference-frame selection
- shot list before edit plan
- selected AI shots only after specs are locked and represented as a Selected Asset Packet
- when a selected AI video shot uses local reference media, resolve the packet's `Privacy/cost gate`, then use `url-relay` after `prompt-director` and before `seedance-2-video`
- historical accuracy, when enabled, checks storyboard first frames, still visual assets, and representative Seedance frames/stills when available
- sound, motion, and color are separate from storyboard

## Film / Brand Film Workflow

```text
studio-orchestrator
-> brief-strategist
-> research-scout
-> creative-director
-> film-director
-> aesthetic-director (when look/world grammar is not locked)
-> scriptwriter
-> production-designer
-> cinematographer
-> storyboard-director
-> edit-director
-> motion-designer (if graphics/titles needed)
-> sound-designer
-> colorist
-> review-producer
-> finishing-producer
```

Key gates:

- directing intent before script
- aesthetic profile before production-design, cinematography, storyboard boards, or generation prompts
- script/treatment before storyboard
- cinematography and production design before AI video prompts
- historical accuracy, when enabled, locks period/civilization choices before production design and checks still images after generation
- edit before sound/color finalization

## Visual Development Board Workflow

Use this only when the user asks for character setting sheets, scene setting sheets, production-design boards, or one-image storyboard boards.

Character setting sheet:

```text
production-designer
-> asset-producer (only if source/risk/asset priority matters)
-> Selected Asset Packet (for the selected sheet/image)
-> prompt-director (only if generating a prompt/image)
-> banana-pro (only if explicitly requested)
```

Scene setting sheet:

```text
production-designer
-> Selected Asset Packet (for the selected scene sheet/image)
-> prompt-director (only if generating a prompt/image)
-> banana-pro (only if explicitly requested)
```

Integrated storyboard sheet:

```text
storyboard-director
-> cinematographer (only if camera continuity needs help)
-> Selected Asset Packet (for the selected storyboard group)
-> prompt-director (only if generating a prompt/image)
-> banana-pro (only if explicitly requested)
```

Key gates:

- one storyboard board group = one image board
- default group target = one 15-second segment
- each group must stay <=15 seconds total duration
- maximum shots per board = 9, but 9 shots is only the upper limit
- do not force a 3x3 board; choose the board layout from the actual shot count
- if a shot cannot land cleanly at the 15-second boundary, first adjust shot durations slightly; if that breaks the beat, start the next group
- exceeding 15 seconds or 9 shots starts the next group
- generate Group A first unless the user explicitly confirms batch generation
- exact labels, logos, and final typography stay in post-production unless the user accepts model text risk

Reference angle frame:

```text
storyboard-director
-> cinematographer (only if the camera angle, lens height, or spatial relation needs precision)
-> Selected Asset Packet (for the selected shot/angle)
-> prompt-director
-> imagegen or banana-pro (only for the selected still/reference plate)
-> storyboard-director (use the still as a reference for the group board or shot list)
```

Key gates:

- one selected shot/angle only by default
- used for scene geometry, subject scale, lighting direction, or camera position
- not a full storyboard board and not every-shot generation
- batch reference frames need explicit confirmation

## Visual方案文件 / Word Handoff Workflow

Use this only when the user asks for a 视觉方案文件, 视觉导演方案, Word视觉方案, DOCX视觉方案, 分镜视觉方案文件, or client-facing visual bible.

If visuals are already selected:

```text
finishing-producer
-> Selected Asset Packet (for the selected visual set)
-> storyboard-visual-word
```

If storyboard/scene visuals still need to be made:

```text
storyboard-director or production-designer
-> asset-producer (if source/risk/selection matters)
-> Selected Asset Packet (for the selected visual to generate/package)
-> prompt-director (if prompt/image generation is needed)
-> banana-pro or other explicit image tool (only if requested)
-> finishing-producer
-> storyboard-visual-word
```

Key gates:

- it is a downstream packaging step, not a complete storyboard generator
- each scene/group needs one selected image and a Selected Asset Packet before DOCX generation
- formal Word should embed images and hide local paths, raw prompts, generation-result tables, and tool parameters
- internal production appendix with prompts/parameters requires explicit user request

## Prompt-Only Workflow

```text
studio-orchestrator
-> prompt-director
-> tool-integrator (only when tool-specific rules are unknown)
-> review-producer (for final-use prompts)
```

Key gates:

- purpose, subject, ratio/duration, and tool known or assumed
- universal prompt first
- tool-specific conversion second
- if the prompt comes from an upstream selected object, consume the Selected Asset Packet instead of rebriefing the whole project
- local media public URL handoff uses `url-relay` before the downstream tool; use SW media uploader first, then confirmed/configured temporary fallback, and do not submit paid generation if no public URL is available

## Revision Workflow

```text
change-manager
-> affected role
-> review-producer (when delivery risk changes)
```

Key gates:

- classify S/M/L/XL before rewriting
- midstream feedback, screen recordings, meeting notes, chat logs, screenshot annotations, and oral/client comments can become a `Change Delta Packet` before role handoff
- preserve confirmed decisions
- preserve `Keep unchanged` from `Review Delta Packet` or `Change Delta Packet`
- do not batch-regenerate unless confirmed

## Handoff And State

At every stage handoff, preserve:

- current stage
- locked decisions
- assumptions
- risks
- open questions
- next role
- cost lane

Do not replay the full conversation unless the user asks for archive, audit, or company handoff.
