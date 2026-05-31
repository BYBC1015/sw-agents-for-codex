---
name: feishu-docs
description: Render or publish SW visual plans, storyboard packages, and selected design handoff Markdown into Feishu/Lark Docs. Use only when the user explicitly asks to 转到飞书, 同步到飞书, 发布到飞书, 飞书视觉方案, 飞书分镜, Lark Docs, Feishu Docs, @feishu-docs, or to package an already-prepared visual方案/storyboard into a Feishu-readable document. Do not use for ordinary storyboard planning, prompt writing, image/video generation, or DOCX export.
---

# Feishu Docs

## Purpose

Turn an already-prepared SW handoff into a Feishu/Lark document route.

This is a downstream delivery tool, not a Studio role. It does not create the storyboard, select images, write prompts, generate images, or replace `storyboard-visual-word`. Use it after the upstream visual plan, storyboard, selected images, or Markdown handoff already exists.

Preferred uses:

- Visual director plans.
- Storyboard packages.
- Scene/character visual references.
- Reviewable handoff notes where a Feishu table-of-contents document is easier to browse than chat.

## Routing

Use only on explicit request:

```text
upstream Studio role if needed
-> Selected Asset Packet (when selected images/media are part of the handoff)
-> finishing-producer if delivery naming/package matters
-> feishu-docs
```

If visuals or storyboard content are not ready, route upstream first. Do not fabricate image selections or publish incomplete work just because Feishu was mentioned.

If a Selected Asset Packet is present, use it to preserve the selected visual set, reference roles, locks, avoid list, and privacy/cost decision. Do not publish local paths, raw prompts, tool parameters, or private media unless the user explicitly requests an internal appendix or confirms external sharing.

Display as a tool skill, not a Studio role:

```text
Tool skill: Feishu Docs / `feishu-docs` (loaded for explicit Feishu handoff).
```

## Privacy And Cost

- Publishing to Feishu/Lark sends content to an external workspace. Ask or confirm before publishing private client material, faces, unreleased products, brand assets, internal prompts, or local file paths.
- Rendering a Feishu-ready Markdown file is local and low-cost.
- Real API publish requires a local private Feishu/Lark app config. Never write app secrets or tenant tokens into the repository, prompts, logs, or final deliverables.
- Native image upload is not assumed in the first pass. Prefer public image URLs from `url-relay` or user-provided URLs when image visibility in Feishu is required.

## Local Config

Private config path:

```text
~/.config/sw-feishu/config.json
```

Supported config/env values:

- `FEISHU_APP_ID`
- `FEISHU_APP_SECRET`
- `FEISHU_FOLDER_TOKEN` (optional default folder)
- `FEISHU_BASE_URL` (defaults to `https://open.feishu.cn/open-apis`; use Lark base URL when needed)

One-time setup:

```powershell
python .\feishu-docs\scripts\feishu_doc_cli.py setup --app-id <app_id> --folder-token <folder_token>
```

The script prompts for the app secret without echoing it when it is not provided through the environment.

## Commands

Check local setup without publishing:

```powershell
python .\feishu-docs\scripts\feishu_doc_cli.py doctor --no-network
```

Render a Feishu-friendly Markdown file:

```powershell
python .\feishu-docs\scripts\feishu_doc_cli.py render --input .\handoff.md --output .\handoff_feishu.md --title "Visual Plan" --mode storyboard
```

Preview a publish plan without sending content:

```powershell
python .\feishu-docs\scripts\feishu_doc_cli.py publish --input .\handoff_feishu.md --title "Visual Plan"
```

Real publishing requires explicit execution:

```powershell
python .\feishu-docs\scripts\feishu_doc_cli.py publish --input .\handoff_feishu.md --title "Visual Plan" --execute
```

## Output Rules

- Prefer a clean table of contents and section headings.
- Keep each storyboard group compact: group title, overview image/link, cells, prompt/code block only when the user asks for an internal production document.
- For formal/client-facing Feishu docs, do not expose raw prompts, local file paths, generation payloads, or tool parameters unless the user asks for an internal appendix.
- If images are local and no public URL exists, render placeholders rather than pretending Feishu can display them.
- If Feishu credentials are missing, provide render/dry-run output only and state that no document was published.

## Failure Fallback

If Feishu API publishing fails:

1. Keep the Feishu-ready Markdown output.
2. Report the API stage that failed without printing secrets.
3. Suggest manual import/paste into Feishu or retry after app permission repair.
4. Do not retry repeatedly or publish to another external platform unless the user asks.
