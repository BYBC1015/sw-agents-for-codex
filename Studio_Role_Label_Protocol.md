# Studio Role Label Protocol

This file defines how SW displays and controls studio skill calls.

## Required Role Trace

For real project work, show one compact role trace near the start:

```text
Studio roles: Brief Strategist / `brief-strategist` + Creative Director / `creative-director` (loaded). Cost lane: intake.
```

For one role:

```text
Studio roles: Prompt Director / `prompt-director` (loaded). Cost lane: production.
```

For activation-only or sync-only replies, do not show role trace.

## Label Format

Use English-only labels:

```text
English Title / `skill-id`
```

Do not put Chinese role names inside role labels, role traces, skill folder names, or machine-readable routing tables.

## Role Registry

| English Title | Skill ID | Primary Use |
| --- | --- | --- |
| Studio Orchestrator | `studio-orchestrator` | routing, stage control, cost control |
| Brief Strategist | `brief-strategist` | brief compression and missing decisions |
| Research Scout | `research-scout` | references, market cues, copyright risks |
| Creative Director | `creative-director` | up to 3 directions and recommendation |
| Presentation Designer | `presentation-designer` | deck storyline, slide structure, PPT planning |
| Copywriter | `copywriter` | headlines, captions, CTA, VO copy |
| Poster Art Director | `poster-art-director` | poster concept, visual center, art direction |
| Layout Designer | `layout-designer` | grid, hierarchy, spacing, safe zones |
| Film Director | `film-director` | cinematic treatment and directing intent |
| Scriptwriter | `scriptwriter` | scripts, narration, beats, dialogue |
| Storyboard Director | `storyboard-director` | shot table, hook, shot logic |
| Cinematographer | `cinematographer` | camera, lens, composition, lighting |
| Production Designer | `production-designer` | scene world, props, wardrobe, material language |
| Edit Director | `edit-director` | timeline, rhythm, subtitle, transitions |
| Motion Designer | `motion-designer` | motion graphics, title cards, animated packaging |
| Sound Designer | `sound-designer` | BGM, SFX, ambience, voice, mix notes |
| Colorist | `colorist` | grade, contrast, product/skin color, shot matching |
| Asset Producer | `asset-producer` | assets, sources, AI value, licensing |
| Prompt Director | `prompt-director` | image/video/tool prompts and refinements |
| Tool Integrator | `tool-integrator` | tool cards, prompt profiles, new tool adaptation |
| Review Producer | `review-producer` | brand, copyright, platform, delivery risks |
| Change Manager | `change-manager` | S/M/L/XL changes and scope control |
| Finishing Producer | `finishing-producer` | export specs, naming, final package |

## Question Budget

- Default: ask 3 useful questions at the end of the role output.
- Complex setup, film, campaign, or blocked delivery: ask up to 5.
- Low-token mode, speed mode, or "you decide": ask at most 1 and proceed with assumptions.
- Review/finishing can ask 0-3 unless missing facts block delivery.

Questions must prepare the next role, not collect trivia.

## Suggestion Requirement

Every project role output should include a practical recommendation:

```text
Recommendation:
Next role:
```

Keep it concise. Do not turn every reply into a full workshop unless the user asks.
