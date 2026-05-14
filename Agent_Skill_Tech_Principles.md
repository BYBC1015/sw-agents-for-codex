# Agent Skill Tech Principles

This file captures agent/skill architecture practices adopted by SW.

Use it when updating SW architecture, debugging role routing, adding tools, writing evals, or handling complex handoffs.

## Adopted Practices

### 1. Progressive Disclosure

Load context in layers:

1. fixed invocation reply
2. compact runtime index
3. cost gate and role label rules
4. selected role skill only
5. references, tool profiles, and prompt specs only when needed

Do not load every role, pipeline, prompt library, or tool profile by default.

### 2. Handoff Packet

When one role hands off to another, keep a compact packet internally:

```text
handoff:
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

Only show the packet if the user asks for status, audit, or handoff notes.

### 3. Role Ownership

Use a handoff only when the next role should own the next answer. Otherwise keep the support role in the background.

Rules:

- split roles only when instructions, tools, risk, or output format differ
- keep handoff descriptions short and concrete
- preserve locked decisions when switching roles
- do not let multiple roles rewrite the same deliverable in one turn

### 4. Guardrails And Human Review

Pause for user confirmation before:

- high-cost generation
- publishing or external posting
- privacy-sensitive uploads
- irreversible tool actions
- final-use AI images/video with brand, face, product, logo, or copyright risk
- tool-specific prompt conversion when the tool behavior is unknown

When blocked, output a low-cost preflight instead of proceeding.

### 5. State And Continuation

Carry forward only the useful project state:

- last_role
- current_stage
- locked_decisions
- assumptions
- pending_questions
- pending_approvals
- next_role
- cost_lane

Do not replay or summarize the entire conversation unless the user asks for archive, audit, or company handoff.

### 6. Observability Trace

Every project answer should have exactly one visible role trace:

```text
Studio roles: English Title / `skill-id` + English Title / `skill-id` (loaded). Cost lane: production.
```

For deeper debugging, use a hidden/internal trace:

```text
route_reason:
loaded_files:
handoff_packet:
guardrails_checked:
cost_decision:
```

Do not expose debug trace by default.

### 7. Eval Loop

Before major SW updates, test at least:

- poster brief -> directions -> poster plan
- presentation/PPT brief -> deck structure -> review
- short video brief -> structure -> storyboard -> edit plan
- prompt-only request -> precise image/video prompt
- revision feedback -> S/M/L/XL decision
- tool-specific request -> tool card before tool prompt

Track:

- did the right role load
- did the trace use English-only labels
- did questions stay within 3/5/1 budget
- did high-cost work pause correctly
- was the output useful enough for the next role

Maintenance note for Windows:

- Run validation with UTF-8 enabled, e.g. set `PYTHONUTF8=1`, because the validator may otherwise read UTF-8 skill files using the system code page and produce false failures.
- Treat default-codepage decode errors as validation-environment issues unless UTF-8 validation also fails.
- Check active startup/sync docs, user-level skills, plugin skills, and `plugin.json` after every version bump.

### 8. Script And Tool Design

If SW later adds deterministic helper scripts:

- avoid interactive prompts
- provide `--help`
- use structured output such as JSON/CSV
- support dry-run for risky actions
- make retries idempotent
- keep output bounded or write large output to files

Creative judgment should stay in role skills; scripts are only for repeatable validation, conversion, extraction, or packaging.
