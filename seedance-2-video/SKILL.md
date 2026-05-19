---
name: seedance-2-video
description: Generate video clips through Volcano Ark Seedance 2.0 / 即梦2.0 from Chinese video prompts, public image URLs, or local image/video files uploaded through SW URL Relay. Use only when the user explicitly asks for 即梦2.0生成, 即梦生成, Seedance 2.0, Ark Seedance, 豆包 Seedance, @seedance-2-video, or this video-generation member. Do not trigger for generic storyboard, edit-plan, film planning, or video prompt requests unless the user asks to generate/execute with Seedance/即梦.
---

# Seedance 2.0 Video

## SW Operating Principle

Use this skill as an explicit video-generation tool after SW has prepared the creative handoff.

It is not a Studio role and is not a story planner. It does not replace `storyboard-director`, `cinematographer`, `edit-director`, `prompt-director`, `colorist`, or `review-producer`.

Default route:

```text
upstream Studio role if needed -> prompt-director -> seedance-2-video
```

If the user asks for storyboard, film/video structure, shot design, motion design, edit rhythm, character/product/scene planning, or prompt writing and also says to use 即梦/Seedance, finish the upstream design first, then convert only the selected shot or clip into a Seedance-ready prompt.

If the user already provides a final video prompt and the needed public image URL, use `prompt-director` only for a quick prompt sanity check, then run this tool.

## Security Rule

Never write a real API key into this skill, generated files, prompts, manifests, logs, or examples. Read the key from `ARK_API_KEY` first, then from the local private key file created by `setup-key`.

If no key is available, run `dry-run` only and say that no real video was submitted. Do not claim a video was generated.

Each user can either set an environment variable:

```powershell
# Set ARK_API_KEY in your local environment or private key file; do not paste the value into repo files.
```

Or run a one-time local setup command:

```bash
python scripts/seedance_task.py setup-key
```

`setup-key` saves the key to `~/.config/codex-seedance-2-video/secrets.json` with private file permissions. This file is outside the shareable skill folder.

For employee distribution, prefer the wrapper:

```bash
scripts/install_employee_key.sh
```

It hides key input, writes the same local private file, and runs `doctor` after installation.

Optional:

```bash
export ARK_BASE_URL="https://ark.cn-beijing.volces.com"
```

## Default Contract And Cost Gate

- Provider: Volcano Ark direct API.
- Model: `doubao-seedance-2-0-260128`.
- Submit endpoint: `POST /api/v3/contents/generations/tasks`.
- Poll endpoint: `GET /api/v3/contents/generations/tasks/{task_id}`.
- Auth: `Authorization: Bearer <local key>`, loaded from `ARK_API_KEY` or the private `setup-key` file.
- Input images: 1-9 public `http` or `https` URLs are required by the bundled runner. Do not pass local paths; Ark must fetch the media itself.
- Local files: pass local references with `--image-file`; the runner uploads them through SW URL Relay first and then sends the returned public URL to Ark.
- Temporary relays: use the configured SW media uploader first. If it is unreachable or returns a server-side failure and the user/config allows fallback, use Catbox/Litterbox only after reporting that the SW server is unavailable. Missing token or config errors do not trigger fallback.
- Default video settings: `ratio=9:16`, `duration=15`, `resolution=720p`, `watermark=false`, `seed=-1`.
- Output: `final.mp4` and `run_manifest.json` in the selected output directory.
- Cost lane: dry-run is low-cost; real generation is high-cost and queue-based.
- Default generation scope: one selected clip or shot. Batch generation, multiple ratios, 1080p, or long retry loops require explicit confirmation.

Before real generation, confirm these fields are known or reasonably defaulted:

- `prompt`: Chinese, one clip/shot, no overloaded multi-scene sequence.
- `ratio`: usually `9:16`, `16:9`, or `1:1`.
- `duration`: default `15`.
- `resolution`: default `720p` for draft speed; use `1080p` only when final quality is worth the cost.
- `image-url`: at least one public `http(s)` URL.
- `image-file`: optional local file input when a public URL is not yet available. Use only after privacy/upload guardrails are satisfied.
- `allow-temporary-relay-url`: only for user-confirmed third-party temporary relay URLs already supplied as public URLs.
- `temporary-relay-fallback`: only after user confirmation or private config; it is tried after SW URL Relay fails, with `auto` currently choosing Litterbox.
- `output-dir`: project-specific output folder.

## Prompt Contract

Seedance prompts should be compact and concrete:

- One clip per prompt.
- Specify subject, action, scene, camera movement, composition, lighting, color, atmosphere, duration, and constraints.
- Replace vague wording such as "更电影感" with controllable choices: lens feel, camera path, light direction, contrast, depth of field, color temperature, pace, and frame size.
- Avoid asking the model to create accurate small text, logos, QR codes, legal copy, or exact subtitles. Add those in editing/post.
- For historical projects, if Historical Accuracy is enabled, check visible costume, architecture, props, symbols, materials, and anachronisms before generation and again when reviewing stills or output frames.

## Workflow

1. Read `references/ark-seedance-api.md` when you need exact payload shape, status parsing, or troubleshooting details.
2. For first-time setup on a new machine, save the key locally:

   ```bash
   python scripts/seedance_task.py setup-key
   ```

3. Run a dry payload check before spending credits, or whenever the key is missing:

   ```bash
   python scripts/seedance_task.py dry-run \
     --prompt "15秒，电影感文旅镜头，晨光中无人机缓慢推进古城街巷，石板路反光，行人自然穿行，暖色低对比，无文字，无logo。" \
     --image-url https://example.com/source.png
   ```

4. Check environment and optional image URLs:

   ```bash
   python scripts/seedance_task.py doctor \
     --image-url https://example.com/source.png
   ```

   For a local reference file that needs URL relay:

   ```bash
   python scripts/seedance_task.py doctor \
     --image-file ./source.png
   ```

5. Submit, poll, download, and write the manifest only after the user confirms real generation:

   ```bash
   python scripts/seedance_task.py run \
     --prompt-file video_prompt.txt \
     --image-url https://example.com/source.png \
     --output-dir outputs/seedance-demo
   ```

   Or with the SW URL Relay:

   ```bash
   python scripts/seedance_task.py run \
     --prompt-file video_prompt.txt \
     --image-file ./source.png \
     --output-dir outputs/seedance-demo
   ```

6. If the task is queued for a long time or a session is interrupted, continue with:

   ```bash
   python scripts/seedance_task.py poll \
     --output-dir outputs/seedance-demo
   ```

## Slow Queue Behavior

Seedance video generation can queue for hours. The script uses slow adaptive polling:

- 0-2 minutes: every 15 seconds.
- 2-15 minutes: every 45 seconds.
- After 15 minutes: every 120 seconds.
- If the provider returns queue or estimated wait fields, record them in `run_manifest.json`; do not fail when those fields are absent.

Use `--submit-only` when the user wants a fast handoff and can poll later.

## Resource Guide

- `scripts/seedance_task.py --help`: commands and arguments, including `setup-key`.
- `../url-relay/SKILL.md`: SW public URL relay policy for local media handoff.
- `scripts/install_employee_key.sh --help`: one-command employee key setup wrapper.
- `references/ark-seedance-api.md`: Ark endpoint, payload, response parsing, and image URL rules.
