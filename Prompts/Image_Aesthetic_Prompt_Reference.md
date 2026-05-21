# Image Aesthetic Prompt Reference

Use this file only when the user asks for stronger image prompts, visual style improvement, filmic references, or AI-looking reduction. Do not load it for normal brief, routing, or activation turns.

Purpose: store compact visual-language levers that improve prompt quality without piling up adjectives.

## Core Principle

Do not copy a film, frame, artist, logo, actor, or protected character. Extract visual grammar:

- composition logic
- light source and shadow behavior
- subject scale and blocking
- foreground/midground/background depth
- production design density
- color relationship
- material and texture behavior
- lens feel and imperfections
- what is intentionally excluded

## High-Value Prompt Levers

| Lever | Use In Prompt | Avoid |
| --- | --- | --- |
| Subject scale | `subject occupies 20% / 45% / 70% of frame` | "big", "small" |
| Frame depth | `foreground obstruction, clear midground subject, readable background plane` | flat background |
| Light logic | `motivated window light from frame-left, soft falloff, visible shadow direction` | generic glow |
| Color relation | `warm subject against cool background`, `low-saturation palette with one accent` | one-note palette |
| Texture | `worn metal edges, fabric weave, dust in backlight, imperfect skin/product surface` | waxy, over-polished |
| Negative space | `upper 35% clean copy area`, `right third left empty for title` | busy full frame |
| Lens behavior | `35mm natural perspective`, `85mm compressed portrait`, `wide 24mm spatial exaggeration` | random lens name |
| Atmosphere | `light haze visible only in backlight`, `wet pavement reflections` | vague mood |
| Imperfection | `subtle grain, slight lens softness, natural motion blur` | oversharpened AI crispness |
| Production design | `three meaningful props that reveal story/world` | decorative clutter |

## Anti-AI-Look Rules

Use when the user says "真实一点", "不要AI感", "更电影", or the output looks plastic.

- Add material imperfections: scratches, dust, fabric fibers, uneven reflections, small dents.
- Add real optical limits: shallow depth of field, mild motion blur, restrained highlight bloom, slight lens falloff.
- Reduce symmetry unless the concept requires it.
- Use one motivated key light instead of everywhere-glowing light.
- Keep skin, fur, products, and architecture structurally plausible.
- Avoid direct text generation unless it is a controlled placeholder.
- Prefer one strong visual idea over many decorative elements.

## Filmic Prompt Micro-Patterns

### Quiet Authority

```text
low-saturation palette, large negative space, one seated subject occupying 30% of the frame, soft side key light from a practical window, compressed 85mm portrait feel, restrained production design, natural shadows, no text, no logo
```

### Lived-In World

```text
environment tells story through worn surfaces and specific props, layered foreground/midground/background, dust visible in side light, muted palette with one small accent color, realistic material wear, no generic sci-fi UI clutter
```

### Premium Product

```text
single product centered slightly off-axis, 45-degree three-quarter view, controlled reflection, soft top-left strip light, matte background, subtle texture, clean copy space above, exact product shape preserved, no generated text
```

### Human Documentary

```text
natural 35mm field of view, imperfect candid posture, real ambient light, background activity softly separated, restrained contrast, authentic skin texture, no beauty-retouch plastic surface
```

### High-Impact Poster Visual

```text
large readable silhouette, subject occupies 65% of the frame, diagonal movement line, foreground shape creates depth, strong rim light, limited palette, top third reserved for title placement, no text in generated image
```

### Historical Visual Caution

```text
period-specific silhouette, materials, architecture, props, and patterns are locked before generation; avoid fantasy-TV costume shortcuts, modern stitching, modern signage, incorrect symbols, and generic palace decoration
```

## Reference Use Protocol

When using `01_Research/Oscar_Best_Picture_Visual_Reference.md`:

1. Pick one film or one visual lever, not a pile of references.
2. Convert the reference into neutral prompt language.
3. Keep the user's brand/project subject primary.
4. Add a copyright-safe note if the prompt risks copying a recognizable frame.

When using `01_Research/Aesthetic_Daily_Selected/Daily_Selected_Index.md`:

1. Treat the daily selected PDFs as a local moodboard, not as final assets.
2. Read the date-level contact sheet only when the user asks for that day's references.
3. Extract one or two useful levers: composition, palette, surface, lighting, type-space, or object styling.
4. Do not copy the exact layout, text, logo, person, product, or proprietary graphic.
5. Convert the selected lever into compact prompt language before any image/video generation step.

Bad:

```text
Make it like The Godfather.
```

Better:

```text
low-key interior, subject partly held in shadow, warm practical light, controlled negative space, quiet power, 50mm natural perspective, no copied actor, no recognizable scene recreation
```
