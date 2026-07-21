# Tool Official Prompt Deltas

This compact file stores prompt lessons distilled from official tool docs. It is not a full manual. Load it only when a named tool is being converted, the user asks for official prompt cases, or prompt execution keeps failing.

## Low-Token Use

- Read only the relevant tool section.
- Keep the universal SW prompt first, then add the tool delta.
- Do not paste full official examples into project replies.
- Do not let tool-specific syntax bypass `storyboard-director`, `cinematographer`, `prompt-director`, or review roles.

## Seedance / Volcano Ark

Use this delta when the user explicitly asks for Ark Seedance / Seedance 2.0 generation or asks for a Seedance-ready prompt. If the user asks for the official Dreamina/Jimeng CLI, use the Dreamina CLI section instead.

- Choose mode first: `text-to-video`, `image-to-video` / `firstFrame`, `firstLastFrame`, or extension/edit when supported by the current runner.
- Pure text-to-video does not need an image URL. Public `http(s)` image URLs are required only when using reference image, first frame, first/last frame, or local media relayed through URL Relay.
- One prompt should describe one executable clip, not a full edit. Split multi-shot ideas into separate clips plus an edit plan.
- Include: duration, ratio, subject, action, scene, camera path, lighting, color mood, speed, continuity locks, and text/logo avoidance.
- If using a reference image, do not over-describe the whole image. State what should move, what must stay unchanged, where the camera goes, and how the clip ends.
- If using a Storyboard Animatic Sheet as the reference, treat the storyboard image as `motion source + structure`, not as a style image. The prompt should say that the storyboard is the primary source of truth, every panel is consecutive, panel order is mandatory, and no alternative coverage should be invented.
- Convert the sheet's Panel Headers, Camera + Lens Plan, Action Path, Rhythm Track, Escalation Map, State Track, and Style Track into a concise `PANEL BEATS` list. Do not ask Seedance to reproduce the physical paper sheet, panel borders, masthead, labels, or director strip.
- For this storyboard-locked mode, include separate reference roles when available: character sheet = identity, environment reference = scene geography/style, storyboard sheet = motion source + structure.
- Keep draft defaults cheap: `720p`, one selected clip, no batch, no long retry loop unless confirmed.
- QA after output: subject stability, unwanted text, logo errors, motion jumps, aspect ratio, usable first/last frames, and whether the clip cuts well.

## Dreamina CLI / Jimeng Official CLI

Use this delta when the user explicitly asks for Dreamina CLI, Jimeng CLI, official Jimeng CLI, `dreamina`, `@dreamina-cli`, 即梦官方 CLI, or image/video generation through the official Jimeng/Dreamina CLI.

- Choose command family first: `text2image`, `image2image`, `image_upscale`, `text2video`, `image2video`, `frames2video`, `multiframe2video`, `multimodal2video`, `query_result`, or `list_task`.
- Do not hardcode model names, duration limits, resolution tiers, output counts, or parameter names. Before real use, inspect `dreamina -h` and the relevant `dreamina <subcommand> -h`.
- Convert the universal SW prompt into one executable command's prompt and parameters. Split multi-shot or multi-asset ideas into separate tasks plus an edit plan.
- Keep the upstream handoff intact: selected object, reference roles, locked items, avoid list, aspect ratio, duration, and privacy/cost gate must survive tool conversion.
- For local references, use local file paths only when the current CLI help confirms support. If the CLI requires public URLs, route the file through URL Relay before generation.
- Do not run installer, login/relogin, real generation, private upload, batch generation, final-output generation, 4K/1080p/final delivery, or long unattended polling without confirmation.
- For async tasks, submission is not delivery. Record the returned `submit_id`, query the task, download or locate usable output, then claim generation is complete.
- QA after output: image/video exists, count/duration/resolution match the request, audio status is known when relevant, no black/failure frames, and the result follows the selected prompt/handoff.
- Fallback: if CLI is missing, login is missing, help is unavailable, or the requested model/parameter is not supported, keep a prompt-only handoff and do not claim output was generated.

## Kling 2.6-3

Use this delta for Kling / 可灵 2.6-3 prompt optimization, especially when the user asks about camera motion, image-to-video, start/end frames, or audio-video prompts.

- Prompt order: subject -> subject action -> scene -> camera/lens -> light/mood -> sound layer -> constraints.
- For image-to-video, let the source image carry appearance and composition. The prompt should focus on motion, camera, expression/action changes, and what must remain stable.
- For start/end-frame workflows, make sure the two frames share subject identity, angle logic, lighting, and scene geometry. Avoid asking the model to bridge impossible spatial changes.
- For camera control, prefer the tool's camera-control UI or supported parameter controls when available; prompt-only camera language is advisory.
- For "steady push-in", write a controlled path: locked horizon, fixed camera height, dolly/slider/gimbal feel, constant speed, no handheld shake, no sudden reframing, stable subject scale change. If it still shakes, switch to tool camera control, start/end frames, or post-production push-in.
- For Kling 2.6-3 audio-video, add only the needed audio layer: narration, dialogue, singing/rap, ambience, object/action sound, or a simple mix. Do not add audio instructions to silent clips.
- Motion Brush / Static Brush belongs to a tool operation, not a generic prompt. Use it only when the workflow actually supports masks/brushes.

## Banana Pro / Gemini Image

Use this delta when the user explicitly asks for Banana Pro, Nano Banana, Gemini image, or imagegen-style prompt polishing based on official image-generation guidance.

- Use natural language with clear intent. Prefer a short visual brief over a keyword pile.
- Include: goal, subject, composition, setting, style, camera/lens feel, light direction, color palette, aspect ratio, and constraints.
- For edits, say exactly what changes and what stays unchanged: `change only X; keep subject identity, pose, background perspective, lighting direction, and color palette unchanged`.
- For multiple references, assign each reference a role: character, product, scene, composition, texture, typography style, or color mood. Do not let one reference silently control every attribute.
- For poster display lettering, short hero text can be part of the image if it is a visual title effect. Exact small text, QR, legal copy, and logo still require post-production QA.
- Revise one variable at a time when possible. Keep locked parameters visible to reduce drift.
- QA after output: subject identity, hands/face/product structure, extra objects, bad text, wrong logo, layout-safe space, and whether post-production text can be added cleanly.

## OpenAI Image Generation / Image Editing

Use this delta for OpenAI image generation or image editing requests.

- Separate generate vs edit. For edit, define the target area, desired change, and protected areas.
- Use a direct natural-language instruction. Include output size/aspect, subject, composition, material, lighting, and negative constraints.
- When editing an existing image, explicitly preserve identity, product shape, perspective, shadows, reflections, and background continuity unless those are the target change.
- Do not rely on generated images for exact long text, QR codes, or legal copy. Treat text as a QA item.
- For transparent-background or cutout needs, state the background/output requirement directly and check edges after generation.

## Stable Camera Failure Fallback

When AI video keeps shaking despite a stable-camera prompt:

1. Prefer native camera controls or motion-control features if the tool offers them.
2. Use a first frame and last frame derived from the same image/scene, with only scale/position changed.
3. Generate a larger still and do the push-in in post-production or a 2.5D/compositing workflow.
4. Shorten the clip and reduce scene complexity.
5. If the shot must be perfectly stable, do not spend repeated video generations before testing a deterministic post path.

## Output Contract

For named tools, output this compact shape:

```text
Universal prompt:
Tool delta:
Key params:
Locked items:
Negative/avoid:
Post-generation QA:
Fallback if it fails:
```
