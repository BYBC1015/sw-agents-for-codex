# PPT Visual And QA Reference

Use this reference when generating, reviewing, or specifying real PPT/PPTX pages, especially cinematic decks, image-heavy proposal decks, or decks produced through automation.

## Image Rhythm

Image use should create rhythm, not clutter.

For a 20-page cinematic proposal deck:

- strong image pages: about 6-8
- mixed image/text pages: about 5-7
- text-led or diagram pages: about 5-7

Do not force a full-bleed image on every page. Logic pages may be mostly typography and structure.

## Dark Overlay Rules

Dark tone is not the same as black.

Recommended overlay ranges:

- full-page atmosphere overlay: 10%-25%
- local text readability panel: 35%-55%, covering only the text area
- small image overlay: 0%-15%
- if the image is already dark, skip the overlay

Small thumbnails should not be heavily darkened. Use a light bottom label strip when needed.

## Layer Order

PowerPoint stacking rule: later-added objects sit above earlier objects.

Correct order:

```text
background image -> dark overlay -> text -> cards -> borders/page numbers/decorative lines
```

Wrong order:

```text
background image -> text -> dark overlay
```

The wrong order hides text and kills image detail.

## Cinematic Proposal Style

For local tourism or film proposals:

- use strong cover and key proposition pages
- use a consistent top chapter bar when the deck has 15+ slides
- include a table of contents for formal decks
- show visual system early, not after too much explanation
- use method pages for camera, packaging, sound, and delivery proof

## Automation Notes

When generating or checking PPTX through code:

- preserve editable text, charts, and key labels
- use template placeholders when possible
- keep images and overlays separate
- normalize transparency handling
- if Chinese file paths break a tool, copy the file to a temporary ASCII filename and keep the original untouched

Example transparency helper logic:

```python
def normalize_transparency(value):
    return value / 100 if value > 1 else value
```

## QA Checklist

Before delivery or review, check:

- slide count matches plan
- aspect ratio is correct, usually 16:9 unless specified
- agenda exists for formal 15+ slide decks
- chapter bar and page numbering are consistent
- no duplicate or redundant pages
- no banned internal words in client-facing pages
- no text overflow or overlap
- no tiny text boxes that signal broken layout
- background overlay does not cover content
- small images are still visible
- key slides are exported to PNG/PDF preview and visually inspected

Priority preview pages:

- cover
- agenda
- visual system
- structure page
- method page
- packaging/sound page
- delivery page
