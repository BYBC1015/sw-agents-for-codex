# Interactive Aesthetic Browser - Tech Notes

This is a planning note only. It does not change the SW runtime and should not be loaded during normal project work.

## Product Goal

Build a local, visual, low-friction way to browse SW's aesthetic image library, review contact sheets, mark bad/duplicate/useless images, and keep only references with reusable visual value.

## Required Workflow

1. Scan portable roots from `Aesthetic_Library_Config.md`.
2. Generate thumbnails and read metadata without moving originals.
3. Show fast grid, large preview, source/index notes, and contact-sheet grouping.
4. Allow lightweight decisions: keep, reject, maybe, duplicate, too low-res, useful for profile.
5. Write decisions to sidecar metadata, not into the image files.
6. Export compact indexes for SW: profile tags, source lane, visual lesson, quality tier, and safe extraction rule.

## Metadata Model

Use a sidecar database or JSONL file with this shape:

```text
id:
relative_path:
source_index:
source_url:
quality_tier:
status: keep | reject | maybe | duplicate | replace
profiles:
visual_levers:
avoid:
notes:
reviewed_at:
```

## Candidate Open-Source Technologies

| Option | Fit | Strengths | Weaknesses | SW Recommendation |
| --- | --- | --- | --- | --- |
| Photofield | Fast local viewing of huge image sets | Single-binary, non-invasive, designed for speed and many visible images | Less focused on manual curation metadata and SW-specific export | Strong viewer candidate; pair with SW sidecar metadata. |
| HomeGallery | Self-hosted gallery with tagging, mobile-friendly browsing, similar-image discovery | Good browsing/tagging/discovery direction; can serve local sources | More setup and its AI API/privacy choices need review | Good research candidate for browsing and tagging patterns. |
| FiftyOne | Dataset curation, visualization, labels, quality filtering, vector/search workflows | Excellent for finding duplicates, clusters, low-quality items, and visual dataset review | More technical and ML-oriented; heavier than a simple gallery | Best advanced QA layer if the library becomes very large. |
| PhotoPrism | Mature self-hosted photo app with AI tagging/search | Strong photo management and automatic organization | Heavier product, more personal-photo oriented than SW references | Useful benchmark, not ideal as SW core. |
| Immich | High-performance self-hosted photo/video management | Excellent media UX, mobile/web, search, albums, dedupe-style features | Designed as a Google Photos alternative, not a design-reference curation tool | Good UX benchmark, not the first SW implementation. |
| Label Studio | General annotation platform with standardized export | Strong if SW later needs structured labels, review fields, and export formats | Overkill for casual viewing; UI is annotation-first, not moodboard-first | Useful if review turns into dataset labeling, not first viewer. |
| CVAT | Mature visual dataset annotation platform with QA/team workflows | Strong for image/video annotation, quality assurance, and dataset-scale review | Heavy setup and too task-oriented for daily aesthetic browsing | Keep as a reference for future QA patterns only. |
| Custom SW browser | Purpose-built for SW metadata, profiles, and rejection workflow | Lowest conceptual mismatch, can stay repo-aware and token-light | Requires building and maintaining our own UI | Recommended first implementation after prototype design. |

## Recommended Architecture

Phase 1 should be custom and local:

```text
image roots -> scanner -> SQLite/JSONL sidecar -> thumbnail cache -> local web UI -> export compact SW indexes
```

Phase 2 can borrow ideas or optional integrations:

- Use Photofield or HomeGallery for fast viewing if their setup is quicker than custom thumbnails.
- Use FiftyOne only when the library is large enough to need duplicate detection, similarity search, clustering, or quality triage.
- Keep SW runtime separate. Normal `/sw` work reads compact indexes, not the browser database or raw images.

## First SW Browser Features

- Grid with keyboard rating: `1 keep`, `2 maybe`, `3 reject`, `D duplicate`, `R replace`.
- Filters: profile, source lane, resolution, status, date added, unreviewed only.
- Large preview with source note and "visual lesson" field.
- Contact-sheet mode for 9/16/25-image comparison.
- Export: update candidate markdown/JSONL without touching original images.
- Safety: never expose API keys, upload tokens, or private project paths.

## Why Not Build Now

- The image library root may move to another disk.
- We should first stabilize the sidecar metadata schema.
- The current SW runtime goal is low-token decision-making; a gallery UI should be an optional maintenance tool, not part of every project.
