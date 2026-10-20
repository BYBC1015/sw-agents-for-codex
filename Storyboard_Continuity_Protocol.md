# Storyboard continuity contract

Use only for persisted storyboard production or revisions in a user-selected Canvas project. Ordinary creative conversation remains lightweight; SW activation rules are unchanged.

## One source of project state

Canvas `apps/media-canvas/canvas_cli.py` owns persisted shot/entity records. Read the installed `media-canvas` API reference for command syntax. Keep the real conversation binding and project ID on every write. Do not write creative decisions to `.sw/MEMORY.md` without the existing explicit memory instruction.

- Give each shot and reusable character/wardrobe/scene/prop/product a stable ID.
- Each shot revision stores script, camera, duration, locks, exact entity versions and its selected output asset ID. A new edit appends a revision; selecting an old revision restores its references and output together.
- Before changing a shared entity, read `storyboard-impact --entity ID`. Report affected shot IDs. A new entity revision flags those shots for review; it never generates replacements automatically.
- For a camera-only edit, send only the camera field. Preserve the shot's entity references and locks. Substantive edits clear the old output unless a replacement is explicitly attached; all new shot revisions need new visual approval.
- Use `expectedRevision` and a stable `requestId`. On an unknown response retry the same request, not a fresh ID. On conflict reread the project; do not remove revision/binding checks.

## Generation handoff

Read `shot-packet --shot ID` immediately before generating. The packet contains the shot version, fixed entity versions, reference asset IDs, protected locks and outstanding issues. Resolve outdated dependencies before generation; never substitute latest references silently. Resolve referenced assets in the same project and pass them to the image tool with the correct reference roles.

Save the packet as UTF-8 JSON for Banana `--lock-file`. This file carries constraints, not authorization to upload or generate. The runner protects locks through compression and retry, and refuses a budget that cannot fit them. Other tools must preserve the same locks during prompt conversion.

Before registering a returned output, reread the shot and compare its version with the packet used to generate it. If the shot changed meanwhile, keep the result as a candidate asset and do not attach it to the new shot automatically.

## Review and export

Inspect the actual selected output for identity, wardrobe, props, scene geometry, direction of movement and adjacent-shot continuity. Record pass/fail with visible evidence and the exact shot version. Metadata checks alone are not visual approval; a successful model call is not approval.

`storyboard-export` produces a draft manifest with blockers. `--final` requires every selected shot to have an output, current dependencies and a recorded passing visual review. It exports selected versions only, with no local file paths. The manifest is a production handoff, not a PDF or rendered film.

## Regression scenario

Use a synthetic 30-second, six-shot story for software tests: change only S03's camera, change a shared wardrobe used in S01–S04, restore S03, then export. Assert unaffected records are identical, affected IDs are exact, prior outputs survive in history, and old approvals cannot validate new revisions. Paid image quality comparisons remain a separate explicitly requested exercise.
