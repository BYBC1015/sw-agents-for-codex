# Token Budget

This file supports `Cost_Governor.md`. `Cost_Governor.md` decides the runtime cost lane; this file records the budget logic and audit table.

## Runtime Cost Lanes

| Lane | Use When | Default Output | High-Cost Allowed |
| --- | --- | --- | --- |
| Sync | `@sw_update`, `SW_UPDATE`, `/sw_update`, `SW_REFRESH` | one English sync line | no |
| Rescue | `/sw-rescue`, `@sw_rescue`, `SW_RESCUE`, `SW_REPAIR`, `SW_FORCE_UPDATE` | one English rescue line | no |
| Activation | `/SW_V1.0`, `@SW_V1.0` with no project request | one English loaded line | no |
| Intake | new or unclear request | brief, assumptions, max 3 questions | no |
| Direction | brief is usable | up to 3 directions | no detailed prompt batch |
| Production | task and direction are clear | one deliverable type | only if confirmed |
| High-cost | detailed prompts, long scripts, full long decks, batch slide rewrites, batch variants, AI asset generation | one confirmed batch | yes, after gate |
| Review/change | final check or revision | concise risk/change decision | no batch rewrite before classification |
| Memory | major durable confirmation or explicit remember/save request | one short suggestion or 1-3 bullets | no |
| Feature help | `@sw_help`, `/sw_help`, trigger-word questions | embedded short help first; detailed trigger index only on request | no |
| Historical reminder | clear historical accuracy risk without user confirmation | one reminder line | no |
| Maintenance-lite | routine SW maintenance, quick optimize, wake/sync check | short check result | no |
| Maintenance-full | publish/upload, deep regression, unresolved failure | focused regression report | no generation |

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
- real Banana Pro image generation or real Seedance/即梦2.0 video generation
- URL Relay upload when it involves private/client assets or directly precedes real paid generation

Project memory reads and one-line memory suggestions are low-cost. Writing to `.sw/MEMORY.md` requires explicit user approval and should append only 1-3 concise bullets.

PPT/deck structure from `presentation-designer` stays low-to-medium by default; only full long decks, detailed speaker notes, broad research, PPTX generation, preview export, or batch slide rewrites become high-cost.

Historical accuracy trigger scanning is low-cost and current-message only. Do not load historical references, browse, or run `historical-consultant` until the user confirms. Once enabled, strict period research, source notes, and post-generation image QA can become medium-to-high cost depending on depth.

Seedance/即梦2.0 dry-run is low-cost because it only validates a sanitized payload. Real generation is high-cost because it can consume quota, require public image URLs, and wait in a long queue. Default to one selected clip/shot at `720p`; batch shots, multiple ratios, `1080p`, and long polling need explicit confirmation.

URL Relay itself does not consume model tokens. Treat it as low-cost for public/test files, but require an upload/privacy guardrail for client-sensitive, face, unreleased product, or brand assets. If the SW relay is unreachable or server-failing, report the outage and use only an already-public URL or confirmed/configured temporary fallback before paid generation; config/auth errors do not fallback.

Help and wake-up hot paths are zero-project-read by default: `@sw_help` uses its embedded short answer, activation-only uses one fixed loaded line, and sync-only uses one fixed sync line. Detailed indexes/logs load only for explicit details or diagnostics.

Image aesthetic, Oscar/classic-film, and detailed video-motion references are progressive-disclosure files. They are not loaded during normal routing. Load them only when the user asks for stronger image taste, anti-AI look, filmic references, one-take/bullet-time/hero-shot language, edit techniques, or execution-level AI video prompts.

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

## Historical Accuracy Gate

- Style-only phrases such as 国风, 古风, 唐风, 宋韵, 东方美学, 敦煌感, 新中式, or 仙侠感 do not trigger historical checking.
- Clear risk without confirmation produces only: `检测到历史准确性风险。是否开启历史准确性检查？默认不开启。`
- After confirmation, historical checking must include final visual output/image QA when images are generated or reviewed.
- Video-stage checking covers still frames, storyboard images, references, visual assets, and representative Seedance output frames when available. Do not claim full automated video QA beyond visible frames/stills.
