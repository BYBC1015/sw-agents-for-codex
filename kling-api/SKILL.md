---
name: kling-api
description: Generate and manage Kling AI / 可灵 official API video tasks. Use when the user explicitly asks for Kling API, 可灵 API, 可灵生成, Kling video generation, text-to-video, image-to-video, multi-image-to-video, Omni-Video, Kling-V3-Omni, task polling, downloading Kling results, or creating a clean shareable Kling API skill for another team. Do not use for generic storyboard, video planning, or prompt writing unless the user asks to execute through Kling API.
---

# Kling API

Use this as a clean, standalone tool skill for the official Kling AI API. It does not depend on SW, project memory, URL Relay, or any private company workflow.

## Safety Contract

- Never write AccessKey, SecretKey, JWT token, generated Authorization header, or private media URLs into this skill, repo files, prompts, logs, or examples.
- Prefer `dry-run` before `run`. `dry-run` prints the payload shape without submitting a task.
- Real API submission can consume credits. Only use `run --yes` after the user explicitly confirms real generation.
- Local image files are encoded and transmitted to Kling during real `run`. Require `--confirm-upload` when using `--image-file` or `--image-tail-file` with `run`.
- Generated result URLs may expire. Download or transfer the final video after success.

## Setup

Use environment variables or a local private config file.

Environment variables:

```bash
KLING_ACCESS_KEY=...
KLING_SECRET_KEY=...
KLING_BASE_URL=https://api-beijing.klingai.com
```

One-time local setup:

```bash
python scripts/kling_task.py setup-key
python scripts/kling_task.py doctor
```

The private config is saved outside this skill folder at `~/.config/kling-api/secrets.json`.

## Official API Notes

Read `references/kling-api.md` when exact endpoint, parameter, model, status, or troubleshooting details matter.

Core verified official routes:

- `POST /v1/videos/text2video`, `GET /v1/videos/text2video/{task_id}`
- `POST /v1/videos/image2video`, `GET /v1/videos/image2video/{task_id}`
- `POST /v1/videos/multi-image2video`, `GET /v1/videos/multi-image2video/{task_id}`
- `POST /v1/videos/omni-video`, `GET /v1/videos/omni-video/{task_id}`
- Default base URL for China-region servers: `https://api-beijing.klingai.com`
- Auth: JWT signed with SecretKey, payload `iss=<AccessKey>`, then `Authorization: Bearer <token>`.
- Omni-Video supports model names such as `kling-video-o1` and `kling-v3-omni`; it uses prompt references like `<<<image_1>>>`, `<<<video_1>>>`, and `<<<element_1>>>`.
- The official Omni-Video payload does not expose `camera_control`; describe camera movement in the prompt or use a reference video with `refer_type=feature`.

## Workflow

1. Build or receive one final video prompt. Keep story planning and storyboard work outside this tool skill.
2. Run `dry-run` to inspect payload and defaults.
3. Run `doctor` if key, media path, or public URL readiness is uncertain.
4. Run `run --yes` only after real-generation confirmation.
5. If interrupted, resume with `poll`.

## Examples

Text-to-video dry run:

```bash
python scripts/kling_task.py dry-run \
  --kind text \
  --prompt "A calm cinematic product shot, slow dolly-in, blue rim light, no readable text." \
  --model-name kling-v2-6 \
  --duration 5 \
  --mode pro \
  --aspect-ratio 16:9 \
  --sound off
```

Image-to-video with a public first frame:

```bash
python scripts/kling_task.py dry-run \
  --kind image \
  --image-url https://example.com/first-frame.png \
  --prompt "The camera slowly pushes forward on rails, stable motion, no shake, soft morning light." \
  --duration 5 \
  --mode pro
```

Omni-Video dry run with `Kling-V3-Omni`:

```bash
python scripts/kling_task.py dry-run \
  --kind omni \
  --model-name kling-v3-omni \
  --image-url https://example.com/reference.png \
  --prompt "Use <<<image_1>>> as the visual reference. A stable slow forward camera move, rail-mounted feeling, no handheld shake." \
  --duration 5 \
  --mode pro \
  --aspect-ratio 16:9
```

Real submit after confirmation:

```bash
python scripts/kling_task.py run \
  --kind image \
  --image-url https://example.com/first-frame.png \
  --prompt-file video_prompt.txt \
  --duration 5 \
  --mode pro \
  --output-dir outputs/kling-shot-001 \
  --yes
```

Resume polling:

```bash
python scripts/kling_task.py poll --output-dir outputs/kling-shot-001
```

Use local image files only when the user understands they will be uploaded to Kling:

```bash
python scripts/kling_task.py run \
  --kind image \
  --image-file ./first-frame.png \
  --prompt-file video_prompt.txt \
  --output-dir outputs/kling-shot-001 \
  --confirm-upload \
  --yes
```

## Handoff Rules

For another team, share the whole `kling-api/` folder only. They must run `setup-key` locally with their own AccessKey and SecretKey.

If they already have a video workflow, add this skill after their prompt-preparation stage. Do not replace their creative planning, storyboard, legal review, or delivery review stages.
