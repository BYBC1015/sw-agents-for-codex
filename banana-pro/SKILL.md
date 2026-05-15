---
name: banana-pro
description: Generate images with Banana Pro / Nano Banana 2 through OpenRouter after SW prompt preparation, including text-to-image, image-to-image, multi-reference images, character sheets, clean scene plates, product or prop design images, and storyboard first frames. Use only when the user explicitly asks for 香蕉, banana, Banana Pro, Nano Banana, OpenRouter image generation, @banana-pro, or asks SW to use this image-generation member. Do not trigger for generic image prompt requests unless the user asks to generate or execute them with Banana Pro.
---

# Banana Pro

## Role

Act as SW's explicit image-generation member after upstream studio work and `prompt-director`.

Use `scripts/generate_openrouter_image.py` to generate images through OpenRouter when:

- the user explicitly asks for 香蕉 / banana / Banana Pro / Nano Banana / `@banana-pro`
- the user wants actual image generation, not only a prompt
- the needed upstream deliverable already exists, such as a locked poster visual direction, slide/page visual brief, storyboard shot, character sheet, product/prop brief, or final visual prompt
- `OPENROUTER_API_KEY` is available in the environment
- high-cost and upload/privacy guardrails are satisfied

The script reads `OPENROUTER_API_KEY` from the process environment and, on Windows, also falls back to the current user's environment variable registry value. If the key is missing, run dry-run or provide the ready payload; do not claim an image was generated.

For speed, do not run a separate key-check command before every generation. Let the runner check the key; after one successful key-readable check or one successful generation in the current conversation, treat the key as available unless the runner reports otherwise.

## Execution Defaults

Default model and settings:

```json
{
  "model": "google/gemini-3.1-flash-image-preview",
  "modalities": ["image", "text"],
  "stream": false,
  "image_config": {
    "aspect_ratio": "16:9",
    "image_size": "1K"
  }
}
```

Prefer `16:9` for storyboard frames, cinematic frames, product demos, UI references, and video first frames. Use user-specified aspect ratio and image size when provided. Default to `1K` for draft speed and cost control; use `2K` or `4K` only when the user asks for final/high-resolution output or the project already passed review.

## No-Bypass Rule

Banana Pro must not skip SW's design pipeline.

- If the user says "design storyboard and use banana to generate", first route to `storyboard-director` for the shot table, then `prompt-director` for the selected shot prompt, then Banana Pro for actual image generation.
- If the user asks for poster design plus Banana output, first route through the poster/art/layout decision needed for a usable visual brief, then `prompt-director`, then Banana Pro.
- If the user asks for PPT/deck pages plus Banana output, first route through `presentation-designer` or `layout-designer` to define page role and visual need, then `prompt-director`, then Banana Pro.
- If the user directly provides a complete final prompt and explicitly says to use Banana, Banana Pro may run without extra upstream roles.
- Generate only the selected frame/image by default. Do not render every storyboard frame unless the user explicitly confirms batch generation.

## Workflow

1. Confirm explicit trigger.
   - Trigger words include: 香蕉, banana, Banana Pro, Nano Banana, OpenRouter image generation, `@banana-pro`.
   - Generic image prompt requests stay with SW's `prompt-director`.

2. Check the handoff quality.
   - Required handoff fields: purpose, subject, scene, composition or shot size, lighting/color, aspect ratio, constraints, and whether this is draft or final.
   - If the request includes an upstream task such as storyboard, video, film, poster, deck, slide, layout, character, product, or prop work, do not generate until the responsible Studio role has produced a usable handoff.
   - If the handoff is underspecified, ask at most one blocking question or produce a low-cost preflight.

3. Use the final visual prompt from `prompt-director`.
   - Keep commercial text, logos, QR codes, and exact Chinese copy for post-production unless the user explicitly asks otherwise.

4. Select pattern only when needed.
   - Read `references/prompt-patterns.md` for text-to-image, image-to-image, multi-reference, character sheet, clean scene plate, product/prop, or storyboard first-frame templates.
   - Read `references/openrouter-direct.md` only for raw payload/API details or troubleshooting.

5. Generate or dry-run.
   - If generation is confirmed and `OPENROUTER_API_KEY` exists, resolve the script relative to the loaded `banana-pro/SKILL.md`, then run:

```powershell
python <banana-pro-skill-dir>\scripts\generate_openrouter_image.py --prompt "<final prompt>" --aspect-ratio "16:9" --image-size "1K"
```

   - For references, add `--reference-image <local-path>` or `--reference-url <url>`.
   - For final-quality output, set `--image-size "2K"` or `--image-size "4K"` only after the user has confirmed the draft direction.
   - If key is missing or user only wants setup, run with `--dry-run` and provide the payload path.
   - The script stores outputs under `banana_outputs/<topic>-<timestamp>` unless `--output-dir` is provided, saves both full and compressed prompts, and retries once with a simpler prompt if the API returns no image.

6. Return concise result.
   - If generated: show the image inline when possible, saved image path(s), settings, and one-line QA.
   - If missing key: state `OPENROUTER_API_KEY` is missing and give the payload path.
   - Never expose API keys or raw secret values.

## Output Shape

```markdown
Studio roles: Prompt Director / `prompt-director` (loaded). Cost lane: high-cost.
Tool skill: Banana Pro / `banana-pro` (loaded by explicit user request).

Banana Pro result:
- status:
- image: ![Banana Pro output](absolute-path)
- settings:
- file:
- QA: one concise line
```

## Guardrails

- Ask before consuming quota, uploading private references, or generating final-use brand/face/product assets.
- Treat an explicit phrase such as "use banana to generate one draft" as confirmation for one draft image only; still pause for private uploads, final brand/face/product assets, or batch generation.
- Do not use `banana-pro` for ordinary prompt drafting.
- Do not use `banana-pro` to replace `storyboard-director`, `poster-art-director`, `presentation-designer`, `layout-designer`, `asset-producer`, or `prompt-director`.
- Do not say an image was generated unless the script returned saved image files.
- If the API returns no images after the built-in retry, report the response path and suggest prompt simplification.
