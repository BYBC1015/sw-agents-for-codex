---
name: black-background-cutout
description: Remove black or simple solid backgrounds from local images for quick cutout/transparent PNG previews. Use when the user says 抠图, 扣图, 去底, 去黑底, 黑底转透明, transparent PNG, or asks to cut out a black/solid-background image. Do not use for complex photo cutouts or finishing-grade no-fringe assets.
metadata:
  short-description: Quick black/solid background cutout
---

# Black Background Cutout

## Job

Turn local black-background or simple solid-background images into transparent PNG previews without regenerating the artwork.

This is a local pixel-processing tool, not an AI image-generation tool and not a formal finishing-grade cutout workflow. It may leave slight edge fringing, especially around glow, dark shadows, antialiased strokes, or compressed JPG edges.

## Use When

- The user explicitly says 抠图, 扣图, 去底, 去黑底, 黑底转透明, or 透明底.
- The source is a local image or a batch of local images.
- The background is pure black, near-black, or another simple solid color.
- The user needs fast transparent PNGs for preview, layout testing, internal review, or temporary compositing.

## Do Not Use For

- Complex photo backgrounds, hair, people, products in natural scenes, smoke, gradients, or textured backgrounds.
- Foregrounds that contain important black/dark details likely to be erased.
- Final delivery assets that require clean professional edges.
- Redesigning, rewriting, or matching AI-generated lettering.

If the user needs final-grade output, say this quick cutout may have light fringing and recommend a regenerated transparent asset, layered source file, or professional cutout pass.

## Workflow

1. Confirm the input file paths exist.
2. Use `scripts/black_background_cutout.py`.
3. Default to black-background mode unless the user asks for a different solid color.
4. Create:
   - `cutout_transparent_png/full_canvas/`
   - `cutout_transparent_png/trimmed/`
   - `cutout_transparent_png/previews/`
   - `cutout_transparent_png/cutout_transparent_png.zip`
5. Inspect the checkerboard preview before reporting completion.

## Default Parameters

For clean black-background PNGs:

```text
edge_start = 2
opaque_at = 24
padding = 24
```

Meaning:

- `max(R,G,B) <= edge_start` becomes fully transparent.
- `max(R,G,B) >= opaque_at` becomes fully opaque.
- Values between them get soft alpha.

For non-black solid backgrounds, use `--bg-color R,G,B` and adjust `--tolerance-start` / `--opaque-distance` cautiously.

## Command Pattern

```powershell
python black-background-cutout\scripts\black_background_cutout.py "C:\path\image.png"
```

Batch:

```powershell
python black-background-cutout\scripts\black_background_cutout.py "C:\path\*.png"
```

Custom output:

```powershell
python black-background-cutout\scripts\black_background_cutout.py "C:\path\*.png" --output-dir "C:\path\cutout_transparent_png"
```

## Validation

Pass criteria:

- Background is transparent in the preview.
- Main foreground remains visible.
- No large black box remains.
- Edge fringe is acceptable for preview use.
- Original files are unchanged.

If the preview has heavy black residue, increase `edge_start` or `opaque_at` slightly. If dark foreground details disappear, lower `opaque_at`.

## Final Response

Keep it short. Include the local output folder, full-canvas PNG folder, trimmed PNG folder, ZIP path, and preview image if available.

Always mention when relevant:

```text
这是快速抠图结果，边缘可能有轻微毛边；正式交付建议重新出透明底或做专业精修。
```
