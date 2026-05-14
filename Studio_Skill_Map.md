# Studio Skill Map

SW is organized like a small design studio. Each role is a local skill in `Studio_Skills/<skill-id>/SKILL.md`.

## Core Rule

For project work, load only the current needed role files and show the role trace defined in `Studio_Role_Label_Protocol.md`.

## Role Groups

| Group | Roles |
| --- | --- |
| Control | `studio-orchestrator`, `brief-strategist`, `change-manager`, `review-producer`, `finishing-producer` |
| Strategy | `research-scout`, `creative-director`, `presentation-designer`, `copywriter` |
| Poster | `poster-art-director`, `layout-designer`, `asset-producer`, `prompt-director` |
| Presentation | `presentation-designer`, `copywriter`, `layout-designer`, `asset-producer`, `review-producer`, `finishing-producer` |
| Video | `scriptwriter`, `storyboard-director`, `cinematographer`, `edit-director`, `motion-designer`, `sound-designer`, `colorist` |
| Film | `film-director`, `scriptwriter`, `production-designer`, `cinematographer`, `storyboard-director`, `edit-director`, `sound-designer`, `colorist` |
| Tools | `tool-integrator`, `prompt-director`, `asset-producer` |

## Default Chains

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
prompt-director -> tool-integrator (only if needed) -> review-producer
```

Revision:

```text
change-manager -> affected role -> review-producer
```

## Routing Notes

- New project: `studio-orchestrator` + `brief-strategist`.
- Direction request: `creative-director`.
- Poster wording: `copywriter`.
- Poster layout: `layout-designer`.
- Poster visual direction: `poster-art-director`.
- Presentation/deck structure, storyline, slide outline, speaker flow, client-facing proposal logic, government report decks, local tourism film proposal PPTs, and PPT planning: `presentation-designer`.
- Presentation/deck slide copy and title takeaways: `copywriter`; layout/readability: `layout-designer`.
- Presentation/deck final check: `review-producer`; export/package: `finishing-producer`.
- Video script: `scriptwriter`.
- Storyboard: `storyboard-director`.
- Camera/lighting: `cinematographer`.
- Scene/set/product world: `production-designer`.
- Edit rhythm: `edit-director`.
- Motion titles/graphics: `motion-designer`.
- Music/SFX/voice: `sound-designer`.
- Color grade: `colorist`.
- AI prompt: `prompt-director`.
- New tool: `tool-integrator`.
- Final package: `finishing-producer`.
- Risk review: `review-producer`.
