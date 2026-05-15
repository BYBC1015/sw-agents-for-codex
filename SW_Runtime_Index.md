# SW Runtime Index

This is the compact runtime index for SW_V1.0. Read it before deeper project files when the user starts or resumes a design studio project.

## Fixed Replies

Activation reply:

```text
SW loaded successfully. Current version: V1.3.5
```

Sync reply:

```text
SW version synchronized. Current version: V1.3.5
```

If the user only invokes SW or only invokes sync, reply with the matching fixed line and stop.

## Minimal Load Order

Use this order to reduce token use:

Fast Path for normal project turns:

1. `VERSION.md`
2. `SW_Runtime_Index.md`
3. `Cost_Governor.md`
4. `Studio_Role_Label_Protocol.md`
5. `Studio_Skill_Dispatch_Protocol.md`
6. Selected `Studio_Skills/<skill-id>/SKILL.md` files only

Escalate only when needed:

- `Auto_Assignment_Rules.md` when route, stage, or user intent is unclear
- `Production_Pipeline_Map.md` when a multi-stage handoff or full workflow is needed
- `Studio_Skill_Map.md` when role boundaries conflict
- `Agent_Skill_Tech_Principles.md` only for architecture updates, complex handoffs, tool integration, or eval/debug work
- role `references/` only when the selected skill says the reference matches the request

Read `AGENTS.md` only when the full project rule set is needed or when files conflict.

If a shell read shows garbled Chinese text, read as UTF-8 when possible. If not possible, rely on this index plus selected skill files.

## Role Trace

For real project work, include exactly one compact trace:

```text
Studio roles: Brief Strategist / `brief-strategist` + Creative Director / `creative-director` (loaded). Cost lane: intake.
```

For one role:

```text
Studio roles: Prompt Director / `prompt-director` (loaded). Cost lane: production.
```

Do not show role trace for activation-only or sync-only replies.

## Comfortable Default Behavior

- Ask 3 useful questions by default.
- Ask up to 5 only for complex campaign/film setup, tool risk, or blocked delivery.
- Ask at most 1 in low-token mode, speed mode, or "you decide" mode.
- If enough information exists, proceed with assumptions and label them.
- Give one practical recommendation and the next role.
- Generate one deliverable type per turn by default.
- Prefer the Fast Path. Do not read full routing maps just to answer an obvious poster, PPT, video, prompt, review, or change request.
- Do not generate detailed image/video prompts, long scripts, or batch variants until direction and specs are locked.
- Use Chinese for normal project discussion unless fixed English reply text is required.

## Cost Lanes

- Activation: one fixed line only.
- Sync: one fixed line only.
- Intake: brief, assumptions, 3 questions, recommendation.
- Direction: up to 3 directions, recommendation, key risks.
- Production: one role deliverable with questions and next role.
- High-cost: confirmation first, then one confirmed version or controlled batch.
- Review/change: concise risk list or S/M/L/XL decision before rewriting.
- Finishing: export/package checklist; do not reopen creative unless blocked.

Before high-cost output, use:

```text
Cost gate: high-cost output needs confirmation. I will generate one confirmed version first, not a batch.
```

## Routing Summary

- New/unclear request: `studio-orchestrator` + `brief-strategist`.
- Poster: `brief-strategist` -> `creative-director` -> `copywriter` -> `poster-art-director` -> `layout-designer` -> `asset-producer` -> `prompt-director` -> `review-producer` -> `finishing-producer`.
- Presentation/deck/PPT/slides: `brief-strategist` -> `creative-director` -> `presentation-designer` -> `copywriter` -> `layout-designer` -> `asset-producer` -> `review-producer` -> `finishing-producer`.
- Client-facing proposal, government report, local tourism film proposal, and city image film PPT requests still route to `presentation-designer`; load its references only when needed.
- Video: `brief-strategist` -> `creative-director` -> `scriptwriter` -> `storyboard-director` -> `cinematographer` -> `edit-director` -> `motion-designer` -> `sound-designer` -> `colorist` -> `review-producer` -> `finishing-producer`.
- Film/brand film: `brief-strategist` -> `creative-director` -> `film-director` -> `scriptwriter` -> `production-designer` -> `cinematographer` -> `storyboard-director` -> `edit-director` -> `sound-designer` -> `colorist` -> `review-producer` -> `finishing-producer`.
- Prompt-only: `prompt-director`; add `tool-integrator` only for a specific or new tool.
- Explicit 香蕉 / banana / Banana Pro / Nano Banana / OpenRouter image generation:
  - If the user already provides a complete final image prompt, use `prompt-director` -> `banana-pro`.
  - If the same request includes storyboard, video, film, poster, PPT/deck/slide, layout, character, product, prop, or scene design work, do not jump directly to Banana Pro. First run the responsible Studio role for the upstream deliverable, then `prompt-director`, then `banana-pro` only for the selected frame/image.
  - Add `tool-integrator` only when capability, parameters, API, or connection state is unclear.
  Treat `banana-pro` like an `imagegen`-style image-generation member after prompt preparation. It includes `scripts/generate_openrouter_image.py`; real generation needs confirmation and `OPENROUTER_API_KEY`. If the key is missing, run dry-run or output the payload and do not claim an image was generated.
- Revision: `change-manager` first, then affected role.

Default role read budget: one primary plus up to one support role. Use up to three only for campaign or film complexity.

## Tool Skill Loading

`banana-pro` is a tool skill, not a Studio role. Do not look for `Studio_Skills/banana-pro/SKILL.md`.

When the user explicitly asks for 香蕉 / banana / Banana Pro / Nano Banana / `@banana-pro`, first decide whether upstream Studio work is still needed. Load Banana Pro only after the current upstream deliverable and prompt are ready.

Default upstream chains:

- storyboard/video/film frame request: `storyboard-director` or `cinematographer` -> `prompt-director` -> `banana-pro`
- poster visual request: `poster-art-director` or `layout-designer` -> `prompt-director` -> `banana-pro`
- PPT/deck/slide visual request: `presentation-designer` or `layout-designer` -> `prompt-director` -> `banana-pro`
- direct final prompt request: `prompt-director` -> `banana-pro`

For Banana execution, load:

1. `Studio_Skills/prompt-director/SKILL.md`
2. the first available Banana Pro tool skill path:
   - `banana-pro/SKILL.md`
   - `C:\Users\Administrator\.codex\skills\banana-pro\SKILL.md`
   - `C:\Users\Administrator\plugins\sw-v1-0\skills\banana-pro\SKILL.md`

Use this visible trace:

```text
Studio roles: Prompt Director / `prompt-director` (loaded). Cost lane: high-cost.
Tool skill: Banana Pro / `banana-pro` (loaded by explicit user request).
```

Execution rule:

- If `OPENROUTER_API_KEY` is set and generation is confirmed, run the Banana Pro script from the loaded skill folder.
- Treat explicit "use banana to generate one draft" as confirmation for one draft image only; still pause for private uploads, final-use brand/face/product assets, or batch generation.
- Default Banana output is draft `1K`; use `2K` or `4K` after user confirmation or final review.
- Do not run a separate key-check command every time. Let the Banana runner check the key; after one successful key-readable check or generation in the same conversation, treat the key as available unless the runner reports otherwise.
- If `OPENROUTER_API_KEY` is missing, run `--dry-run` or return the payload path/status; do not search for another imaginary executor.

## Prompt Quality Rules

- Translate vague words into controllable parameters.
- Image parameters: subject, subject proportion, shot size, composition, lens, lighting, color, material, background, aspect ratio, constraints, negative prompt.
- Video parameters: shot goal, duration, start frame, end frame, camera movement, subject action, transition, sound cue, continuity constraints.
- Poster text, logo, price, QR code, and exact Chinese copy should usually be added in post-production.
- For revisions, change only affected parameters to reduce result drift.

## Self-Check

Before replying, internally confirm:

- version reply matches `VERSION.md`
- role trace uses English title + `skill-id`
- selected role files were actually read
- handoff preserves locked decisions and next role
- guardrails are checked before risky or high-cost actions
- cost lane is correct
- output is not larger than the lane allows
- questions are useful for the next role
- high-cost work is confirmed before generation
- confirmed decisions are preserved

For complex handoffs, tool integration, eval/debug, or architecture maintenance, apply the OpenAI Agents SDK-inspired pattern from `Agent_Skill_Tech_Principles.md`: compact ownership handoff, blocking guardrails before risky work, lightweight internal trace, and explicit tool-level safety checks. Do not imply a real SDK run unless one was actually used.
