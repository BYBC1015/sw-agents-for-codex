# Tool Registry 工具注册表

本文件记录当前和未来可接入聊天窗口的 AI/设计工具。新增工具时先添加工具卡，再进入正式工作流。

## 当前默认工具类型

| 工具类型 | 状态 | 默认处理 |
| --- | --- | --- |
| 通用图片生成 | 预留 | 用 `prompt-director` 输出通用图片 prompt |
| 通用视频生成 | 预留 | 用 `prompt-director` 输出逐镜头视频 prompt |
| 图像编辑/扩图 | 预留 | 先锁定修改区域、保留项和禁止项 |
| Canva/在线设计 | 预留 | 用 `poster-art-director` 处理版式和尺寸 |
| Adobe 工作流 | 预留 | 用 `poster-art-director` / `edit-director` 输出执行清单 |
| 剪映/CapCut | 预留 | 用 `edit-director` 输出时间线、字幕、音效 |
| 音频/配音 | 预留 | 用 `edit-director` 输出旁白、BGM、音效需求 |
| 素材库/云盘 | 预留 | 用 `asset-producer` 管理素材来源和授权 |

## 已登记工具成员

```text
工具名：Banana Pro
工具类型：图像生成 / 出图执行 / OpenRouter image generation
接入状态：本地 skill 已接入；定位等同 `imagegen` 类出图成员；已打包 OpenRouter API 执行脚本；补齐 `OPENROUTER_API_KEY` 或本机私密 `~/.config/banana-pro/openrouter.env` 后可在确认后真实生成图片
触发说法：香蕉、banana、@banana-pro、Banana Pro、Nano Banana、google/gemini-3-pro-image-preview、OpenRouter 图像生成、用 banana-pro 生成/出图/转换
最适合：海报主视觉、分镜首帧、产品或道具概念图、角色设定图、场景底图、多参考图像提示词包
不适合：普通图片提示词的默认处理、准确中文文字、logo/二维码、未确认版权或客户敏感素材的自动上传、未经确认的额度消耗、未配置 `OPENROUTER_API_KEY` 时假装已生成图片
输入需要：用途、主体、画幅、image_size、参考图角色、风格、连续性锁定、必须避免项
输出格式：生成后的图片路径、payload、response 和 QA；未配置 key 时输出 dry-run payload
提示词格式：由 `prompt-director` 先产出通用视觉 prompt，再交给 Banana Pro 作为生成/出图环节
不可越级：若同一需求包含分镜、视频/电影镜头、海报、PPT/deck/slide、版式、角色、产品、道具或场景设计，先由对应 Studio role 产出 handoff，再由 `prompt-director` 生成最终 prompt，最后交给 Banana Pro；默认只生成选中的一张/一帧
提示词剖面：图像生成 / 图像编辑 / 多参考图像
关键参数：model `google/gemini-3-pro-image-preview`、modalities `["image", "text"]`、aspect_ratio、image_size、reference image roles、`OPENROUTER_API_KEY` 或本机私密 `~/.config/banana-pro/openrouter.env`
限制与风险：模型、参数或 OpenRouter 行为可能更新；可能消耗额度；参考图可能涉及隐私、版权、客户未公开素材；未配置 key 时只能 dry-run，不能声称已出图
成本等级：真实生成为高；仅准备设置为中
隐私注意：生成前确认是否允许上传客户素材、人物照片、未公开产品图或品牌资产
质检方式：主体一致性、画幅、产品/角色保真、文字/logo 风险、额外物体、可排版留白
失败时替代方案：保留通用 prompt，改用通用图像工具、后期合成、素材库或只输出分镜首帧方案
归属岗位：prompt-director -> banana-pro；tool-integrator 仅在能力、参数、API 或接入状态不清楚时介入
派单显示：`prompt-director` 放在 `Studio roles:`；`banana-pro` 必须单独显示为 `Tool skill:`，不要写成 Studio role
读取路径：优先 `banana-pro/SKILL.md`，其次用户级 `C:\Users\Administrator\.codex\skills\banana-pro\SKILL.md`，最后插件级 `C:\Users\Administrator\plugins\sw-v1-0\skills\banana-pro\SKILL.md`
执行脚本：`scripts/generate_openrouter_image.py`，从 skill 根目录相对解析；无 key 时用 `--dry-run` 或返回 missing-key
```

```text
工具名：Seedance 2.0 Video
工具类型：视频生成 / 出视频执行 / Volcano Ark Seedance 2.0 / 即梦2.0
接入状态：本地 skill 已接入；定位为 `prompt-director` 之后的视频生成成员；已打包 Ark API dry-run/run/poll 执行脚本；补齐 `ARK_API_KEY` 或本地私密 key 后可在确认后真实生成视频
触发说法：即梦2.0生成、即梦生成、Seedance 2.0、Ark Seedance、豆包 Seedance、@seedance-2-video、用即梦生成视频、用 Seedance 生成视频
最适合：单条短镜头生成、分镜验证、产品动态氛围、文旅/品牌片镜头草稿、已有首帧/参考图的视频化
不适合：普通视频提示词的默认处理、复杂多镜头长剧情、准确字幕/文字/logo、没有公共图片 URL 的本地图片直接传入、未确认额度消耗、未配置 `ARK_API_KEY` 时假装已生成视频
输入需要：用途、选中镜头、中文视频 prompt、画幅 ratio、时长 duration、分辨率 resolution、video-mode、至少 1 个公共 `http(s)` image-url 或可经 `url-relay` 上传的本地 image-file、输出目录
输出格式：dry-run payload；真实生成后的 `final.mp4`、`run_manifest.json`、任务状态和下载路径
提示词格式：由 `prompt-director` 先产出通用逐镜头视频 prompt，再交给 Seedance 作为生成/出视频环节
不可越级：若同一需求包含脚本、分镜、视频/电影镜头、剪辑、动效、声音、调色、场景或方案设计，先由对应 Studio role 产出 handoff，再由 `prompt-director` 生成最终 prompt，最后交给 Seedance；默认只生成选中的一条镜头/片段
提示词剖面：视频生成 / 图生视频 / 参考图视频化
关键参数：model `doubao-seedance-2-0-260128`、ratio、duration、resolution、seed、watermark、video-mode、public image URLs、`ARK_API_KEY`
限制与风险：真实生成可能消耗额度并排队较久；Ark 必须能访问公共图片 URL；本地私有素材需先经 `url-relay` 中转并满足隐私授权；长片、多镜头和 1080p 成本更高；文字/logo/字幕不稳定
成本等级：dry-run 为低；真实生成/长轮询为高
隐私注意：不要把客户未公开图片传到公共 URL；不要把 API key 写入 skill、仓库、日志或示例
质检方式：主体稳定、动作合理、镜头连续、画幅、可剪辑性、文字/logo 风险、历史/服装/道具/建筑风险、是否符合分镜意图
失败时替代方案：保留通用视频 prompt，改用剪辑方案/实拍素材/其他视频工具；无 key 时只输出 dry-run payload；队列过久时使用 `poll` 续查或 `--submit-only` handoff
归属岗位：prompt-director -> seedance-2-video；tool-integrator 仅在能力、参数、API、key 或接入状态不清楚时介入
派单显示：`prompt-director` 放在 `Studio roles:`；`seedance-2-video` 必须单独显示为 `Tool skill:`，不要写成 Studio role
读取路径：优先 `seedance-2-video/SKILL.md`，其次用户级 `C:\Users\Administrator\.codex\skills\seedance-2-video\SKILL.md`，最后插件级 `C:\Users\Administrator\plugins\sw-v1-0\skills\seedance-2-video\SKILL.md`
执行脚本：`scripts/seedance_task.py`，从 skill 根目录相对解析；无 key 时用 `dry-run` 或返回 missing-key，不进行真实提交
```

```text
工具名：URL Relay
工具类型：公网 URL 中转 / 本地素材上传 / AI 工具参考图桥接
接入状态：本地 skill 已接入；默认使用 SW media uploader 服务器；配置文件保存在用户本机 `~/.config/sw-media-uploader/config.json`，上传 token 不进入仓库
触发说法：URL中转、公网URL、上传参考图、上传参考视频、中转上传、@url-relay、给即梦用的公网图、把本地素材转成 URL
最适合：Seedance/即梦2.0 需要公网参考图时上传本地图片；未来视频工具、图生视频工具或多参考图工具需要 `http(s)` URL 时做桥接
不适合：创意策划、提示词撰写、长期公开素材托管、客户敏感素材未确认上传、需要永久 CDN 或权限管理的交付场景
输入需要：本地文件路径、用途、下游工具、是否允许上传外部服务器；可选 relay config 路径
输出格式：公网 `http(s)` URL、过期/清理提示、失败原因；不得输出上传 token
提示词格式：无；它只服务于工具执行，不改写 prompt
提示词剖面：素材/资产桥接 / 工具执行支持
关键参数：`upload_url`、`public_base`、`token`、`max_bytes`、允许扩展名、清理周期、`temporary_fallback`、`litterbox_time`
限制与风险：拥有链接者可访问中转文件；服务器停用、网络失败或 token 失效时不能保证上传；上传消耗服务器带宽和存储；不等于 AI 模型 token 消耗
成本等级：低到中；上传本身不是模型费用，但可能触发后续高成本生成
隐私注意：客户未公开素材、人物照片、产品机密、品牌资产上传前必须确认；不把 token 写入 prompt、日志、skill、仓库或示例
质检方式：上传后检查 URL 可访问、文件类型正确、下游工具可抓取；失败时先停在 payload/提示词，不提交高成本生成
失败时替代方案：连接失败或服务器侧错误时先提示自有 SW media uploader 不可用；优先使用用户提供的已有公网 URL；若用户确认或本机私密配置允许，则按优先级使用 Litterbox/Catbox 临时中转；缺 token、缺地址或权限错误不触发 fallback；否则请求用户提供公网链接并保留 prompt/payload
归属岗位：prompt-director -> url-relay -> downstream tool；tool-integrator 仅在中转能力、服务器状态或隐私策略不清楚时介入
派单显示：`url-relay` 必须单独显示为 `Tool skill:`，不要写成 Studio role；若随 Seedance 使用，显示在 `seedance-2-video` 之前
读取路径：优先 `url-relay/SKILL.md`，其次用户级 `C:\Users\Administrator\.codex\skills\url-relay\SKILL.md`，最后插件级 `C:\Users\Administrator\plugins\sw-v1-0\skills\url-relay\SKILL.md`
执行脚本：`scripts/url_relay.py`；Seedance runner 也可用 `--image-file` 自动调用同一配置完成上传
```

```text
工具名：Storyboard Visual Word
工具类型：DOCX视觉方案交付 / Word视觉导演方案 / storyboard visual bible packaging
接入状态：本地 skill 已接入；定位为下游交付工具成员；已打包 DOCX 生成与结构检查脚本
触发说法：视觉方案文件、视觉导演方案、Word视觉方案、DOCX视觉方案、分镜视觉方案文件、视觉方案docx、@storyboard-visual-word、把这些分镜/场景图整理成 Word
最适合：已选定分镜图、场景概念图、角色/场景视觉图后，生成客户/导演/团队可读的正式 Word 视觉方案；每场一图或每组一图的视觉导演 handoff
不适合：普通分镜创作、脚本拆解、镜头设计、提示词生成、图片生成、未选图时强行做正式 Word、需要完整 PPT/deck 的汇报包装
输入需要：片名/项目名、场景标题、镜头/时间范围、每场选定图片绝对路径、叙事功能、色调/光线、视觉符号、视觉设定、为什么这样设定、QA notes
输出格式：`[片名]_视觉导演方案.docx`；可选 inspection JSON；最终回复优先给 DOCX 文件链接
提示词格式：无；它不生成 prompt，不把 Midjourney/Banana/Seedance prompt 放进正式 Word
提示词剖面：文档交付 / 视觉方案包装 / DOCX handoff
关键参数：JSON spec、absolute image paths、output docx path、embedded media count、forbidden visible text scan
限制与风险：依赖已选图片；不替代上游 storyboard/production design/prompt/image generation；没有 LibreOffice/预览渲染时只能做结构检查；若用户需要内部复盘版，需另行确认是否保留 prompt/参数
成本等级：中；生成 DOCX 本身不是模型高消耗，但整理大量场景文字会增加输出/编辑成本
隐私注意：图片会嵌入 Word；不要把客户未公开素材、人物照片、敏感项目图打包给外部，除非用户确认交付对象和权限
质检方式：图片嵌入数量不少于场景数；不可见本地路径；无 `Midjourney Prompt`、`--ar`、生成结果表或路径表；文案只保留视觉设定和理由；必要时进行 DOCX 渲染预览
失败时替代方案：若缺图片，返回所需 spec 清单并请求选图；若脚本/依赖失败，输出结构化 Word 大纲或简版 handoff；若渲染不可用，说明只完成结构检查
归属岗位：上游 Studio role 完成设计/选图 -> storyboard-visual-word；`finishing-producer` 可协作定义交付命名和收件人，但不替代该工具
派单显示：`storyboard-visual-word` 必须单独显示为 `Tool skill:`，不要写成 Studio role；只有用户要求视觉方案文件/DOCX/Word 交付时加载
读取路径：优先 `storyboard-visual-word/SKILL.md`，其次用户级 `C:\Users\Administrator\.codex\skills\storyboard-visual-word\SKILL.md`，最后插件级 `C:\Users\Administrator\plugins\sw-v1-0\skills\storyboard-visual-word\SKILL.md`
执行脚本：`scripts/build_scene_visual_docx.py`，从 skill 根目录相对解析；输入 JSON spec 后生成 DOCX 并输出结构检查报告
```

## 工具卡模板

复制以下模板新增工具：

```text
工具名：
工具类型：
接入状态：未接入 / 已接入 / 待验证
触发说法：
最适合：
不适合：
输入需要：
输出格式：
提示词格式：
提示词剖面：图像生成 / 图像编辑 / 视频生成 / 视频编辑 / 版式设计 / 音频配音 / 其他
关键参数：
限制与风险：
成本等级：低 / 中 / 高
隐私注意：
质检方式：
失败时替代方案：
归属岗位：
```

## 注册示例：通用图片生成工具

```text
工具名：Generic Image Generator
工具类型：图像生成
接入状态：预留
触发说法：出图、生成主视觉、图片 prompt、海报背景
最适合：主视觉、背景、氛围图、分镜参考图
不适合：准确文字、logo、二维码、严格产品标签
输入需要：用途、主体、构图、景别、光线、色彩、画幅、禁止项
输出格式：图片或图片提示词
提示词格式：通用图片 prompt + 负面 prompt + 可控修改项
提示词剖面：图像生成
关键参数：画幅、主体占比、风格、一致性锁定
限制与风险：文字错误、产品变形、版权相似
成本等级：中到高
隐私注意：不要上传未授权商业机密或客户敏感素材
质检方式：主体、文字区域、品牌风险、可排版性
失败时替代方案：改为后期合成或素材库
归属岗位：prompt-director
```

## 注册示例：通用视频生成工具

```text
工具名：Generic Video Generator
工具类型：视频生成
接入状态：预留
触发说法：视频 prompt、生成镜头、AI 镜头、动态画面
最适合：短镜头、产品动效、氛围动态、分镜验证
不适合：复杂多镜头连续剧情、准确文字、稳定 logo
输入需要：镜头编号、时长、起始画面、动作、运镜、结束画面、连续性、禁止项
输出格式：视频片段或视频提示词
提示词格式：逐镜头 prompt，不合并复杂镜头
提示词剖面：视频生成
关键参数：时长、画幅、运动速度、主体一致性
限制与风险：变形、闪烁、跳切、主体变化
成本等级：高
隐私注意：谨慎上传客户未公开产品和人物素材
质检方式：主体稳定、动作合理、时长、画幅、可剪辑性
失败时替代方案：拆短镜头或改为实拍/剪辑方案
归属岗位：prompt-director
```

## Historical Accuracy Tool Note

Historical accuracy is not a standalone external generator. It is an optional QA gate handled by `historical-consultant` after user confirmation.

- Applies to image-stage outputs: poster key visuals, storyboard first frames, Banana Pro outputs, reference stills, prop/wardrobe/scene images, and final still review.
- Does not imply that a video-generation module is available.
- Future image/video tools should add a `Historical QA` field to their tool card when they can affect period/civilization accuracy.
