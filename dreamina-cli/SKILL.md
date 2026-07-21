---
name: dreamina-cli
description: Use Dreamina / Jimeng official CLI for explicit image generation, video generation, login, credit checks, sessions, task history, result query, and downloads. Use only when the user explicitly asks for Dreamina CLI, Jimeng CLI, official Jimeng CLI, dreamina, @dreamina-cli, Jimeng image generation, or Jimeng video generation through the official CLI. Do not use for generic prompts, storyboard planning, or Ark Seedance API requests.
---

# Dreamina CLI

Use this as an explicit downstream tool skill for the official Dreamina / Jimeng CLI command named `dreamina`.

This tool is separate from `seedance-2-video`:

- `dreamina-cli` uses the official Dreamina/Jimeng local CLI and account login.
- `seedance-2-video` uses the Ark Seedance API runner and `ARK_API_KEY`.

## Current Verified Source

The install entry provided by the user is:

```bash
curl -fsSL https://jimeng.jianying.com/cli | bash
```

The installer currently downloads:

- CLI program name: `dreamina`
- official skill file from Dreamina static storage
- version metadata showing CLI version `1.4.10`, release date `2026-06-26`

The official Lark wiki may require login. When the wiki cannot be read, do not invent parameters from memory. Treat `dreamina -h` and `dreamina <subcommand> -h` as the live reference.

## Local Install Status

Checked on 2026-07-13:

- Windows official CLI installed at `C:\Users\Administrator\bin\dreamina.exe`.
- Installer wrote `C:\Users\Administrator\bin` into the Windows user PATH; a new terminal may be needed before plain `dreamina` resolves.
- Installed metadata: version `1.4.10`, release date `2026-06-26`.
- Build command reports commit `2a20fff`, build time `2026-06-26T06:36:39Z`.
- Account login is not yet configured on this machine; `user_credit` reports that login is required.

## Safety Contract

- Do not execute `curl | bash` without explicit user confirmation.
- Do not claim generation is available unless `dreamina` is installed and login/session state is usable.
- Real image or video generation may consume Dreamina credits. Ask before real submission unless the user explicitly asked to generate one draft.
- Private/client images, faces, unreleased products, brand assets, audio, or videos require upload/privacy confirmation before use.
- Never write login tokens, OAuth device codes, cookies, account state, or generated private media URLs into the repository, prompts, logs, or handoff docs.
- If login is required, keep the user visibly informed until success, reuse, or failure is clear.

## Capabilities

Use the CLI for:

- `dreamina -h` and subcommand help inspection
- account login/relogin/logout/checklogin
- credit checks
- session management
- text-to-image generation
- image-to-image generation
- image upscale
- text-to-video generation
- image-to-video generation
- frames-to-video generation
- multi-frame video generation
- multimodal video generation
- async result query and result download
- saved task history review

## Verified Command Surface

Observed from installed CLI help on 2026-07-13. Re-check subcommand help before real generation because model capacity and flags can change.

Image:

- `text2image`: model versions `3.0`, `3.1`, `4.0`, `4.1`, `4.5`, `4.6`, `4.7`, `5.0`; ratios `21:9`, `16:9`, `3:2`, `4:3`, `1:1`, `3:4`, `2:3`, `9:16`; `generate_num` 1-10; `3.0/3.1` support `1k` or `2k`; `4.0+` support `2k` or `4k`.
- `image2image`: uploads 1-10 local images; model versions `4.0`, `4.1`, `4.5`, `4.6`, `4.7`, `5.0`; same ratios as text2image; `generate_num` 1-10; resolution `2k` or `4k`; `1k` is not supported.
- `image_upscale`: uploads one local image; resolution `2k`, `4k`, `8k`; `4k` and `8k` require VIP.

Video:

- `text2video`: model versions `seedance2.0`, `seedance2.0fast`, `seedance2.0_vip`, `seedance2.0fast_vip`, `seedance2.0mini`; ratios `1:1`, `3:4`, `16:9`, `4:3`, `9:16`, `21:9`; duration 4-15s; `seedance2.0_vip` supports `720p`, `1080p`, or `4k`, other models support `720p`; default model is `seedance2.0fast`.
- `image2video`: uploads one local first-frame image; ratio is inferred from the image; model versions `seedance1.0fast`, `seedance1.0`, `seedance1.5pro`, `seedance2.0`, `seedance2.0fast`, `seedance2.0_vip`, `seedance2.0fast_vip`, `seedance2.0mini`; duration depends on model family; `seedance2.0_vip` supports `720p`, `1080p`, or `4k`, other models support `720p`.
- `frames2video`: uploads local first and last images; model versions `seedance1.5pro`, `seedance2.0`, `seedance2.0fast`, `seedance2.0_vip`, `seedance2.0fast_vip`, `seedance2.0mini`; default model is `seedance2.0_vip`; duration 4-12s for `seedance1.5pro`, 4-15s for Seedance 2.0 family.
- `multiframe2video`: uploads 2-20 local images; exactly 2 images can use shorthand `--prompt` and `--duration`; 3+ images require repeated `--transition-prompt` and optional `--transition-duration`; segment duration is limited to 0.5-8s and total duration must be at least 2s.
- `multimodal2video`: uploads local images, videos, and audio; requires at least one image or video; supports up to 9 images, 3 videos, and 3 audio files; audio inputs must be 2-15s; model versions `seedance2.0`, `seedance2.0fast`, `seedance2.0_vip`, `seedance2.0fast_vip`, `seedance2.0mini`; duration 4-15s.

Task/account:

- `login` / `relogin`: OAuth Device Flow; `--headless` prints authorization material and exits; `login checklogin --device_code=<device_code> --poll=30` completes later.
- `user_credit`: requires login.
- `session`: create/list/search/rename/delete sessions; session `0` is the default.
- `query_result`: query by `submit_id`; `--download_dir` downloads result media.
- `list_task`: filter by `gen_status`, `gen_task_type`, `submit_id`, `limit`, and `offset`.

## Command Selection

Always inspect help before real use:

```bash
dreamina -h
dreamina <subcommand> -h
```

High-level route:

- Use `text2image` for prompt-only image generation.
- Use `image2image` for image-guided image editing or transformation.
- Use `image_upscale` for upscaling.
- Use `text2video` for prompt-only video generation.
- Use `image2video` when one main image drives the clip.
- Use `frames2video` when first and last frames are both important.
- Use `multiframe2video` when multiple images should become one coherent story video.
- Use `multimodal2video` for the broadest reference mode across images, video, and audio when supported.
- Use `query_result` with a returned submit id for async follow-up.
- Use `list_task` to inspect saved task history.

## Model Rule

Do not hardcode model support.

If the user specifies a model, inspect the relevant subcommand help before running it:

```bash
dreamina <subcommand> -h
```

Confirm whether that command exposes model selection, whether the requested model is supported, and what constraints apply to duration, ratio, resolution, quantity, reference inputs, or `model_version`.

If the user asks for "all models", first inspect CLI help/model options and report what is actually exposed by the installed CLI. Do not promise hidden models.

## SW Routing

Default route after SW activation:

```text
upstream Studio role if needed -> Selected Asset Packet if a concrete object is selected -> prompt-director -> dreamina-cli
```

Examples:

- poster/key visual through Dreamina image generation: poster/layout/asset role if needed -> `prompt-director` -> `dreamina-cli`
- storyboard first frame through Dreamina image generation: `storyboard-director` -> optional `cinematographer` -> Selected Asset Packet -> `prompt-director` -> `dreamina-cli`
- selected video shot through Dreamina video generation: video/storyboard/edit role if needed -> Selected Asset Packet -> `prompt-director` -> `dreamina-cli`

Do not bypass upstream Studio roles. If the same user request asks for script, storyboard, camera language, edit rhythm, sound, color, poster layout, deck design, character, product, prop, or scene design, finish that handoff first.

## Local Media

Prefer passing local file paths directly only if the installed CLI help says the subcommand accepts local files.

If a downstream mode requires public URLs instead of local files, route through `url-relay` after the privacy/upload gate:

```text
prompt-director -> url-relay -> dreamina-cli
```

## Async Success Rule

Do not rely on shell exit code alone.

For submit commands, treat submission as successful only when the CLI output includes a usable `submit_id` and status indicates querying or success. If the status is failure, inspect and report the concrete failure reason.

For async tasks:

1. Save the `submit_id`.
2. Query with `query_result`.
3. Download to a local output folder only when appropriate.
4. Report whether the output exists, not only that submission was accepted.

## Login Rule

If login is required, use the CLI login flow. If the CLI prints a verification URL, user code, device code, or QR path, present exactly enough information for the user to complete login.

When login completes, explicitly tell the user whether it succeeded, reused an existing session, or failed. Do not stop silently after displaying login material.

## Fallback

- If `dreamina` is not installed: report that the CLI is not installed and offer the official install command for confirmation.
- If login is missing or expired: run or propose login/relogin.
- If credits are insufficient: keep the prompt and handoff, then ask whether to change account/tool.
- If a model or parameter is unsupported: use the installed CLI help to choose a supported alternative or return a prompt-only handoff.
- If generation fails: preserve the universal prompt, tool prompt, selected asset packet, command intent, and failure reason.

## Trace

Use a separate tool trace, not a Studio role:

```text
Tool skill: Dreamina CLI / `dreamina-cli` (loaded by explicit user request).
```
