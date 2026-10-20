# Feature Trigger Index

This compact index is for `@sw_help`, `/sw_help`, `/sw-help`, feature discovery, and low-cost trigger checks. It does not start a project by itself.

## Project Asset Graph

Purpose: compact project-level asset continuity map before storyboard.

Trigger after SW activation when:

- a new video, film, campaign story, product story, or storyboard project starts and recurring assets are not locked
- the user asks for a storyboard but characters, scenes, props, products, wardrobe, existing footage, or reference files are unclear
- a Seedance/Jimeng storyboard-locked sequence needs character/environment continuity before panel beats

Default route:

```text
production-designer -> Project Asset Graph -> storyboard-director
```

Ask only the useful asset questions: what already exists, what must be created, and what must stay locked. In fast mode, write assumptions and continue.

Do not confuse it with Selected Asset Packet. Project Asset Graph is project-level before storyboard; Selected Asset Packet packages one selected item for prompt/tool/document handoff.

## Banana Pro

Purpose: explicit image generation after SW prompt preparation.

Trigger only when the user explicitly asks for:

- `香蕉`
- `banana`
- `Banana Pro`
- `Nano Banana`
- `@banana-pro`
- OpenRouter image generation
- use Banana to generate/output an image

Default route:

```text
upstream Studio role if needed -> Selected Asset Packet if a concrete object is selected -> prompt-director -> banana-pro
```

Do not trigger for ordinary image prompt drafting.

## Dreamina CLI

Purpose: explicit Dreamina / Jimeng official CLI image and video generation after SW prompt preparation.

Trigger only when the user explicitly asks for:

- `Dreamina CLI`
- `Jimeng CLI`
- official Jimeng CLI
- `dreamina`
- `@dreamina-cli`
- official Jimeng/Dreamina CLI
- official Jimeng image generation
- official Jimeng video generation
- Jimeng image generation through the official CLI
- Jimeng video generation through the official CLI

Default route:

```text
upstream Studio role if needed -> Selected Asset Packet if a concrete object is selected -> prompt-director -> dreamina-cli
```

Do not trigger for ordinary image/video prompt drafting. Do not execute the installer, login/relogin, private upload, real generation, batch generation, or long polling without confirmation. If `dreamina` is not installed, report that the CLI is missing and offer the official install route.

Model behavior: do not hardcode supported models. Inspect `dreamina -h` and `dreamina <subcommand> -h` before real use.

## Kling CLI

Purpose: explicit Kling official CLI / MCP image and video generation after SW prompt preparation.

Use this route for the OAuth-based official Kling CLI/MCP integration. If the user explicitly asks for API Key or legacy AK/SK official API usage, route to `kling-api` instead.

API examples: “用可灵 API 生成普通视频” selects Kling 3.0; “用 3.0 Omni 参考这个视频的运镜” selects reference generation; “用 3.0 Omni 修改原视频的场景/元素” selects base-video editing. Read the current API tool skill for the contents/settings schema.

Hermes collaboration: “接入 Hermes” / “与 Hermes 协作” selects `hermes-bridge`; it uses the existing local Hermes runtime and shared project/Kling runner. It does not start a background conversation or activate SW automatically.

Trigger only when the user explicitly asks for:

- `Kling CLI`
- `可灵 MCP`
- `kling-cli`
- `@kling-cli`
- 可灵官方 CLI
- 可灵文生图
- 可灵图生图
- 可灵文生视频
- 可灵图生视频
- Kling image generation through the official CLI
- Kling video generation through the official CLI

Default route:

```text
upstream Studio role if needed -> Selected Asset Packet if a concrete object is selected -> prompt-director -> kling-cli
```

Do not trigger for ordinary image/video prompt drafting. Do not execute the installer, login/relogin, private upload, real generation, batch generation, or long polling without confirmation. If `kling` is not installed or OAuth credentials are missing, report the missing state and use prompt-only/preflight.

Model behavior: do not hardcode supported models. Inspect `kling who_am_i` and, when needed, `kling tool_list` or `kling <command> --help` before real use.

## Seedance 2.0 Video

Purpose: explicit Ark Seedance API video generation after SW shot/prompt preparation.

Use this route for Ark Seedance API / Seedance 2.0 execution. If the user explicitly asks for the official Dreamina/Jimeng CLI, route to `dreamina-cli` instead.

Trigger only when the user explicitly asks for:

- ??2.0??
- Jimeng generation through the Ark Seedance API route
- `Seedance 2.0`
- `Ark Seedance`
- ?? Seedance
- `@seedance-2-video`
- use Seedance to generate/output a video

Default route:

```text
upstream Studio role if needed -> Selected Asset Packet if a concrete shot/media item is selected -> prompt-director -> seedance-2-video
```

Do not trigger for ordinary storyboard, edit-plan, or video prompt drafting.

No key behavior: if `ARK_API_KEY` or a local Seedance key file is missing, run dry-run/payload only and do not claim a video was generated.

Local media behavior: if the user provides a local image/video file for Seedance, use `url-relay` first to create a public `http(s)` URL, then pass that URL to `seedance-2-video`. If relay upload fails, stop before real generation and keep the prompt/payload.

## URL Relay

Purpose: convert local media into public `http(s)` URLs for AI tools that cannot fetch local files.

Trigger when the user explicitly asks for:

- `URL中转`
- `公网URL`
- `上传参考图`
- `上传参考视频`
- `中转上传`
- `@url-relay`
- local file to public URL
- use local reference image/video for Seedance/即梦/Ark

Default route:

```text
Selected Asset Packet if a concrete media item is selected -> prompt-director if prompt work is needed -> url-relay -> downstream tool
```

Do not upload private client assets, faces, unreleased products, or brand assets without explicit user permission.

Fallback: use the configured SW server first. If it is unreachable or returns a server-side failure, report `SW media uploader unavailable`; then use Litterbox/Catbox only when the user confirms fallback or local private config enables it. Missing token/address or permission errors do not fallback. If no fallback is allowed, keep the prompt/payload and ask for a public URL.

## Black Background Cutout

Purpose: fast local transparent PNG preview from black or simple solid-background images.

Trigger when the user explicitly asks for:

- `抠图`
- `扣图`
- `去底`
- `去黑底`
- `黑底转透明`
- `透明底 PNG`
- `transparent PNG`
- `@black-background-cutout`

Default route:

```text
existing local image file -> black-background-cutout
```

Do not run prompt writing, image generation, public upload, or full project routing unless the user also asks for redesign. This tool is for quick cutout preview only and may leave slight edge fringing. For complex photo cutouts or formal delivery, recommend professional refinement or a regenerated transparent asset.

## Storyboard Visual Word

Purpose: create a clean Word/DOCX visual director handoff from already-selected storyboard, scene, or concept images.

Trigger only when the user explicitly asks for:

- `视觉方案文件`
- `视觉导演方案`
- `Word视觉方案`
- `DOCX视觉方案`
- `分镜视觉方案文件`
- `视觉方案docx`
- `@storyboard-visual-word`
- make these storyboard/scene images into a Word visual bible

Default route when selected visuals already exist:

```text
Selected Asset Packet for selected visuals -> finishing-producer -> storyboard-visual-word
```

Default route when visuals are not ready:

```text
storyboard-director or production-designer -> asset-producer if needed -> prompt-director if needed -> explicit image tool if requested -> Selected Asset Packet -> finishing-producer -> storyboard-visual-word
```

Do not trigger for ordinary storyboard planning, prompt writing, image generation, integrated storyboard sheet design, or Word/PPT tasks that are not visual director handoffs.

Formal DOCX output should embed selected images and include scene title, time/shot range, visual setting, and rationale. Do not include raw prompts, local paths, generation-result tables, or tool parameters unless the user asks for an internal production appendix.

## Feishu Docs

Purpose: render or publish already-prepared visual plans and storyboard handoffs into Feishu/Lark Docs.

Trigger only when the user explicitly asks for:

- `转到飞书`
- `同步到飞书`
- `发布到飞书`
- `飞书视觉方案`
- `飞书分镜`
- `Feishu Docs`
- `Lark Docs`
- `@feishu-docs`
- make this visual plan/storyboard into a Feishu document

Default route when the handoff already exists:

```text
Selected Asset Packet if selected images/media are part of the handoff -> finishing-producer -> feishu-docs
```

Default route when the visual/storyboard source is not ready:

```text
storyboard-director or production-designer -> optional image/URL tools if needed -> Selected Asset Packet -> finishing-producer -> feishu-docs
```

Do not trigger for ordinary storyboard planning, prompt writing, image/video generation, DOCX packaging, or general mention of 飞书 unless the user asks to transfer/render/publish into Feishu.

No credential behavior: render Feishu-friendly Markdown or dry-run a publish plan only. Real publishing requires local private Feishu/Lark app credentials and explicit `--execute`.

Privacy: external publishing can expose client material, local paths, prompts, or internal notes. Confirm before publishing sensitive content.

## Aesthetic Decision

Purpose: choose a high-taste visual profile when the user has not specified a look, asks SW to decide, or supplies project-local visual references that need interpretation.

Trigger when the user says:

- `/aesthetic`
- 自动选择审美
- 审美画像
- 视觉参考方向
- moodboard direction
- SW decide the look
- 你按审美库来
- 我没指定视觉风格，你来定

Default route:

```text
aesthetic-director -> next production role
```

Use `Aesthetic_Decision_Index.md` first. Do not load raw images, contact sheets, or broad source indexes unless the user asks for reference inspection, moodboard comparison, or aesthetic-library maintenance.

Project-local `.sw/ASSETS.md`, `.sw/RULES.md`, `.sw/MEMORY.md`, and user-provided reference images override the global library.

## Obsidian Aesthetic Vault

Purpose: browse, review, and curate SW's aesthetic reference library in Obsidian without loading raw images into normal SW runtime. Generated notes embed local contact-sheet previews so clicking graph/profile/collection nodes shows images first, then source links.

Trigger only when the user explicitly asks for:

- `Obsidian审美库`
- `打开审美资料库`
- `整理审美库`
- `筛选审美图片`
- `审美 vault`
- `把审美资料放进 Obsidian`

Default action:

```text
run tools/sync_obsidian_aesthetic_vault.py -> sync the active Obsidian vault when available, otherwise use Obsidian_Aesthetic_Vault/
```

Normal project work must not load this vault. Use `Aesthetic_Decision_Index.md` for low-token automatic aesthetic selection.

## Historical Accuracy

Purpose: optional historical/civilization accuracy gate for visual outputs, especially poster key visuals, storyboard first frames, Banana-generated images, Seedance representative frames/stills, reference-image QA, and final image review.

Historical checking is not just prompt wording. When enabled, it checks the final visual asset/image for anachronism and credibility.

Related optional look support: Historical Drama Style Capsule. It can be suggested for historical drama, cultural heritage, archaeology, ancient craft, intangible heritage, or museum storytelling, but it is only a visual baseline and does not enable historical checking.

### Five Trigger Groups

1. Historical accuracy intent:
   - 历史准确, 考据, 严谨, 符合史实, 不要穿帮, 复原, 学术, 依据, 可查, 博物馆级, 纪录片级

2. Dynasty/period specificity:
   - 夏商周, 秦汉, 魏晋, 隋唐, 宋元明清, 民国
   - 初唐, 盛唐, 晚唐, 北宋, 南宋, 明代, 清代
   - 朝代考究, 时代背景, 某朝服饰, 某朝建筑

3. Civilization/archaeology/site:
   - 古埃及, 两河, 波斯, 希腊, 罗马, 玛雅, 印度
   - 良渚, 古蜀, 三星堆, 殷墟, 敦煌, 龟兹, 楼兰
   - 考古, 遗址, 文物, 墓葬, 壁画, 器物复原

4. Material culture / production design:
   - 服饰, 甲胄, 官服, 冠帽, 发髻, 妆容
   - 建筑, 家具, 器物, 纹样, 兵器, 车马, 礼制, 祭祀
   - 道具, 场景复原, 历史人物造型

5. Serious historical project context:
   - 博物馆展陈, 文物宣传片, 历史纪录片, 文旅历史片
   - 非遗, 城市历史片, 历史人物专题, 学校/政府/院所汇报
   - 展览, 科普, 教材, 学术展示

### Non-Triggers

Do not trigger or remind for style-only phrases by themselves:

- 国风
- 古风
- 唐风
- 宋韵
- 东方美学
- 敦煌感
- 新中式
- 仙侠感

If the user says "只是氛围", "不要太考据", "好看优先", "商业感优先", or "随便古风", do not trigger historical checking.

### Reminder Threshold

Do not auto-load `historical-consultant`.

Add a one-line reminder when:

- group 1 is hit, or
- group 5 is hit, or
- a dynasty/civilization/site term is combined with a concrete visual object from group 4.

Reminder text:

```text
检测到历史准确性风险。是否开启历史准确性检查？默认不开启。
```

Load `historical-consultant` only after the user confirms with words such as:

- 开启
- 要考据
- 需要准确
- 是
- 按历史准确做

If the request is otherwise actionable, continue the normal low-cost route with historical checking off by default unless the user confirms.

### Scope And Close

Default scope is the current request or current visual-output chain only. It is not automatically permanent.

Scope commands:

- `本项目开启历史检查`
- `全程开启历史检查`
- `本项目按历史准确做`

Close commands:

- `关闭历史检查`
- `不用历史检查`
- `恢复普通模式`

Persistent memory changes require the user to explicitly ask to remember/write/delete project memory.

## Rescue Entry

Purpose: bypass stale `sw-v1-0` or `sw-update` skill chips that keep replaying sealed old versions.

Trigger when the user says:

- `@sw_rescue`
- `/sw-rescue`
- `/sw_rescue`
- `SW_RESCUE`
- `SW_REPAIR`
- `SW_FORCE_UPDATE`
- `SW rescue`
- `SW force refresh`

Required reply:

```text
SW rescue synchronized. Current version: V1.16.1
```

This is not a project start, not a normal sync replacement, and not a tool-generation step.

## Help Entry

Use `@sw_help`, `/sw_help`, `/sw-help`, `SW_HELP`, or "SW 帮助 / 功能触发词" to show a short feature list.
