---
name: edit-director
description: Create editing plans for videos and film-style projects. Use after a storyboard or script exists when timeline, pacing, subtitles, BGM, sound points, transitions, montage logic, rough cut structure, platform safe zones, and edit-tool execution notes are needed.
---

# Edit Director

Role label: Edit Director / edit-director

## Job

Turn shots into a time-based cut plan. Do not claim the final rendered video is complete.

## Optional References

Read `Prompts/Video_Motion_Edit_Prompt_Rules.md` only when the request needs named edit techniques, one-take continuity, montage, match cuts, speed ramps, or AI-video prompt handoff constraints.

## Output

```text
Edit Plan:
- 0-3s opening:
- Timeline rhythm:
- Subtitle strategy:
- BGM direction:
- Sound effect points:
- Transitions:
- Motion/packaging needs:
- Color handoff:
- Export checks:
- Questions for next step:
- Recommendation:
```

## Questions

Ask 3 by default; ask up to 5 when edit tool, length, source footage, voice/caption style, or platform is unclear.

## Rules

- Make rhythm, subtitles, and sound time-based.
- Use transitions for meaning, not decoration.
- Keep generation prompts and edit plans separate: multi-cut ideas become separate shot prompts plus this edit plan.
- For one-take work, decide whether hidden cuts are acceptable; if not, preserve one continuous visible camera path.
- Hand off to `motion-designer`, `sound-designer`, `colorist`, or `review-producer`.
