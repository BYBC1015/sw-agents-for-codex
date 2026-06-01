# Stage Runbook 阶段运行手册

## V1.1.0 Question Override

For all stages, role skills ask 3 useful questions by default and may ask up to 5 only when complex campaign, film, tool-risk, or blocked-delivery context requires it. In low-token, speed, "少问", or "你定" mode, ask at most 1 question and proceed with assumptions.

本文件规定 Codex 在显式启用 SW 后如何逐阶段工作。核心目标：少问、少消耗、可执行、可改稿。未输入 `/sw`、`@SW_V1.0`、`调用 SW_V1.0`、`按本项目架构执行` 等显式入口时，不进入本阶段手册。

## 全局状态卡

Codex 在每个项目开始和每次阶段切换时，内部维护一张状态卡。无需每轮完整展示给用户，除非用户问“现在到哪了”。

```text
项目类型：海报 / 视频 / 海报+视频 / 提示词专项 / 工具接入 / 暂不明确
当前阶段：Brief / Research / Direction / Poster / Presentation / Storyboard / Edit / Asset / Prompt / Tool / Review / Change / Archive
本轮主责：自动派单得到的 lead skill
协作岗位：自动派单得到的 support skill，可能为空
已锁定：平台、尺寸/时长、受众、主方向、风格禁区、素材来源
默认假设：未确认但已按常规处理的内容
项目记忆：是否存在 `.sw/MEMORY.md` / `.sw/RULES.md` / `.sw/PROJECT.md`
待确认：最多 3 个关键问题
消耗等级：低 / 中 / 高
下一步产物：
下一棒：自动派单得到的 next skill
```

派单必须先执行 `Auto_Assignment_Rules.md`，再进入具体阶段输出。

长期项目如果存在 `.sw/` 本地记忆包，阶段输出前只读取相关小文件。阶段中出现重大确认时，最多给一句短建议写入 `MEMORY.md`，不要自动写。

每个阶段的产物必须优先输出。阶段结尾最多加 1 条轻提醒，只用于记忆、锁定、下一步、风险或成本提醒；无必要时不提醒，也不为了提醒增加文件读取。

## 轻量对比与快速改稿

Compare Board 不是新大阶段，只是方向、分镜组或 deck 结构之后的短中间物。用户需要比较、反馈很抽象，或下一步会进入高成本制作时才使用，固定只保留：

```text
Compare Board:
- Keep:
- Remove:
 - Next version:
```

Selected Asset Packet is not a new stage. It is a short selected-object handoff used only after a poster visual, deck page visual, storyboard shot/group, reference still, local media item, public URL, or generated image has been chosen and before it goes to `prompt-director`, URL Relay, Banana, Seedance, Kling, Storyboard Visual Word, or Feishu.

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

Use the packet to preserve what was selected, what must not change, what each reference is responsible for, and which tool gets the object next. Do not use it for direct prompt-only requests where the user already supplied a complete final prompt.

Quick edit 适用于已有对象的 S/M 级局部改动：海报/图片、deck 页面或结构、分镜组或单个镜头、剪辑表片段、prompt 参数。最多问 1 个阻塞问题，先输出修改后的对象；如果改动影响受众、主卖点、叙事结构、视觉风格或交付形式，必须回到阶段 9 变更处理。

## 阶段 0：项目识别

| 项目 | 规则 |
| --- | --- |
| 触发 | 用户开启新项目、粘贴需求、要求做海报/视频/提示词 |
| 目标 | 判断项目类型，不急着展开 |
| 最多提问 | 3 个 |
| 默认消耗 | 低 |
| 输出 | 项目类型判断、默认假设、下一步 |
| 退出条件 | 能进入 Brief、或用户只需要提示词专项 |

### 特殊路由

- 用户只要“图片提示词/视频提示词”：进入阶段 7 提示词专项，不强制跑完整项目。
- 用户只要“PPT/slide deck/演示文稿”：进入 presentation/deck 路由，先做低成本结构和页面角色，不直接生成整套长 deck。
- 用户只要“角色设定图/角色设定表/场景设定图/一体式分镜/分镜板”：进入视觉开发板路由；先输出设定 handoff 或分镜组表，再决定是否生成 prompt/图片。
- 用户说“做一套传播”：默认海报+视频，先共用 Brief 和创意方向。
- 用户只给模糊词如“高级、年轻、炸”：先翻译成设计参数，再轻问关键缺口。

## 阶段 1：Brief 压缩

| 项目 | 规则 |
| --- | --- |
| 进入条件 | 有原始需求或用户口述 |
| 目标 | 把原话压成可执行 Brief |
| 最多提问 | 3 个；优先问平台/目标/必须出现 |
| 默认消耗 | 低 |
| 输出 | 目标、受众、平台、核心信息、必须出现、禁止出现、默认假设 |
| 禁止 | 不生成完整方案，不生成高成本提示词 |
| 退出条件 | 目标、平台、交付类型基本明确 |

### 缺失信息默认值

| 缺失项 | 默认处理 |
| --- | --- |
| 平台未知 | 先按小红书/朋友圈海报或抖音/视频号短视频常规处理 |
| 尺寸未知 | 海报默认 3:4；短视频默认 9:16 |
| 时长未知 | 短视频默认 15-30 秒 |
| 受众未知 | 按产品/活动最常见目标人群推断并标注 |
| 风格未知 | 先给 3 个方向，不锁死风格 |

## 阶段 2：轻量研究

| 项目 | 规则 |
| --- | --- |
| 进入条件 | Brief 已压缩，需判断风格或参考 |
| 目标 | 提炼风格，不做重研究 |
| 最多提问 | 2 个；优先问参考和禁区 |
| 默认消耗 | 低 |
| 输出 | 可借鉴点、不能照搬点、风格关键词、素材风险 |
| 禁止 | 不照搬参考图，不扩展成大篇竞品分析 |
| 退出条件 | 可支持 3 个创意方向 |

### 省消耗规则

- 用户没给参考时，使用行业常识生成“参考类型”，不主动大规模搜索。
- 用户给参考图时，只提取色彩、构图、光线、材质、节奏。
- 研究结果只服务下一阶段，不单独写成长报告。

## 阶段 3：创意方向

| 项目 | 规则 |
| --- | --- |
| 进入条件 | Brief 基本明确 |
| 目标 | 给用户 3 个以内方向用于选择 |
| 最多提问 | 通常不问；除非目标冲突 |
| 默认消耗 | 中 |
| 输出 | 方向表、推荐方向、风险 |
| 禁止 | 超过 3 个方向；每个方向写成完整执行案 |
| 退出条件 | 用户选择，或 Codex 推荐并默认进入 |

### 输出要求

每个方向只包含：

- 一句话概念
- 画面感
- 文案语气
- 适合原因
- 风险

如果用户说“你定”，Codex 选择最稳妥方向并说明原因。

当方向之间需要选择，或用户反馈仍是“高级一点/不够抓人/保留这个感觉但别太满”这类抽象判断时，先给轻量 Compare Board，不额外扩写新方向：

```text
Compare Board:
- Keep:
- Remove:
- Next version:
```

## Stage 3B: Aesthetic Decision

Use this stage when the creative direction is usable but the visual style is not locked, the user says SW should decide the look, or project-local visual references need interpretation.

| Item | Rule |
| --- | --- |
| Lead skill | `aesthetic-director` |
| Input | brief, direction, user references, optional `.sw/ASSETS.md` or `.sw/RULES.md` |
| Default cost | low to medium |
| Output | one recommended aesthetic profile, visual levers, avoid list, reference lane, next role |
| Forbidden | loading raw image folders/contact sheets by default, copying exact film frames or layouts |

Exit when one aesthetic profile is selected or when the user explicitly says to skip visual taste selection.

## Stage 4A: Poster Plan

### Poster Default: Image-Native Typography

Poster production is not the same as PPT/deck production. For most posters, SW should act as an art director and revision director: judge the visual problem, translate feedback into precise image-edit instructions, and inspect the result. Do not rebuild poster hero typography with plain system fonts by default.

- Use image/visual-model lettering for hero titles, launch titles, big numerals, glowing/metal/3D/neon title effects, and other display lettering.
- Use editable/system text mainly for exact information text, small copy, legal copy, logo/QR placement, or when the user explicitly asks for editable layers.
- In quick poster edits, output the changed visual first and keep explanation to the affected layer plus QA risk.

| 项目 | 规则 |
| --- | --- |
| 进入条件 | 主方向已确认或默认确认 |
| 目标 | 形成可执行海报方案 |
| 最多提问 | 2 个；优先问尺寸和必须文案 |
| 默认消耗 | 中 |
| 输出 | 文案、版式、主视觉、色彩、字体、素材、后期执行注意 |
| 禁止 | 把海报主标题/数字字效降级成普通系统字体；让 AI 直接生成 logo/二维码或大段必须准确的小字 |
| 退出条件 | 文案、主视觉、版式和导出要求明确 |

### 海报快速改稿触发

当用户已经有海报/截图/参考图，并要求“改一下、换文字、修残影、出单张/四版、照图二、让它更好看、别那么素”时，默认进入海报快速改稿，而不是重跑完整项目：

- 最多问 1 个阻塞问题；能从图和用户话里判断的直接执行。
- 先判断问题属于构图、层级、字效、素材、瑕疵、尺寸还是导出。
- 输出优先给改后图/预览/文件，再给不超过 3 条改动说明。
- 主标题、发布会标题、核心数字、发光字、金属字、3D 字、霓虹字属于视觉文字，优先保留或用 image/视觉模型重绘质感；不要用普通系统字体替代。
- 日期、参数、小字、logo、二维码属于精确信息，走可控排版和字符 QA。
- 如果需要同时保证字效和准确文字，先用视觉模型做字效，再用可控排版校准文字。

### 海报提示词触发

只有在用户要求 AI 图像、主视觉、背景或素材生成时，进入阶段 7 提示词专项。否则只给“画面描述+执行建议”，节省消耗。

## 阶段 4B：PPT / Presentation 方案

| 项目 | 规则 |
| --- | --- |
| 进入条件 | 用户要做 PPT、presentation、deck、slides、汇报、路演、方案演示、客户提案、政府汇报、影片提案或培训课件 |
| 目标 | 把客户目标变成清晰的 deck 结构、章节流、页面角色和下一步制作计划 |
| 主责 skill | `presentation-designer` |
| 最多提问 | 3 个；优先问使用场景、受众/决策人、素材来源；复杂投标/路演/公司汇报最多 5 个 |
| 默认消耗 | 低到中 |
| 输出 | Deck purpose、audience、client decision outcome、section flow、slide-by-slide roles、title takeaway strategy、visual system direction、asset/source needs |
| 禁止 | 一开始直接生成 20+ 页完整长 deck、批量改写所有页面、或跳过结构直接做视觉精修 |
| 退出条件 | 章节流、页面数量范围、核心信息和下一岗位明确 |

### PPT 阶段区别

- 结构阶段：解决“这套 deck 为什么讲、讲给谁、按什么顺序讲”。
- 对比阶段：当 deck 有多个章节流、页面角色方案或用户反馈抽象时，只用 Compare Board 收口，不直接重写整套 deck。
- 客户提案阶段：先判断这套 PPT 要促成什么结果，例如批准预算、确认方向、建立信任、政府汇报或项目过会。
- 页面角色阶段：解决“每一页承担什么任务”，不要先堆内容。
- 文案阶段：交给 `copywriter` 处理标题、章节名、CTA 和精简表达。
- 版式阶段：交给 `layout-designer` 处理网格、字号、留白、图文关系和模板适配。
- 终审阶段：交给 `review-producer` 检查逻辑、标题结论、图表可读性、无障碍和交付风险。
- 导出阶段：交给 `finishing-producer` 处理 PPTX/PDF、字体、嵌入媒体、命名和版本包。

## 阶段 4C：视频结构与分镜

| 项目 | 规则 |
| --- | --- |
| 进入条件 | 主方向已确认或默认确认 |
| 目标 | 把创意转成镜头和时间 |
| 最多提问 | 3 个；优先问平台/时长/素材来源 |
| 默认消耗 | 中 |
| 输出 | 视频结构、前 3 秒钩子、分镜表、素材清单 |
| 禁止 | 只写情绪不写镜头；把所有镜头塞成一段 |
| 退出条件 | 每个镜头有时长、画面、字幕/旁白、素材需求 |

### 视频阶段区别

- 结构阶段：解决“先说什么、后说什么”。
- 分镜阶段：解决“每个镜头看到什么”。
- 对比阶段：当多个分镜组、镜头顺序或节奏方向需要判断时，只用 Compare Board 收口“保留/删除/下一版”，不重写全片。
- 一体式分镜板阶段：把连续镜头组织成可审阅的一张图；默认按 15s 段落分组，单组总时长不超过 15s，最多 9 个镜头但不强行凑九宫格；若镜头卡不到 15s 边界，可先微调镜头时长，仍不自然则转下一组。
- 剪辑阶段：解决“怎么剪、怎么听、怎么转场”。
- 提示词阶段：解决“AI 生成某个镜头怎么描述”。

## 阶段 5：剪辑与最终呈现

| 项目 | 规则 |
| --- | --- |
| 进入条件 | 分镜已形成 |
| 目标 | 给用户可照着剪的时间线 |
| 最多提问 | 2 个；优先问剪辑工具和节奏偏好 |
| 默认消耗 | 中 |
| 输出 | 时间线、节奏、字幕、BGM、音效点、转场、调色、包装 |
| 禁止 | 代替用户承诺已完成最终视频 |
| 退出条件 | 用户能进入 Premiere/AE/剪映执行 |

### 输出重点

- 开场 0-3 秒必须单独写。
- 字幕要考虑移动端可读。
- 音效点要对应时间点。
- 导出规格要按平台说明。

## 阶段 6：AI 资产规划

| 项目 | 规则 |
| --- | --- |
| 进入条件 | 海报或分镜已有明确资产缺口 |
| 目标 | 判断哪些资产要 AI 生成，哪些应人工/素材库处理 |
| 最多提问 | 2 个；优先问是否有品牌素材和产品图 |
| 默认消耗 | 低到中 |
| 输出 | 资产清单、来源建议、风险、是否值得生成 |
| 禁止 | 对每个资产立刻写详细 prompt |
| 退出条件 | 选出需要生成的 1-3 个关键资产 |

### 资产来源优先级

1. 用户/客户提供素材。
2. 自有拍摄或设计素材。
3. 商用授权素材库。
4. AI 生成草稿或辅助素材。
5. AI 生成可进最终稿的素材，必须加强版权和一致性检查。

显式工具执行规则：

- Banana Pro 出图只在用户明确要求香蕉/banana/Banana Pro 时进入，且必须位于对应设计 handoff 和 `prompt-director` 之后。
- Seedance/即梦出视频只在用户明确要求即梦2.0生成/Seedance 生成时进入，且必须位于对应镜头/剪辑 handoff 和 `prompt-director` 之后。
- 未配置 key 或未确认高消耗时，只做 dry-run/payload，不声称已经生成最终资产。

### 视觉开发板资产

- 需要人物连续性时，优先建议角色设定图：大人设、正背侧、表情、细节、剪影、色卡。
- 需要空间连续性时，优先建议场景设定图：建立镜头、关键角度、材质/道具、光线、色卡。
- 需要审阅多镜头时，优先建议一体式分镜板：一组一张，默认 15s 段落、单组不超过 15s、最多 9 镜头；镜头数按内容决定，不强行凑 9 格。
- 这些属于生产参考资产；生成图片前仍需通过 `prompt-director`，真实出图工具需显式确认。
- 当其中某个资产被选中进入 prompt、URL 中转、生成工具、DOCX 或 Feishu 交付时，先写 `Selected Asset Packet`，不要把“选中哪张/哪镜/哪条 URL”只放在口头描述里。

### 用户上传素材规则

- 用户提供 logo、产品图、参考图、视频片段、截图时，先分析可用信息，不重复询问已经能从素材看出的内容。
- 对参考图只提取色彩、构图、光线、材质、节奏，不复刻可识别品牌、人物、logo、文字和独特图案。
- 对产品图优先锁定产品形状、比例、材质、包装结构和不可变形部分。
- 对视频素材优先提取可用镜头、节奏、画幅、画质问题和可剪辑片段。
- 如果素材不可读取或缺失关键细节，只问 1-2 个会影响执行的问题。

## 阶段 7：提示词专项

| 项目 | 规则 |
| --- | --- |
| 进入条件 | 用户要求图片/视频提示词，或某个 AI 资产已确认 |
| 目标 | 输出可复制的高质量 prompt |
| 最多提问 | 2 个；优先问用途和画幅/时长 |
| 默认消耗 | 中；详细多镜头为高 |
| 输出 | 主提示词、负面提示词、可控修改项；视频按镜头输出 |
| 禁止 | 使用“近一点、远一点、高级一点”这类模糊词原样当 prompt |
| 退出条件 | 提示词包含主体、场景、构图、景别、光线、色彩、限制；视频还包含起止画面和运镜 |

必须执行 `Prompts/Prompt_Spec_Rules.md`。

如果提示词输入来自已选海报主视觉、deck 页面视觉、分镜镜头、参考角度帧、本地素材、公网 URL 或已生成图片，先读取或生成 `Selected Asset Packet`。`prompt-director` 只转换该包对应的对象，必须保留 `Locked items`，按 `Reference roles` 使用参考物，并把 `Avoid` 写入负面/限制条件。

如果是角色设定图、场景设定图或一体式分镜板，按需读取 `Prompts/Visual_Development_Board_Rules.md`。默认只输出一张/一组的 prompt，不批量输出全部分镜组。

### 提示词修改策略

用户要求微调时，只改相关参数：

- 距离问题：改景别、主体占比、裁切、背景信息量。
- 风格问题：改色彩、光线、材质、元素密度。
- 视频冲击力：改运镜速度、主体占比变化、前景、节奏点。
- 产品稳定：加强形状、比例、标签、材质一致性和禁止变形。

## 阶段 8：终审

| 项目 | 规则 |
| --- | --- |
| 进入条件 | 方案、海报或视频已接近交付 |
| 目标 | 找问题，不再发散创意 |
| 最多提问 | 0-2 个；只问会影响交付的问题 |
| 默认消耗 | 低 |
| 输出 | 必改项、可选优化、版权/品牌/平台风险、交付结论；有必改项时附 `Review Delta Packet` |
| 禁止 | 在终审阶段随意提出新创意方向 |
| 退出条件 | 可以交付，或明确列出必须修改项 |

### 终审优先级

1. 事实错误、价格、时间、地点、活动规则。
2. 品牌和版权风险。
3. 平台尺寸、时长、字幕可读性。
4. 视觉和节奏优化。

### Review Delta Packet

终审发现必改项时，先压缩成轻量交接包，再进入变更处理，避免重新发散：

```text
Review Delta Packet:
- Object:
- Issue type:
- Impact scope:
- Fix route:
- Responsible role:
- Keep unchanged:
- Evidence/reference:
- Cost lane:
```

## 阶段 9：变更处理

| 项目 | 规则 |
| --- | --- |
| 进入条件 | 用户提出修改、老板/客户反馈、方向变化，或终审产出 `Review Delta Packet` |
| 目标 | 判断影响，不直接重做 |
| 最多提问 | 2 个；只问影响等级无法判断的问题 |
| 默认消耗 | 低 |
| 输出 | S/M/L/XL 等级、影响范围、保留项、更新方案、是否回退阶段 |
| 禁止 | 覆盖旧方向；无评估地大范围重写 |
| 退出条件 | 给出修改版或确认回到哪个阶段 |

### 等级动作

- S：直接修改当前输出。
- M：更新当前阶段，保留方向。
- L：回到创意方向，旧方案保留为历史版本。
- XL：重新立项，当前对话可作为旧项目归档。

若来自 `Review Delta Packet`，必须优先保留其中的 `Keep unchanged`，只修 `Object` 对应的问题；除非明确判断为 L/XL，不要把终审反馈扩大成重做项目。

### Change Delta Packet

中途反馈、老板口头意见、甲方碎评论、录屏反馈、会议纪要、聊天记录、截图批注或非终审改稿，先压缩成 `Change Delta Packet` 再派单。它和 `Review Delta Packet` 的区别是：前者处理制作过程中的反馈，后者处理终审必改项。

```text
Change Delta Packet:
- Source feedback:
- Object:
- Requested change:
- Impact scope:
- Fix route:
- Responsible role:
- Keep unchanged:
- Cost lane:
```

若来自 `Change Delta Packet`，必须先判断 S/M/L/XL，再只修 `Object` 对应范围。S/M 级可进入 quick edit；L/XL 才回到方向或重新立项。

## 阶段 10：归档与复盘

| 项目 | 规则 |
| --- | --- |
| 进入条件 | 用户要求保存、归档、总结、给公司复用 |
| 目标 | 把对话结果整理成文件或 SOP |
| 最多提问 | 2 个；优先问归档名称和用途 |
| 默认消耗 | 低到中 |
| 输出 | 项目摘要、最终方案、关键提示词、变更记录、复盘建议 |
| 禁止 | 默认把所有对话全文塞进文档 |
| 退出条件 | 用户能复用或移交 |

## 阶段跳转规则

- Brief 不完整但用户只要快速方向：可直接给方向，并标注默认假设。
- 方向未锁定时，不进入详细 AI 图像/视频 prompt。
- 用户只要 prompt：可跳到阶段 7，但必须补足用途、画幅/时长、主体。
- 用户提出修改：立即进入阶段 9，再回到对应阶段。
- 用户说“直接给我最终版”：仍先做最低限度 Brief 压缩，再给一版，不批量发散。
- 每次阶段跳转都重新执行自动派单，不沿用上一阶段岗位。

## 每轮回复长度规则

- 启动和 Brief：短，优先要点。
- 方向：表格，不超过 3 个方向。
- 海报/分镜/剪辑：可中等长度，必须可执行。
- 提示词：结构完整，但默认只给 1 版。
- 终审/变更：短而明确，先结论后原因。

## V1.5 Historical Accuracy Stage Note

- Historical/civilization checking is optional and confirmation-gated.
- Clear historical risk without confirmation only adds: `检测到历史准确性风险。是否开启历史准确性检查？默认不开启。`
- Clear historical drama, cultural-heritage, archaeology, ancient craft, intangible-heritage, dynasty-specific artifact, or museum-narrative work may add one broader nudge: `检测到历史/文博题材。可开启历史准确性检查，或使用历史剧胶片风格胶囊；默认不开启。`
- If the request is otherwise actionable, continue the normal low-cost stage route with historical checking off by default.
- After the user confirms, `historical-consultant` can enter before visual production and again after generated/selected images for image QA.
- This applies to poster key visuals, storyboard first frames, reference stills, Banana-generated images, scene/prop/wardrobe concept images, and final still review.
- For video projects, check storyboard images, still references, visual assets, and representative generated frames/stills when available; do not claim full automated video QA beyond visible frames/stills.
- The Historical Drama Style Capsule is optional visual style guidance, not historical checking. Keep it as a global baseline plus per-shot deltas; do not make it a new stage.
