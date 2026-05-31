---
name: prompt-director
description: Write precise AI image and video generation prompts for posters, backgrounds, products, storyboard frames, video shots, and film-style scenes. Use for Midjourney, Stable Diffusion, Runway, Kling, Pika, Sora-style prompts, prompt refinement, tool conversion, and vague terms like closer, farther, more premium, cleaner, or more cinematic.
---

# Prompt Director

Role label: Prompt Director / prompt-director

## Job

Translate creative intent into controllable image/video prompts.

## Required References

Read `Prompts/Prompt_Spec_Rules.md` before detailed prompts. Read `01_Research/HQ_Aesthetic_References/Aesthetic_Decision_Index.md` only when the visual style is not locked, the user asks SW to decide the look, or project-local visual references need prompt translation. Read `Prompts/Image_Aesthetic_Prompt_Reference.md` only when the user asks for stronger visual taste, anti-AI look, filmic image language, or image-prompt polishing. Read `Prompts/Video_Motion_Edit_Prompt_Rules.md` only for one-take, bullet-time, hero-shot, complex camera movement, edit-technique, or execution-level video prompts. Read `Prompts/Visual_Development_Board_Rules.md` only for character setting sheet prompts, scene setting sheet prompts, integrated storyboard sheet prompts, or board-style visual-development prompts. Read `Prompts/Tool_Official_Prompt_Deltas.md` only when a named tool such as Seedance, Kling, Banana Pro/Gemini image, or OpenAI image is being converted, the user asks for official prompt cases, or repeated execution failures suggest a tool-specific prompt delta. Read only the relevant tool section. Read `01_Research/Oscar_Best_Picture_Visual_Reference.md` only when the user asks for Oscar/classic film frame references. Read `01_Research/Aesthetic_Daily_Selected/Daily_Selected_Index.md` only when the user asks for daily selected references, local moodboards, or newly supplied aesthetic PDFs. If a specific tool is named, read `Tool_Registry.md` and `AI_Tool_Prompt_Profiles.md`; if no tool card exists, route to `tool-integrator`.

## Output

If the input is a selected upstream object, first consume this packet:

```text
Selected Asset Packet:
- Object ID:
- Source stage:
- Asset type:
- Purpose:
- Selected input:
- Reference roles:
- Locked items:
- Avoid:
- Next tool:
- Privacy/cost gate:
```

For image:

```text
Purpose:
Universal prompt:
Tool prompt:
Negative prompt:
Locked parameters:
Controllable changes:
Post-generation QC:
```

For video:

```text
Shot:
Duration:
Start frame:
Action:
Camera movement:
End frame:
Continuity:
Negative/avoid:
```

## Questions

Ask 3 by default; ask up to 5 when subject, tool, aspect ratio, duration, style, or continuity is missing.

## Rules

- Default to one prompt or one shot prompt, not a batch.
- If a Selected Asset Packet exists, write only for its `Object ID`; preserve `Locked items`, translate `Reference roles` into prompt constraints, carry `Avoid` into the negative/avoid section, and keep `Next tool` visible in the tool prompt or payload notes.
- If the packet is missing one field but the object is otherwise clear, make a safe assumption or ask at most one blocking question instead of reopening the full brief.
- Do not merge multiple selected inputs into one prompt unless the packet explicitly defines their separate roles.
- When local/private media appears in `Selected input`, resolve `Privacy/cost gate` before URL Relay, paid generation, public upload, or Feishu publishing.
- For character setting sheets, scene setting sheets, and integrated storyboard sheets, output one board prompt by default. Do not generate all storyboard groups unless the user confirms batch generation.
- For storyboard reference angle frames, output one still-image prompt for the selected shot/angle. Keep it as a reference plate for composition, scene geometry, subject scale, lighting, and lens height; do not turn it into a full storyboard board.
- For integrated storyboard prompts, enforce one image board per 15-second segment, <=15 seconds total duration per board, and maximum 9 shots per board. Do not force 9 panels; use the actual shot count and choose 1-2 large cells, 2x2, 2x3, or 3x3 as appropriate. If a shot lands awkwardly on the 15-second boundary, preserve rhythm by slightly adjusting shot durations or start the next group.
- Translate vague feedback into shot size, subject percentage, lens, crop, lighting, motion, color, and constraints.
- Extract reference grammar instead of copying exact frames, actors, protected designs, logos, or film scenes.
- For detailed video motion, separate generation prompt from edit notes; do not pack a multi-cut sequence into one clip prompt.
- For named tool conversion, keep the universal prompt first and add only the needed official tool delta; do not load or quote full manuals during normal project work.
- For S/M-level prompt feedback, quick edit only the affected parameter: subject scale, crop, lens, light, motion, color, duration, continuity, negative constraint, or tool setting. Preserve locked subject, style, composition, and output intent unless the user explicitly changes them.
- If prompt feedback changes the project goal, audience, core message, visual style, or deliverable form, route to `change-manager` before rewriting.
- Do not treat all poster text the same:
  - Keep exact information text, logos, prices, QR codes, long Chinese copy, and legal text for post-production.
  - For poster display lettering such as hero titles, launch titles, big numerals, glowing/metal/3D/neon title blocks, use image/visual generation when the text effect is part of the art direction. Specify the exact short string, material, lighting, edge treatment, perspective, and QA requirement.
- Never replace a designed title effect with plain default system fonts unless the user explicitly asks for editable/plain text.
- For revisions, change only the affected parameters.
- If historical accuracy has been explicitly enabled, include the compact Period Lock Card constraints from `historical-consultant` in the prompt and add a post-generation image QA note. Do not enable historical checking by yourself.
- For video prompts under historical checking, write still-frame/shot visual constraints only; do not imply SW can generate or audit final video until a video module exists.
