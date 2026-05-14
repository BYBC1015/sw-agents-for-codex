# Studio Skill Dispatch Protocol

This protocol makes each studio skill an executable role, not a decorative label.

## When It Applies

Apply this protocol for all project work:

- brief, research, direction
- presentation, PPT, deck, slides
- poster, layout, copy
- video, film, script, storyboard
- edit, motion, sound, color
- AI image/video prompts
- tool integration
- review, change, finishing

Do not apply it when the user only invokes `/SW_V1.0`, `@SW_V1.0`, or only invokes `@sw_update`.

## Dispatch Steps

Use the Fast Path unless the request needs deeper routing.

Fast Path:

1. Read `SW_Runtime_Index.md`.
2. Read `Cost_Governor.md`.
3. Read `Studio_Role_Label_Protocol.md`.
4. Use the routing summary in `SW_Runtime_Index.md` to choose the obvious role.
5. Read selected `Studio_Skills/<skill-id>/SKILL.md` before producing the deliverable.
6. Show one role trace using the label protocol.
7. Produce only the current role's deliverable, plus questions and recommendation for the next step.

Escalate to full routing only when needed:

- request type or stage is unclear
- route conflicts with current project state
- user asks for full workflow, status, audit, SOP, or company handoff
- complex campaign, film, tool integration, eval/debug, or architecture maintenance
- stage transition depends on a chain decision
- a selected skill references optional files that are relevant to the request

Full routing adds only the necessary files:

1. Read `Auto_Assignment_Rules.md` for route resolution.
2. Read `Production_Pipeline_Map.md` for multi-stage handoff or full pipeline decisions.
3. Read `Studio_Skill_Map.md` for role boundary conflicts.
4. Read `Agent_Skill_Tech_Principles.md` only for architecture updates, complex handoffs, tool integration, or eval/debug work.

## Skill Count

- Default: 1 primary role plus up to 1 support role.
- Low-token mode: primary role only unless a support role is required for safety or tool correctness.
- Complex campaign/film: up to 3 roles when needed.
- Never load all studio roles by default.

## Required Trace

```text
Studio roles: English Title / `skill-id` + English Title / `skill-id` (loaded). Cost lane: production.
```

If only one role is needed:

```text
Studio roles: English Title / `skill-id` (loaded). Cost lane: review/change.
```

If a selected skill file is missing:

```text
Studio roles: English Title / `skill-id` (file missing, fallback rules used). Cost lane: intake.
```

## Questions And Suggestions

- Each invoked project role should include 3 useful questions by default.
- Use up to 5 questions for complex setup, film, campaign, tool risk, or blocked delivery.
- Use at most 1 question in low-token or "you decide" mode.
- Questions must support the next role or unblock execution.
- Every role should include a concise recommendation and next role.

## Handoff Packet

Keep this internally whenever one role hands off to another:

```text
from_role:
to_role:
project_type:
current_stage:
locked_decisions:
assumptions:
deliverable_done:
risks:
open_questions:
next_action:
cost_lane:
```

Show it only when the user asks for status, audit, or handoff notes.

## Agents SDK-Inspired Routing Rules

Use the OpenAI Agents SDK pattern as an internal routing discipline:

- a handoff means the next role owns the next answer
- the handoff reason must be short and tied to the next deliverable
- blocking guardrails run before expensive generation, tool use, uploads, publishing, or irreversible actions
- final output review belongs to the final deliverable/review role, not every intermediate role
- internal trace should record selected role, handoff reason, checked guardrails, and cost lane

Do not over-apply this pattern:

- do not create extra roles just because a handoff is possible
- do not expose debug trace unless the user asks
- do not claim a real SDK trace, guardrail, or agent run unless an actual SDK/tool integration was used
- do not treat role-level guardrails as enough for external tools; tool integrations need their own checks

## No Pretend Calls

Do not say a role was loaded unless its `SKILL.md` file was available and read.

If a historical conversation cannot read the latest local files, tell the user to run `@sw_update` or start a new conversation.

## Token Control

- never paste full skill contents into the answer
- never show the full pipeline unless the user asks for structure
- produce one deliverable type per turn
- high-cost prompts/scripts/batches require confirmation
- prompt-only requests skip full workflow and go directly to `prompt-director`
- preserve locked decisions and pass only the useful handoff packet to the next role
