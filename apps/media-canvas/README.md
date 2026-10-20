# SW Canvas 0.4.1

Local visual production workspace bundled with SW V1.16.1. Stores project media references, tasks, revisions, annotations and versioned storyboard records. No model calls or cloud uploads happen automatically.

## Start

Requires Python 3.10+, Pillow, and FFmpeg/ffprobe on PATH for video previews. Image-only work does not need FFmpeg.

```powershell
python -m pip install -r apps/media-canvas/requirements.txt
python -B -X utf8 apps/media-canvas/launcher.py
```

Windows: `Start-Canvas.cmd` or `start.ps1`. To leave the browser closed, pass `--no-browser` to the Python launcher or `-NoBrowser` to PowerShell. The server listens only on 127.0.0.1:8961; an existing service with another version is reported instead of being killed automatically. Close the old server or choose another port before starting the upgrade.

`python tools/sw_sync_installed.py` installs the `sw-canvas` and `media-canvas` skills with paths resolved to this checkout. Moving the checkout requires rerunning sync.

On Windows, the launcher uses local WMI to create a hidden server independently of the invoking shell's process tree. Startup parameters are passed as data; only required system/media environment settings are forwarded. No scheduled task or login startup is installed. Other platforms use a separate process session. The server records its PID and startup/exit diagnostics in the data directory.

If a saved page reports `ERR_CONNECTION_REFUSED`, run the launcher again and refresh that same URL. This restores the service without creating a project or changing conversation bindings. Browser refresh cannot start a stopped local program; after reboot, start Canvas once. If local WMI is unavailable, the launcher reports the failure instead of claiming success.

In a bound Canvas workflow, register generated media in Canvas and return a short text receipt/link in chat. Banana follows the same rule; its JSON image links are not instructions to embed images. Mandatory native tool output and images explicitly requested in chat still follow their respective rules. Previously displayed chat images remain in history.

## Storyboards

Open a project and choose **分镜与连续性**. Create reusable character, wardrobe, scene, prop, product or style records; each revision keeps its description, locks and optional reference asset. Create shots with stable IDs, script, duration, camera, exact entity versions and an output asset.

- Editing a shot appends a version. Changes to script, camera, references or locks clear an unchanged output association. Every new revision needs its own visual review.
- Changing a shared asset lists its affected shots and flags their old references for review. It never starts generation.
- Version selection restores the exact prior shot and references. Old versions and original media remain available.
- Review the actual image and record pass/fail with evidence. The software tracks reviews; it does not itself recognize faces or judge visual continuity.
- Export a draft manifest with blockers, or a reviewed manifest after all selected shots pass. The JSON includes only selected versions and referenced entity revisions, without local paths. This release does not add PDF rendering.

The board UI supports edits, version selection and review. CLI, HTTP and on-demand WebMCP tools share the same project state. See [API reference](integrations/media-canvas/references/api.md) and [continuity contract](../../Storyboard_Continuity_Protocol.md).

## Existing Canvas features

Project switching and explicit conversation binding; local image/video import; version lineage; frame annotations and side-by-side comparison; fixed-input tasks; atomic result registration; collision-aware layout with one-step layout undo; bounded context summaries and immutable project handoff snapshots.

Project writes retain revision and conversation-binding guards. Tasks do not execute themselves. A result in review is not automatically accepted. Checkpoints contain metadata and references, not copies of all media.

## Storage and configuration

New installations default to `~/SWCanvas`: project workspace under `projects/`, default data under `default/`, and the registry in `projects/.media-canvas/catalog.sqlite3`. Existing Windows `T:/Work素材` and `E:/Downloads/制作画布_项目数据` locations are reused when present, preserving current bindings. No automatic media or database migration.

Environment overrides: `MEDIA_CANVAS_HOME`, `MEDIA_CANVAS_WORKSPACE`, `MEDIA_CANVAS_DATA`, `MEDIA_CANVAS_REGISTRY`, `MEDIA_CANVAS_FFMPEG`, `MEDIA_CANVAS_FFPROBE`. PowerShell can use `MEDIA_CANVAS_PYTHON`. `MEDIA_CANVAS_MEDIA_ROOTS` is a JSON array of extra absolute import roots. Defaults allow the workspace and user Downloads; other inputs can be copied into the project with `ingest` and `mode: copy`.

The CLI/server also accept `--data-dir`, `--registry`, `--workspace-root` and project-specific commands. If using a custom workspace outside configured roots, add that directory to `MEDIA_CANVAS_MEDIA_ROOTS` for media imports.

For live backups use CLI `backup --path NEW_PATH`, which uses SQLite's backup API. Preserve the catalogue and original media separately. Never publish `.runtime`, databases, media caches, logs, private configuration or client files.

## Validation

```powershell
python -B -X utf8 -m unittest discover -s apps/media-canvas/tests -v
node --check apps/media-canvas/web/storyboard.js
```

Tests use temporary projects and synthetic images. See [VALIDATION.md](VALIDATION.md). Large-project stress testing, automatic visual scoring, remote collaboration and cloud synchronization are outside this release.
