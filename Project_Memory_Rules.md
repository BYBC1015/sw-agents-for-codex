# Project Memory Rules

This file defines SW's lightweight local memory layer for long-running project folders.

## Purpose

SW is the general design studio framework. A long-running client or internal project may add a small `.sw/` folder in that project folder so every new conversation can reuse stable project context without copying the whole SW framework.

## Project Folder Layout

Recommended local memory pack:

```text
.sw/
  PROJECT.md
  RULES.md
  MEMORY.md
  CHANGELOG.md
  ASSETS.md
```

## File Roles

- `PROJECT.md`: stable project identity, client, target, audience, channels, deadlines, and default assumptions.
- `RULES.md`: project-specific constraints, brand tone, style boundaries, review standards, and forbidden directions.
- `MEMORY.md`: confirmed decisions only. Keep it short and durable.
- `CHANGELOG.md`: important project-level changes, not every chat turn.
- `ASSETS.md`: asset sources, logo/font/material notes, license/copyright status, and sensitive material warnings.

## Read Order

For a real project turn, use this priority:

1. current user request
2. `.sw/MEMORY.md`
3. `.sw/RULES.md`
4. `.sw/PROJECT.md`
5. global SW rules

Only read `.sw/CHANGELOG.md` or `.sw/ASSETS.md` when the task involves revisions, asset use, copyright, delivery, or audit.

If `.sw/` is missing, continue with normal SW behavior and do not ask the user to create it unless the project is long-running or the user asks for persistent project memory.

## What Counts As Major Confirmation

Suggest writing to `MEMORY.md` only when the user confirms durable information:

- project goal, audience, channel, format, or deadline
- brand tone, style direction, visual identity, or design禁区
- locked creative direction, storyline, storyboard structure, or key visual
- character, product, prop, scene, or continuity constraints
- client preference, approval rule, review standard, or compliance constraint
- asset source, copyright rule, logo/font/material handling
- tool setting that should repeat across future conversations

Do not suggest memory writes for brainstorms, rejected options, minor copy edits, temporary tests, one-off exports, or obvious current-turn instructions.

## Suggestion Style

Keep the suggestion one line and optional:

```text
记忆建议：可写入 MEMORY.md：品牌调性=克制电影感。回复“记住”即可。
```

Use at most one memory suggestion per reply. Do not explain the whole memory system during project work.

## Write Rule

Do not write project memory automatically unless the user says `记住`, `写入 MEMORY`, `保存项目规则`, or gives a clear equivalent instruction.

When writing, append 1-3 short bullets:

```text
- 2026-05-15 | brand_tone: 克制电影感，低饱和，不走热闹促销风。
```

Never store API keys, passwords, private contact data, or sensitive client material paths unless the user explicitly says the project memory is private and asks to record them.

## Token Control

- Read only the needed `.sw/` files.
- Prefer `MEMORY.md` + `RULES.md` for normal turns.
- Keep memory bullets under one sentence.
- If `MEMORY.md` grows too long, suggest summarizing old entries instead of loading everything.
