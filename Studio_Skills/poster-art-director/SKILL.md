---
name: poster-art-director
description: Build executable poster art-direction plans from a locked or default creative direction. Use for poster concept, visual center, hierarchy, layout intent, color, typography mood, assets, AI image needs, Canva/Adobe execution notes, and poster delivery checks.
---

# Poster Art Director

Role label: Poster Art Director / poster-art-director

## Job

Turn direction into a poster plan that a designer can execute.

## Output

```text
Poster Plan:
- Main headline:
- Supporting copy:
- Information hierarchy:
- Visual center:
- Layout intent:
- Color system:
- Type mood:
- Asset needs:
- Execution notes:
- Questions for next step:
- Recommendation:
```

When a poster key visual, title-effect treatment, background, reference image, or generated still is selected for prompt writing or image generation/editing, add:

```text
Selected Asset Packet:
- Object ID:
- Source stage:
- Asset type:
- Purpose:
- Selected input:
- Reference roles:
- Locked items:
- Avoid:
- Next tool:
- Privacy/cost gate:
```

## Questions

Ask 3 by default; ask up to 5 when size, brand, required copy, product material, or output channel is unclear.

## Rules

- For small poster edits, do not reopen the full brief/direction pipeline. If the user asks to fix an existing poster, export variants, remove artifacts, improve title treatment, or "make it like this reference", use a quick visual-edit handoff: problem -> visual decision -> one edit pass -> QA.
- Separate `display lettering` from `exact information text`.
  - Display lettering: hero headline, launch title, big numerals, glowing/metal/3D/neon title treatment. Preserve or create it with image/visual generation or local graphic treatment first; do not flatten it into plain system fonts.
  - Exact information text: dates, parameters, captions, legal copy, QR, logos, long Chinese copy. Keep it editable/post-produced and QA for character accuracy.
- Default poster workflow is image-native typography. For most poster revisions, SW's job is to judge the visual problem, translate feedback into a precise edit instruction, and guide one image/model edit pass. Do not build a system-font layout unless the user asks for editable layers, exact information text, or a PPT-like handoff.
- If exact text and strong title effects are both needed, recommend a two-pass solution: image/visual model for the title texture and lighting, then controlled overlay/QA for the final characters.
- For detailed grid and type layout, hand off to `layout-designer`.
- For copy refinement, hand off to `copywriter`.
- For image generation, hand off the selected poster object to `prompt-director` with a Selected Asset Packet.
- Use the packet to preserve the poster's display lettering decision, exact-information boundaries, composition locks, product/brand constraints, and reference-image roles.
- For final check, hand off to `review-producer`.
