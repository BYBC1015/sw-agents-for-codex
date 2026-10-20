---
name: kling-api
description: Generate, query, and download videos through the official Kling API, including Kling 3.0 and 3.0 Omni video reference or scene/element editing. Use for requested Kling API or API Key integration; keep OAuth Kling CLI/MCP separate.
metadata:
  version: "1.16.0"
---

# Kling API

Use the official current API with an API Key. Ordinary text/image videos default to **Kling 3.0**; video reference or editing an existing clip uses **Kling 3.0 Omni**. This tool also runs independently of SW. When SW is active, consume the selected prompt and asset handoff from upstream design work.

## Private setup

The runner uses Python's standard library. Private config: `~/.config/kling-api/secrets.json` (`XDG_CONFIG_HOME` overrides its config root), with `api_key` and optionally `base_url`. Local private config takes priority over environment credentials; `KLING_API_KEY` and `KLING_BASE_URL` are fallbacks.

```text
python scripts/kling_task.py setup-key
python scripts/kling_task.py doctor
```

`setup-key` accepts hidden input; `--api-key-stdin` supports trusted local secret input without placing a key in command arguments. Never print credentials or put them in repository files, prompts, manifests, examples, or handoffs. Never read CLI OAuth credentials. Share this skill without private config; another machine supplies its own key. Hermes on this machine uses the same runner and private user config.

API Key authentication is `Authorization: Bearer <API Key>`, directly, at `https://api-beijing.klingai.com`. Do not turn a new key into AK/SK or JWT. Existing AK/SK users may explicitly select `--api-version legacy`; the payloads differ.

## References

- [Current API](references/kling-api.md): endpoints, contents/settings, Omni reference modes, limits and task lifecycle, verified 2026-09-11.
- [Legacy API](references/kling-api-legacy.md): old `/v1/videos/*` schema only for legacy compatibility. Do not reuse its reference tokens or response fields in a current request.

## Choose a mode

| Request | Runner options | Current model |
| --- | --- | --- |
| Ordinary text video | `--kind text` | Kling 3.0 |
| First-frame or first/last-frame video | `--kind image` | Kling 3.0 |
| Use a video's camera/action as a reference for a new clip | `--kind omni --video-refer-type feature` | Kling 3.0 Omni |
| Modify an existing video's elements, clothing, or scene | `--kind omni --video-refer-type base` | Kling 3.0 Omni |

Always specify reference mode for a video. Name what changes and what remains. Reference assets in prompts with `@video_1` or `@image_1`; current API does not use legacy angle-bracket tokens.

Local videos need a Kling-accessible public URL: no documented local-path, video-Base64, or multipart upload field. Use the configured upload workflow within the user's authorization, then pass its URL. Do not upload during integration checks. Local images can use `--image-file`; real submission requires `--confirm-upload`.

## Prepare, submit, resume

Inspect one concrete `dry-run`, then submit only within the user's authorization for that generation. Setup and document maintenance do not authorize a charged video. Existing explicit authorization for the same clip is sufficient; do not ask again.

Ordinary video defaults: 5 seconds, 1080p, silent, single shot.

```text
python scripts/kling_task.py dry-run --kind text --prompt "A calm product shot with a slow controlled dolly-in." --duration 5 --resolution 1080p --audio off
```

Motion/camera reference:

```text
python scripts/kling_task.py dry-run --kind omni --video-url https://example.com/reference.mp4 --video-refer-type feature --prompt "参考 @video_1 的运镜与动作节奏，生成雨夜街道画面。" --audio off
```

Edit the original scene and retain its audio:

```text
python scripts/kling_task.py dry-run --kind omni --video-url https://example.com/source.mp4 --video-refer-type base --prompt "将 @video_1 的背景改为雨夜街道；保留人物身份、动作、机位、时序与其他元素。" --audio original
```

Replace `dry-run` with `run`, add a unique `--output-dir` and `--yes` for an authorized task. Prefer `--submit-only` and subsequent bounded polling when the agent needs to remain responsive. A submission is accepted only after a real task ID is returned. Do not automatically resubmit after timeout or interruption.

```text
python scripts/kling_task.py poll --output-dir outputs/kling-shot-001 --timeout 40
```

Record the manifest location in a local handoff so Hermes or Codex can continue the same task. Deliver after success and file verification; download results before their URLs expire. Inspect the output against the requested edits and preserved elements.
