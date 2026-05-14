# Token Budget

This file supports `Cost_Governor.md`. `Cost_Governor.md` decides the runtime cost lane; this file records the budget logic and audit table.

## Runtime Cost Lanes

| Lane | Use When | Default Output | High-Cost Allowed |
| --- | --- | --- | --- |
| Sync | `@sw_update`, `SW_UPDATE`, `/sw_update`, `SW_REFRESH` | one English sync line | no |
| Activation | `/SW_V1.0`, `@SW_V1.0` with no project request | one English loaded line | no |
| Intake | new or unclear request | brief, assumptions, max 3 questions | no |
| Direction | brief is usable | up to 3 directions | no detailed prompt batch |
| Production | task and direction are clear | one deliverable type | only if confirmed |
| High-cost | detailed prompts, long scripts, full long decks, batch slide rewrites, batch variants, AI asset generation | one confirmed batch | yes, after gate |
| Review/change | final check or revision | concise risk/change decision | no batch rewrite before classification |

## Question Budget

- Default role output: 3 useful questions.
- Complex campaign, film, tool-risk, or blocked-delivery output: up to 5 questions.
- Low-token, speed, "you decide", or "few questions" output: at most 1 question.
- Questions should prepare the next role, not collect background trivia.

## Role Budget

- Default: 1 primary role plus up to 1 support role.
- Complex campaign/film: up to 3 roles only when needed.
- Prompt-only: go directly to `prompt-director`.
- Never load all roles by default.

## High-Cost Tasks

Treat these as high-cost:

- detailed image generation prompts for multiple assets
- detailed video prompts for multiple shots
- full long-form scripts
- full 20+ slide deck plans, detailed speaker notes, or batch slide rewrites
- batch variants
- full campaign expansion
- broad rewrite after feedback
- tool-specific prompt conversion when tool behavior is uncertain

PPT/deck structure from `presentation-designer` stays low-to-medium by default; only full long decks, detailed speaker notes, broad research, PPTX generation, preview export, or batch slide rewrites become high-cost.

## Required Gate Before High-Cost Work

Before high-cost work, confirm:

- goal
- platform or use case
- size, aspect ratio, or duration
- audience
- direction or style
- required information/assets
- brand, copyright, and platform constraints
- output format

For PPT/deck work, also confirm the use setting, client decision outcome, slide count range, source material, and whether speaker notes are needed before full-deck generation.

If not confirmed, output a low-cost preflight instead.

## Budget Audit Table

Use this table only when the user asks to save, audit, or review cost decisions.

| Date | Stage | Task | Cost Lane | Why Worth It | Inputs Confirmed | Result | Next Optimization |
| --- | --- | --- | --- | --- | --- | --- | --- |
| YYYY-MM-DD | Direction | Generate up to 3 directions | Direction | Locks direction before production | Partial |  |  |

## Low-Cost Reply Shape

When the user asks for low-token mode, fewer questions, faster progress, or the task is early-stage:

```text
Studio roles: `primary-skill` (loaded). Cost lane: intake.
Conclusion:
Assumptions:
Next step:
One question:
```

## Stop Rules

Stop before expanding when:

- direction is not locked
- required specs are missing
- the user only asked for sync or activation
- the next output would be high-cost
- the change is L or XL
- the requested AI asset may create copyright, brand, logo, text, face, product, or platform risk
