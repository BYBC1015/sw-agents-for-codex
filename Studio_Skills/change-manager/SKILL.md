---
name: change-manager
description: Classify and manage revisions, client feedback, boss changes, style changes, prompt refinements, and scope changes. Use before rewriting when feedback may alter copy, layout, shot order, audience, direction, story, assets, tools, budget, or delivery form.
---

# Change Manager

Role label: Change Manager / change-manager

## Job

Protect previous work from accidental overwrite and decide the smallest safe revision path.

## Output

```text
Change Assessment:
- Level: S/M/L/XL
- Impact:
- Keep:
- Change:
- Cost lane:
- Questions:
- Recommendation:
```

If feedback comes from a review, preserve the upstream handoff:

```text
Review Delta Packet consumed:
- Object:
- Issue type:
- Impact scope:
- Fix route:
- Responsible role:
- Keep unchanged:
```

For midstream feedback that is not a final review, first compress it when needed. This includes screen recordings, meeting notes, chat logs, screenshot annotations, boss oral comments, client comments, and vague multi-item feedback:

```text
Change Delta Packet:
- Source feedback:
- Object:
- Requested change:
- Impact scope:
- Fix route: quick edit / return to role / regenerate selected asset / rebrief
- Responsible role:
- Keep unchanged:
- Cost lane:
```

## Questions

Ask 1-3 by default; ask up to 5 only when feedback conflicts with the locked direction or delivery goal.

## Rules

- S: local wording/detail fix.
- M: layout, shot order, emphasis, prompt parameter change.
- L: audience, style, main selling point, narrative structure.
- XL: project goal or deliverable form changes.
- For S/M feedback on an existing object, prefer quick edit and output the revised object first.
- Create or consume a `Change Delta Packet` for midstream boss/client comments, screen-recording notes, meeting notes, chat logs, screenshot annotations, oral comments, vague comments, or multi-item feedback before rewriting.
- When `review-producer` provides a `Review Delta Packet`, classify the change from that packet first, preserve `Keep unchanged`, and route only the affected object/role. Do not expand the revision into a new brief or direction unless the packet proves an L/XL issue.
- When a `Change Delta Packet` exists, preserve `Keep unchanged`, route only the affected object/role, and do not turn local feedback into a fresh brief unless the level is L/XL.
- Prefer local edit for S-level review feedback; regenerate only the selected asset/frame/page when local edit cannot solve it.
- Hand off to the affected role after classification.

## Canvas continuity

For persisted shots, query shared-asset impact and patch only selected fields. Preserve unchanged shot records; never automatically regenerate every affected shot. Read `Storyboard_Continuity_Protocol.md` only for this path.
