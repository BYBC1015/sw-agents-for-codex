# Canvas 0.4.0 validation

Run the test suite from the repository root or from this app. All tests use temporary databases and synthetic fixtures; no user projects or paid generation are used.

The 30-second / six-shot regression checks camera-only edits, exact shared-wardrobe impact, unchanged unaffected shots, version restoration, selected-version export, stale revision rejection, invalid cross-project references, retries, checkpoint history, CLI and HTTP parity, and explicit visual review gates.

The existing suite also checks project/conversation isolation, media boundaries, local-origin HTTP controls, atomic imports/results, state snapshots, summaries and layout undo. Browser testing additionally exercises editing and restoration through the actual page when Playwright/Chromium are available.

These are software behavior checks. Synthetic passing review records are test data, not evidence that generated creative work has passed visual quality review. No automatic face/wardrobe recognition or paid model-quality benchmark is claimed.
