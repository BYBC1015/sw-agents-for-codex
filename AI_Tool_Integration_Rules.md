# AI Tool Integration Rules AI工具适配与接入规则

本文件用于适配现在和未来接入聊天窗口的 AI 工具。目标：先有统一创意和提示词规范，再按工具能力转换，不被某个工具的写法绑死。

## 工具使用原则

- 先判断任务，再选择工具；不要因为某个工具可用就强行使用。
- 先用通用创意提示词锁定意图，再转换成工具专用提示词。
- 每个工具必须有工具卡，记录能力、输入、输出、限制、成本和风险。
- 新工具接入时，先注册工具卡，再加入自动派单。
- 工具参数不确定或可能已更新时，优先查官方文档或让用户提供工具说明。
- 点名具体生成工具或要求“官方案例/官方手册”时，先保留 Universal Prompt，再按 `Prompts/Tool_Official_Prompt_Deltas.md` 读取对应小节做工具差异转换；普通项目不要加载完整官方手册。
- 当上游已经选定具体海报视觉、deck 页面、分镜镜头、参考图、URL、本地素材或生成结果时，先用 `Selected Asset Packet` 记录对象 ID、用途、参考物角色、锁定项、禁止项、下一工具和隐私/成本门，再进入 prompt 或工具转换。
- 涉及付费、高成本、外部发布、版权风险时，先低成本预检。
- Black Background Cutout / `black-background-cutout` 是显式触发的本地抠图工具，不是 AI 生成工具。只有用户明确说抠图、扣图、去底、去黑底、黑底转透明、透明底 PNG 或 `@black-background-cutout` 时才加载；它只对本地黑底/简单纯色底图片做快速透明 PNG 预览，可能有轻微毛边，不作为正式无损交付资产。
- Banana Pro / `banana-pro` 是显式调用的出图成员，作用类似 `imagegen`，位于 `prompt-director` 之后：只有用户明确提到香蕉、banana、Banana Pro、Nano Banana、OpenRouter 图像生成、`@banana-pro`，或明确要求用这个成员生成图片时才加载；普通图片提示词仍由 `prompt-director` 处理。
- Banana Pro 不能越过上游设计岗位。若同一请求包含分镜、视频/电影镜头、海报、PPT/deck/slide、版式、角色、产品、道具或场景设计，先由对应 Studio role 产出设计 handoff，再由 `prompt-director` 转为最终视觉 prompt，最后才交给 Banana Pro 生成选中的一张/一帧。
- Banana Pro 已包含 OpenRouter API 执行脚本；真实生成需要用户明确确认且环境存在 `OPENROUTER_API_KEY` 或本机私密 `~/.config/banana-pro/openrouter.env`。当用户明确要求生成一张草稿且 prompt/handoff 已清楚时，走 API fast path：不额外 doctor/key-check，不读无关参考，直接运行固定命令并让脚本返回 `ok/missing-key/no-image`。没有 key 时只做 dry-run/payload，不声称已出图。
- Dreamina CLI / `dreamina-cli` 是显式调用的官方即梦/Dreamina CLI 图像与视频生成成员，位于 `prompt-director` 之后：只有用户明确提到 Dreamina CLI、Jimeng CLI、official Jimeng CLI、dreamina、`@dreamina-cli`、即梦官方 CLI、即梦生成图片，或明确要求通过官方 CLI 生成图像/视频时才加载；普通图片/视频提示词仍由 Studio roles 与 `prompt-director` 处理。
- Dreamina CLI 不能越过上游设计岗位。若同一请求包含分镜、脚本、镜头语言、剪辑节奏、声音、调色、海报、PPT/deck/slide、版式、角色、产品、道具或场景设计，先由对应 Studio role 产出设计 handoff，再由 `prompt-director` 转为最终 prompt，最后才交给 Dreamina CLI 生成选中的图片、片段或任务。
- Dreamina CLI 依赖本地 `dreamina` 命令、账号登录态和异步任务查询。不要直接执行 `curl | bash`、登录、重登、真实生成、上传私密素材或批量生成，除非用户明确确认。不要硬编码模型能力；每次真实调用前用 `dreamina -h` 和 `dreamina <subcommand> -h` 确认当前 CLI 暴露的模型、参数、数量、时长、画幅和下载方式。未安装或未登录时只做 help/preflight 或 prompt-only handoff，不声称已生成。
- Kling CLI / `kling-cli` 是显式调用的官方可灵 CLI/MCP 图像与视频生成成员，位于 `prompt-director` 之后：只有用户明确提到 Kling CLI、可灵 MCP、`kling-cli`、`@kling-cli`、可灵文生图、可灵图生图、可灵文生视频、可灵图生视频，或明确要求通过官方可灵 CLI/MCP 生成图像/视频时才加载；普通图片/视频提示词仍由 Studio roles 与 `prompt-director` 处理。
- Kling CLI 不能越过上游设计岗位。若同一请求包含分镜、脚本、镜头语言、剪辑节奏、声音、调色、海报、PPT/deck/slide、版式、角色、产品、道具或场景设计，先由对应 Studio role 产出设计 handoff，再由 `prompt-director` 转为最终 prompt，最后才交给 Kling CLI 生成选中的图片、片段或任务。
- Kling CLI 依赖本地 `kling` 命令、OAuth 登录态和异步任务查询。不要读取或展示 `~/.kling/.credentials` 内容；不要绕过 CLI 直接请求 MCP/API；不要安装、登录、重登、真实生成、上传私密素材或批量生成，除非用户明确确认。不要硬编码模型能力；真实调用前用 `kling who_am_i`、必要时 `kling tool_list` 或 `kling <command> --help` 确认当前模型、参数、数量、时长、画幅和下载/轮询方式。未安装或未登录时只做 help/preflight 或 prompt-only handoff，不声称已生成。
- Seedance 2.0 Video / `seedance-2-video` 是显式调用的视频生成成员，位于 `prompt-director` 之后：只有用户明确提到即梦2.0生成、即梦生成、Seedance 2.0、Ark Seedance、豆包 Seedance、`@seedance-2-video`，或明确要求用这个成员生成视频时才加载；普通视频提示词和分镜仍由 Studio roles 与 `prompt-director` 处理。
- Seedance 不能越过上游视频设计岗位。若同一请求包含脚本、分镜、镜头语言、剪辑节奏、动效、声音、调色、场景或电影方案，先由对应 Studio role 产出 handoff，再由 `prompt-director` 转为最终视频 prompt，最后才交给 Seedance 生成选中的一条镜头/片段。
- 当 Seedance 要严格按 storyboard 执行一个 sequence 时，先创建或选中 Storyboard Animatic Sheet。该 sheet 必须包含 panel grid + director strip；`prompt-director` 再把它转成“引用 storyboard + 角色 + 环境 + PANEL BEATS”的 Seedance 执行 prompt。普通分镜图或无 director strip 的 contact sheet 只能作为视觉参考，不足以声明严格按分镜执行。
- Seedance 已包含 Ark API dry-run/run/poll 脚本；真实生成需要用户明确确认且环境存在 `ARK_API_KEY` 或本地私密 key 文件。没有 key 时只做 dry-run/payload，不声称已出视频。
- URL Relay / `url-relay` 是显式或工具需要时触发的公网素材中转层，位于下游生成工具之前：当 Seedance/即梦、Ark、图生视频或其他 AI 工具需要公共 `http(s)` URL，而用户只提供本地图片/视频路径时，优先使用已配置的 SW media uploader；若自有服务器连接失败或返回服务器侧错误，必须提示无法连接服务器，并且只有用户确认或本机私密配置允许时，才按优先级切到 Litterbox/Catbox 临时中转；缺 token、缺地址或权限错误不触发 fallback。
- URL Relay 不参与创意、不改写提示词，也不是 Studio role。它只负责本地素材 -> 公网 URL；上传 token 和服务器配置必须留在本机私密配置，不进入仓库、prompt、日志或交付文件。
- Storyboard Visual Word / `storyboard-visual-word` 是显式触发的 DOCX 视觉方案交付工具，位于上游分镜/视觉开发/选图完成之后：只有用户明确要求视觉方案文件、视觉导演方案、Word视觉方案、DOCX视觉方案、分镜视觉方案文件或 `@storyboard-visual-word` 时才加载；普通分镜、提示词、图片生成和一体式分镜板不自动触发它。
- Storyboard Visual Word 不能越过上游设计岗位。若同一请求还需要脚本、分镜、场景设定、角色设定、出图或选图，先由对应 Studio role 和工具完成设计与选图，再把已选图片和视觉设定打包成 DOCX。
- Feishu Docs / `feishu-docs` 是显式触发的 Feishu/Lark Docs 交付工具，位于上游视觉方案、分镜、选图、DOCX/Markdown handoff 完成之后：只有用户明确要求转到飞书、同步到飞书、发布到飞书、飞书视觉方案、飞书分镜、Lark Docs、Feishu Docs 或 `@feishu-docs` 时才加载；普通分镜、提示词、图片生成、Word/DOCX 交付不自动触发它。
- Feishu Docs 不能越过上游设计岗位。若同一请求还需要脚本、分镜、场景设定、角色设定、出图、选图或 Markdown/DOCX 源内容，先完成对应设计与交付整理，再渲染飞书友好 Markdown 或发布到飞书。真实发布必须确认外部发布和隐私风险。
- Obsidian Aesthetic Vault 是本地审美资料库浏览和筛选层，不是生成工具。只有用户明确要求 Obsidian 审美库、整理审美库、筛选审美图片、打开审美资料库或维护 aesthetic vault 时才使用；普通 SW 项目仍只读取 `Aesthetic_Decision_Index.md`，不加载 vault 或大图。
- Obsidian Aesthetic Vault 不能替代 `aesthetic-director` 的低成本判断。它只服务人工浏览、资料筛选、profile 维护和项目 moodboard；同步脚本只生成 Markdown 链接，不启动 WPS/Word/Office，不复制大图，不消耗模型 token。

## 工具类型

| 类型 | 用途 | 主责岗位 |
| --- | --- | --- |
| 图像生成 | 海报主视觉、背景、产品氛围、分镜图 | `prompt-director` |
| 图像编辑 | 扩图、局部替换、去背景、风格统一 | `prompt-director` + `asset-producer` |
| 本地像素处理 | 黑底/纯色底抠图、透明 PNG 预览 | 显式工具 skill |
| 视频生成 | AI 镜头、动态视觉、产品动效 | `prompt-director` + `storyboard-director` |
| 视频编辑 | 自动剪辑、字幕、节奏、转场 | `edit-director` |
| 版式/设计 | Canva、海报模板、尺寸适配 | `poster-art-director` |
| 音频/配音 | BGM、音效、旁白、口播 | `edit-director` |
| 素材/资产 | 素材库、字体、品牌资产、云盘 | `asset-producer` |
| 审核/质检 | 版权、品牌、平台规格、可读性 | `review-producer` |
| 文档交付 | Word视觉方案、视觉导演方案、分镜视觉方案文件 | `finishing-producer` + `storyboard-visual-word` |

## 工具卡模板

新增工具时，在 `Tool_Registry.md` 增加一张工具卡：

```text
工具名：
工具类型：
触发说法：
最适合：
不适合：
输入需要：
输出格式：
提示词格式：
关键参数：
限制与风险：
成本等级：
隐私注意：
质检方式：
失败时替代方案：
```

## 通用提示词到工具提示词

所有 AI 生成工具都走 4 层转换；若已有 Selected Asset Packet，则在 Studio Brief 之后、Prompt Profile 之前消化该包：

1. Studio Brief：目标、受众、平台、方向、禁区。
2. Selected Asset Packet：仅在已有选中对象时使用，保留对象 ID、用途、参考角色、锁定项、禁止项、下一工具、隐私/成本门。多参考图优先按 `identity / structure / style / motion source` 标注，避免把所有参考都当成全局风格。
3. Prompt Profile：按 `AI_Tool_Prompt_Profiles.md` 选择图像生成、图像编辑、视频生成、视频编辑、版式或音频剖面。
4. Universal Prompt：主体、场景、构图、镜头、光线、色彩、动作、限制。
5. Official Delta：只有点名工具或排错时，按 `Prompts/Tool_Official_Prompt_Deltas.md` 叠加官方提示词差异。
6. Tool Prompt：按工具支持的语法、参数、比例、时长、参考图、负面词转换。
7. QA Notes：后期处理、版权风险、一致性和二次修改参数。

## 工具选择规则

| 情况 | 优先工具类型 |
| --- | --- |
| 需要准确文字、logo、二维码 | 版式/设计工具或后期软件，不用生成模型硬画 |
| 需要真实产品不变形 | 原产品图 + 图像编辑/合成，不直接重绘 |
| 需要多镜头连续人物 | 先做分镜和一致性锁定，再用视频工具 |
| 需要封面或海报主视觉 | 图像生成/图像编辑 + 后期排版 |
| 用户明确要求香蕉 / banana / Banana Pro / Nano Banana / OpenRouter 图像生成 | 已有完整 prompt：`prompt-director` -> `banana-pro`；仍需设计：先上游 Studio role -> `prompt-director` -> `banana-pro`；`tool-integrator` 只在能力、参数或接入状态不清楚时介入 |
| 用户明确要求 Dreamina CLI / Jimeng CLI / official Jimeng CLI / dreamina / @dreamina-cli / 即梦官方 CLI 图像或视频生成 | 已有完整 prompt：`prompt-director` -> `dreamina-cli`；仍需设计：先上游 Studio role -> `prompt-director` -> `dreamina-cli`；未安装/未登录/模型参数不清楚时先 help/preflight，不直接生成 |
| 用户明确要求 Kling CLI / 可灵 MCP / kling-cli / @kling-cli / 可灵官方 CLI 图像或视频生成 | 已有完整 prompt：`prompt-director` -> `kling-cli`；仍需设计：先上游 Studio role -> `prompt-director` -> `kling-cli`；未安装/未登录/模型参数不清楚时先 who_am_i/tool_list/help preflight，不直接生成 |
| 用户明确要求即梦2.0生成 / 即梦生成 / Seedance 2.0 / Ark Seedance 视频生成 | 已有完整 prompt：`prompt-director` -> `seedance-2-video`；仍需设计：先上游 Studio role -> `prompt-director` -> `seedance-2-video`；`tool-integrator` 只在能力、参数、key 或接入状态不清楚时介入 |
| 下游 AI 工具需要公网 URL，但用户提供本地图片/视频文件 | `url-relay` 将本地素材中转为 `http(s)` URL；随后回到 Banana/Seedance/其他工具；隐私不明时先确认 |
| 用户明确要求视觉方案文件 / 视觉导演方案 / Word视觉方案 / DOCX视觉方案 | 已有选定图片和设定：`storyboard-visual-word`；仍需分镜/设定/选图：先上游 Studio role -> 可选生成工具 -> `storyboard-visual-word` |
| 用户明确要求转到飞书 / 同步到飞书 / 发布到飞书 / 飞书视觉方案 / 飞书分镜 | 已有 handoff：`feishu-docs`；仍需分镜/设定/选图/Markdown：先上游 Studio role -> 可选生成工具 -> `finishing-producer` -> `feishu-docs` |
| 用户明确要求 Obsidian审美库 / 整理审美库 / 筛选审美图片 / 打开审美资料库 | 运行 `tools/sync_obsidian_aesthetic_vault.py` 生成/同步 Markdown vault；日常审美决策仍回到 `aesthetic-director` + compact index |
| 需要剪辑节奏 | 视频编辑工具或人工剪辑方案 |
| 需要音效/BGM | 音频工具或授权素材库 |
| 需要团队协作 | Canva/云盘/项目管理工具 |

## 新工具接入流程

1. 识别工具类型和能力。
2. 建立工具卡。
3. 判断归属岗位 skill。
4. 选择 `AI_Tool_Prompt_Profiles.md` 里的提示词剖面。
5. 加入 `Auto_Assignment_Rules.md` 的工具触发规则。
6. 加入 `Prompt_Spec_Rules.md` 或独立工具提示词规则。
7. 用 `Examples/Tool_Integration_Test.md` 做一次测试。

## 聊天窗口工具规则

当用户后续在聊天窗口集成新工具：

- 先检查当前可用工具列表；如果环境提供工具发现能力，先使用工具发现；否则让用户说明工具能力。
- 如果工具是插件/连接器，优先用工具自己的官方能力，不臆测不存在的功能。
- 如果工具需要外部账号、付费额度、上传素材或导出权限，先提醒用户。
- 如果工具输出不可逆或会消耗额度，先给预览级提示词和执行说明。
- 如果工具失败，保留通用提示词和替代工具建议。

## 提示词版本管理

每次为工具生成 prompt，保留：

- 通用版 prompt。
- 工具专用版 prompt。
- 负面/禁止项。
- 参数锁定项。
- 可改参数。
- 生成后质检项。

## Historical Accuracy Tool Rule

When historical accuracy is enabled:

- Treat historical checking as a final visual-output QA gate for image tools, not only a prompt constraint.
- For Banana Pro or future image generators, pass compact historical constraints into `prompt-director`, then check the generated still/image after output.
- For Seedance or future video generators, pass compact historical constraints into `prompt-director`, then review representative output frames/stills when available. Do not claim full automated video QA beyond visible frames/stills.
- Do not auto-enable historical checking for style-only phrases.
