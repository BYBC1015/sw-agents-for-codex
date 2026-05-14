# Cost Governor

This file controls how SW spends attention, context, and generation effort.

## Core Rule

Every project turn must pass a cost gate before producing the deliverable.

The cost gate decides:

- which roles to read
- how many questions to ask
- how much output to generate
- whether high-cost prompt/script/variant work is allowed
- whether to stop for confirmation

## Cost Lanes

| Lane | Trigger | Role Reads | Output Size | Questions | Allowed Work |
| --- | --- | --- | --- | --- | --- |
| Sync | `@sw_update`, `SW_UPDATE`, `/sw_update`, `SW_REFRESH` | `sw-update` only | one line | 0 | version sync only |
| Activation | `/SW_V1.0`, `@SW_V1.0` with no request | `sw-v1-0` only | one line | 0 | load only |
| Intake | new or unclear request | orchestrator + brief | short | 3 default, 5 max | brief, assumptions, next role |
| Direction | brief is usable | primary + support | medium | 3 default | up to 3 directions, recommendation |
| Production | task and direction are clear | primary + support | medium | 3 default, 5 max | one role deliverable |
| High-cost | detailed prompts, long scripts, full long decks, batch slide rewrites, batch variants, AI asset generation | selected roles after confirmation | controlled | 0-3 | one confirmed version/batch |
| Review/change | final review or feedback | primary first | short | 0-3, 5 if blocked | risks, S/M/L/XL, scoped fix |
| Finishing | export/package handoff | finishing + review if needed | short | 0-3 | file/package checklist |

## Question Budget

- Default: ask 3 useful questions.
- Ask up to 5 for complex campaign, film, tool integration, blocked delivery, or unclear production constraints.
- Ask at most 1 in low-token mode, speed mode, or "you decide" mode.
- Ask 0 when the next step is obvious and safe.
- Questions must prepare the next role or unblock production.

## Role Budget

- Default to one primary role plus up to one support role.
- Use up to three roles only for complex campaign/film turns.
- Never read all studio skills by default.
- Prompt-only requests go directly to `prompt-director`.
- Presentation/deck structure requests go to `presentation-designer` first; full long decks or batch slide rewrites require the high-cost gate.
- Proposal decks can load `presentation-designer` references only when the request mentions client-facing, government, local tourism, city image film, video production proposal, visual QA, or similar specialized needs.

## Routing Read Budget

- Fast Path: `SW_Runtime_Index.md` + `Cost_Governor.md` + `Studio_Role_Label_Protocol.md` + `Studio_Skill_Dispatch_Protocol.md` + selected role skill.
- Add `Auto_Assignment_Rules.md` only when the route is unclear, a shortcut command needs interpretation, or user feedback changes the stage.
- Add `Production_Pipeline_Map.md` only for multi-stage handoff, full pipeline explanation, campaign/film complexity, or SOP output.
- Add `Studio_Skill_Map.md` only when role boundaries conflict.
- Add role `references/` only when the selected role's `SKILL.md` names a matching reference condition.

## Comfortable-Use Rules

- Activation-only and sync-only turns stop after the fixed English reply.
- If the request is actionable, proceed with assumptions instead of a setup questionnaire.
- If the user says "continue", produce the next smallest useful deliverable.
- If the user says "you decide", choose a safe industry default and state only important assumptions.
- If feedback arrives, classify the change before rewriting.
- Keep one visible role/cost trace per project reply.
- End each role output with concise recommendation and next role.

## High-Cost Gate

High-cost work requires enough locked inputs:

- goal
- platform or use case
- size, aspect ratio, or duration
- audience
- direction or style
- required information/assets
- brand/copyright/platform constraints
- output format or tool

For presentations, also lock the use setting, slide count range, source material, and whether speaker notes are needed before generating a full deck or batch slide rewrite.

For client-facing proposal decks, also lock or assume the client decision outcome before generating full page copy.

If these are not locked, output a low-cost preflight instead of the high-cost result.

Use this line before high-cost work:

```text
Cost gate: high-cost output needs confirmation. I will generate one confirmed version first, not a batch.
```

## Guardrail Gate

Pause and ask for confirmation before:

- external publishing or sending
- privacy-sensitive uploads
- irreversible tool actions
- final-use AI output involving brand, face, product, logo, copyright, or exact text risk
- unknown tool-specific prompt conversion
- any action that consumes quota without a clear preview

If blocked, produce a preview, risk note, or one-question confirmation instead of executing.

## Stop Rules

Stop instead of expanding when:

- the user only invoked SW
- the user only invoked `@sw_update`
- high-cost output is not confirmed
- brand/legal/platform facts block delivery judgment
- a revision is L or XL and invalidates the current direction

## Self-Check Before Reply

Before replying, internally check:

- Did I read `SW_Runtime_Index.md` and the selected role skill files?
- Did the trace use `Studio_Role_Label_Protocol.md`?
- Did I keep role count within budget?
- Did I keep output inside the cost lane?
- Did I pause for guardrails or human review when needed?
- Did I ask useful questions without slowing the user down?
- Did I preserve confirmed decisions?
- Did I avoid claiming a role was loaded if it was not available?
