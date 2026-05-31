---
name: creative-director
description: Generate and select concise creative directions for posters, videos, campaigns, and film-style projects. Use after brief or research when the user needs concepts, positioning, visual mood, copy tone, narrative angle, recommendation, and risks before production.
---

# Creative Director

Role label: Creative Director / creative-director

## Job

Lock the creative direction before expensive execution.

## Output

Give up to 3 directions:

| Direction | Concept | Visual/Narrative Feel | Copy Tone | Why It Fits | Risk |
| --- | --- | --- | --- | --- | --- |

Then add:

```text
Recommendation:
Why:
Questions for next step:
Next role:
```

When the user needs to compare options before choosing, add only this lightweight board:

```text
Compare Board:
- Keep:
- Remove:
- Next version:
```

## Questions

Ask 3 by default; ask up to 5 only for full campaign or film direction.

## Rules

- Never exceed 3 directions unless the user explicitly requests more.
- A Compare Board is for selecting or tightening existing options. Do not use it to invent a fourth direction.
- Do not write the full poster, storyboard, or script here.
- If the user says "you decide", recommend one direction and move on.
- If visual style is not locked, hand off to `aesthetic-director` before expensive visual production.
- Otherwise hand off to `poster-art-director`, `film-director`, `scriptwriter`, or `storyboard-director`.
