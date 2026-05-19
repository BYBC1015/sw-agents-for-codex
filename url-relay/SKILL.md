---
name: url-relay
description: Convert local image or video files into public http(s) URLs through the configured SW media uploader. Use when Codex needs a public URL relay for Seedance/即梦2.0, Ark, Banana Pro reference images, image-to-video tools, or any AI tool that cannot read local files. Trigger on URL中转, 公网URL, 上传参考图, 上传参考视频, 中转上传, @url-relay, or when a Seedance request includes a local image/video path instead of a public URL.
---

# URL Relay

## Principle

Use this as a small tool skill, not a Studio role. It turns local media into a public URL through the configured SW media uploader so another tool can fetch it.

Default route for Seedance:

```text
upstream Studio role if needed -> prompt-director -> url-relay when local files need public URLs -> seedance-2-video
```

Do not use URL Relay for creative planning, prompt writing, storyboard design, or review. It is an execution support layer.

## Privacy And Cost

- Public relay URLs are fetchable by anyone who has the link until the server cleanup removes them.
- Upload only files the user has permission to send outside the local machine.
- Do not upload client-confidential, unreleased product, face, brand, or private-location material unless the user explicitly allows it.
- Uploading uses server bandwidth and storage, not AI model tokens. The downstream generator may still consume model credits.
- Never print or commit the upload token. Read it from `~/.config/sw-media-uploader/config.json`, `SW_RELAY_TOKEN`, or a user-provided local config path.

## Default Relay

Prefer the configured SW media uploader:

```text
config: ~/.config/sw-media-uploader/config.json
upload_url: http://123.56.255.86/upload
public_base: http://123.56.255.86/u
```

The config file is private local state and must stay outside the Git repository.

## Priority Fallback Policy

If the SW media uploader is unavailable or intentionally abandoned:

1. Keep the prepared prompt and generation payload.
2. Use an already-public user URL if available.
3. If a temporary relay fallback is configured or the user confirms it in this turn, try `Litterbox`/`Catbox` only after the SW media uploader is unreachable or returns a server-side failure.
4. When fallback is used, explicitly tell the user: `SW media uploader unavailable; temporary relay fallback used: <relay>.`
5. If the issue is missing token, missing upload URL, or a permission/config error, do not fallback; fix the private config or pause before spending generation credits.
6. If no confirmed fallback exists, ask the user for a public URL or pause before spending generation credits.

Do not invent a public URL, and do not submit Seedance with local paths.
Do not describe third-party temporary relay output as "our server".

## Commands

Use the bundled script from this skill folder:

```bash
python scripts/url_relay.py doctor
python scripts/url_relay.py upload --file ./reference.png
python scripts/url_relay.py upload --file ./reference.png --temporary-relay-fallback auto
```

Expected upload output is JSON with `ok`, `url`, `relay`, and `expires_hint`.

For one-time local setup:

```bash
python scripts/url_relay.py setup --upload-url http://host/upload --public-base http://host/u
```

Then paste the upload token when prompted. The token is saved only to the private local config file.

## Seedance Integration

`seedance-2-video/scripts/seedance_task.py` supports both:

```bash
--image-url https://example.com/reference.png
--image-file ./local-reference.png
```

When `--image-file` is used, the runner should upload the file with this relay first, then pass the returned public URL to Ark.

If upload fails, stop before real generation and report the relay failure. Fall through to Catbox/Litterbox only when `temporary_fallback` is configured or the user explicitly confirms that fallback; never use a fake URL.
