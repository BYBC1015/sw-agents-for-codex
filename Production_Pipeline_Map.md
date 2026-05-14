# Production Pipeline Map

This file maps project types to studio skills from concept to delivery.

## Cost Principle

Do not run the whole pipeline at once. Use the map to choose the current primary role and next likely handoff.

Default role budget:

- normal project: 1 primary + up to 1 support role
- complex campaign or film: up to 3 roles when needed
- low-token mode: primary role only unless unsafe

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
- edit before sound/color finalization

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
