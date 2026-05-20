# Production Pipeline Map

This file maps project types to studio skills from concept to delivery.

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
-> copywriter
-> poster-art-director
-> layout-designer
-> asset-producer
-> prompt-director (only for selected AI assets)
-> review-producer
-> finishing-producer
```

Key gates:

- brief locked before directions
- direction locked before layout/prompt detail
- exact text/logo/QR handled in post-production
- review before delivery

## Presentation / Deck Workflow

```text
studio-orchestrator
-> brief-strategist
-> research-scout (optional)
-> creative-director
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
- slide storyline locked before visual polish
- slide roles and title takeaways locked before detailed copy/layout
- client-facing proposal decks may load `presentation-designer` references only when the subject requires them
- use editable placeholders/layouts when PPTX or template handoff matters
- check logic, hierarchy, readability, brand consistency, speaker flow, accessibility, and export format
- AI image prompts are optional and only for selected visuals

## Video Full Workflow

```text
studio-orchestrator
-> brief-strategist
-> research-scout (optional)
-> creative-director
-> scriptwriter
-> storyboard-director
-> cinematographer
-> production-designer (when scene/world matters)
-> edit-director
-> motion-designer
-> sound-designer
-> colorist
-> asset-producer
-> prompt-director (only for selected AI shots/assets)
-> review-producer
-> finishing-producer
```

Key gates:

- structure before shot list
- shot list before edit plan
- selected AI shots only after specs are locked
- when a selected AI video shot uses local reference media, use `url-relay` after `prompt-director` and before `seedance-2-video`
- historical accuracy, when enabled, checks storyboard first frames, still visual assets, and representative Seedance frames/stills when available
- sound, motion, and color are separate from storyboard

## Film / Brand Film Workflow

```text
studio-orchestrator
-> brief-strategist
-> research-scout
-> creative-director
-> film-director
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
-> prompt-director (only if generating a prompt/image)
-> banana-pro (only if explicitly requested)
```

Scene setting sheet:

```text
production-designer
-> prompt-director (only if generating a prompt/image)
-> banana-pro (only if explicitly requested)
```

Integrated storyboard sheet:

```text
storyboard-director
-> cinematographer (only if camera continuity needs help)
-> prompt-director (only if generating a prompt/image)
-> banana-pro (only if explicitly requested)
```

Key gates:

- one storyboard board group = one image board
- default group duration = 15 seconds
- maximum shots per board = 9
- exceeding 15 seconds or 9 shots starts the next group
- generate Group A first unless the user explicitly confirms batch generation
- exact labels, logos, and final typography stay in post-production unless the user accepts model text risk

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
- local media public URL handoff uses `url-relay` before the downstream tool; use SW media uploader first, then confirmed/configured temporary fallback, and do not submit paid generation if no public URL is available

## Revision Workflow

```text
change-manager
-> affected role
-> review-producer (when delivery risk changes)
```

Key gates:

- classify S/M/L/XL before rewriting
- preserve confirmed decisions
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
