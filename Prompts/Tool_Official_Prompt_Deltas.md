# Tool Official Prompt Deltas

This compact file stores prompt lessons distilled from official tool docs. It is not a full manual. Load it only when a named tool is being converted, the user asks for official prompt cases, or prompt execution keeps failing.

## Low-Token Use

- Read only the relevant tool section.
- Keep the universal SW prompt first, then add the tool delta.
- Do not paste full official examples into project replies.
- Do not let tool-specific syntax bypass `storyboard-director`, `cinematographer`, `prompt-director`, or review roles.

## Seedance / Jimeng / Volcano Ark

Use this delta when the user explicitly asks for Seedance / 即梦2.0 generation or asks for a Seedance-ready prompt.

- Choose mode first: `text-to-video`, `image-to-video` / `firstFrame`, `firstLastFrame`, or extension/edit when supported by the current runner.
- Pure text-to-video does not need an image URL. Public `http(s)` image URLs are required only when using reference image, first frame, first/last frame, or local media relayed through URL Relay.
- One prompt should describe one executable clip, not a full edit. Split multi-shot ideas into separate clips plus an edit plan.
- Include: duration, ratio, subject, action, scene, camera path, lighting, color mood, speed, continuity locks, and text/logo avoidance.
- If using a reference image, do not over-describe the whole image. State what should move, what must stay unchanged, where the camera goes, and how the clip ends.
- Keep draft defaults cheap: `720p`, one selected clip, no batch, no long retry loop unless confirmed.
- QA after output: subject stability, unwanted text, logo errors, motion jumps, aspect ratio, usable first/last frames, and whether the clip cuts well.

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
