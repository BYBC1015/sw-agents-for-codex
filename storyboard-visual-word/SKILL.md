---
name: storyboard-visual-word
description: Create clean Word/DOCX visual director handoff files from already-selected storyboard, scene, or concept images. Use only when the user explicitly asks for a 视觉方案文件, 视觉导演方案, Word视觉方案, DOCX视觉方案, 分镜视觉方案文件, or a polished client-facing visual bible with images embedded per scene. Do not use for ordinary storyboard planning, prompt writing, image generation, or integrated storyboard board design unless the user asks to package the selected visuals into a Word/DOCX file.
---

# Storyboard Visual Word

## Purpose

Turn an existing storyboard visual-director package into a clean `.docx` handoff. The final Word should read like a director's visual bible: scene split, each scene image, visual setting, and why the setting supports the story.

This is a downstream delivery tool. It does not create the full storyboard, choose the visual direction, generate images, or replace SW's `storyboard-director`, `production-designer`, `prompt-director`, Banana Pro, or Seedance.

Use this skill's script for the repeatable "scene images + rationale -> Word" layout. If an external document-rendering tool is available, use it for visual QA; otherwise use the script's structural DOCX inspection and state when full render QA was skipped.

## Canonical Output Rules

- Create one final Word file named like `[片名]_视觉导演方案.docx`.
- Embed each scene image into the DOCX; never leave local image paths as visible content.
- Put each scene's image directly under that scene title, followed by `视觉设定` and `为什么这样设定`.
- Do not include a standalone `Midjourney 提示词` section after images exist.
- Do not include `Midjourney Prompt`, raw `--ar` parameter text, or prompt bodies under scenes unless the user explicitly asks.
- Do not include a `生成结果` gallery/path table or any table like `场次 / 正选图 / 备注`.
- Avoid overview contact sheets in the formal Word unless the user explicitly asks for a contact sheet. The Word should be scene-by-scene, not a generation-results report.
- If generation failed and there are no images, deliver a prompt-only fallback separately; once images exist, remove prompt sections from the formal Word.
- If the user has not selected images yet, do not fabricate a Word file. Ask for selected image paths or route back to the relevant SW role to create/select visuals first.
- If Selected Asset Packets exist, use them to confirm selected images, scene/group ids, reference roles, locked items, avoid list, and privacy/cost gates. Do not expose packet internals, local paths, raw prompts, or tool parameters in the formal Word unless the user asks for an internal appendix.

## Workflow

1. Gather the clean source material.
   - Scene titles and shot/time ranges.
   - One selected image path per scene.
   - Per-scene narrative function, tone/light, visual symbols.
   - Per-scene `视觉设定` and `为什么这样设定`.
   - Brief QA notes.

2. Build a JSON spec for the script.
   - Use absolute image paths.
   - Do not include prompt text in the spec.
   - Keep metadata concise.

3. Generate DOCX with the bundled script:

```powershell
python .\storyboard-visual-word\scripts\build_scene_visual_docx.py `
  --spec C:\path\to\spec.json `
  --out C:\path\to\片名_视觉导演方案.docx
```

4. Validate the DOCX.
   - Check the script's validation output: embedded image count, no prompt text, no result/path table terms.
   - Run a render gate when `soffice`/LibreOffice or another DOCX preview/render tool is available.
   - If LibreOffice is unavailable, do structural QA by inspecting the DOCX zip: image relationships, media count, and visible text. State in the final response that full render QA was skipped because `soffice` was unavailable.

## Spec Shape

Use this JSON shape:

```json
{
  "title": "《片名》视觉导演方案",
  "subtitle": "分镜概念图 · Midjourney 16:9 电影帧 · 8 场景视觉设定",
  "metadata": [
    ["来源", "脚本分镜.docx"],
    ["抽取结果", "识别到 46 个镜头；合并为 8 个场景级概念图。"],
    ["生成状态", "已通过 Midjourney via Legnext 生成完成；本文嵌入每场概念图。"]
  ],
  "scenes": [
    {
      "title": "第1场｜雨后报警与疑案钩子",
      "range": "镜头 1-6｜00:00-00:24",
      "image": "/absolute/path/scene1.png",
      "function": "建立县城、报案、主持人钩子",
      "tone": "雨后蓝灰、湿地反光、派出所窗光",
      "symbols": "雨伞、湿地、派出所门口、窗影",
      "setting": "视觉设定正文。",
      "reason": "为什么这样设定正文。"
    }
  ],
  "qa": [
    "画幅已按 16:9 电影帧生成。",
    "事故、死亡、掩埋均以远景、剪影、反应、后果表达。"
  ]
}
```

## Layout Guidance

- Use a simple polished report style: title, metadata, scene split, then per-scene cards.
- Keep visual-design summary as prose/cards rather than wide tables when the Chinese text is long.
- Use only compact key-value tables inside each scene card: `叙事功能`, `色调/光线`, `视觉符号`.
- Insert page breaks so scene cards do not become cramped; two scenes per page is usually the upper limit for image-heavy docs.
- Use Chinese-capable fonts such as PingFang SC or Microsoft YaHei via Word style fallback, with Arial/Calibri as Latin fallback.

## Final Response

Return only the final `.docx` link unless the user asks for intermediate files. Mention render QA status only if render could not be completed or found an issue.

## SW Routing

Use after the visual package is ready:

```text
storyboard-director / production-designer / asset-producer if needed
-> Selected Asset Packet for each selected image/group
-> prompt-director if prompt/image generation is needed
-> banana-pro or other image tool if explicitly requested
-> storyboard-visual-word
```

Display as a tool skill, not a Studio role:

```text
Tool skill: Storyboard Visual Word / `storyboard-visual-word` (loaded for visual方案文件/DOCX handoff).
```
