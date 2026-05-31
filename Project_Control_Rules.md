# Project Control Rules 对话控制规则

## V1.1.0 Question Override

Default project replies ask 3 useful questions. Complex campaign, film, tool-risk, or blocked-delivery turns may ask up to 5. Low-token, speed, "少问", or "你定" turns ask at most 1 and continue with clear assumptions.

本文件是 Codex 的“项目控制层”。它只在当前对话已经显式启用 SW 后生效，不替代 `Stage_Runbook.md`，而是规定用户在对话里如何快速指挥 Codex，以及 Codex 如何按模式、质量门和平台默认值执行。未显式输入 `/sw`、`@SW_V1.0`、`调用 SW_V1.0`、`按本项目架构执行` 等入口时，不因普通设计词自动进入这些控制规则。

## 工作模式

用户没有指定时，默认使用“标准模式”。

| 模式 | 触发说法 | Codex 行为 | 适合场景 |
| --- | --- | --- | --- |
| 省 token 模式 | 省 token / 快速 / 先别展开 | 每轮只给结论、关键假设、下一步；不写长方案 | 前期判断、改稿评估 |
| 标准模式 | 默认 | 少量追问，给可执行方案；不批量发散 | 日常海报、视频、分镜 |
| 精修模式 | 精修 / 细化 / 给完整执行版 | 输出更完整的版式、分镜、剪辑、提示词 | 方向已定、准备制作 |
| 公司交付模式 | 给公司看 / SOP / 汇报版 | 增加结构、检查项、交接话术和风险说明 | 推荐给团队或汇报 |

### 模式切换规则

- 用户可随时说“切到省 token 模式/标准模式/精修模式/公司交付模式”。
- 切模式不重启项目，只改变输出粒度。
- 高消耗任务在省 token 模式下只输出骨架，不输出完整 prompt 或多版本。
- 精修模式也不默认批量生成，除非用户明确要多版。

## 快捷口令

用户可以用很短的指令推进项目。Codex 需要识别并执行，不要让用户重复解释。

| 用户口令 | Codex 应做 |
| --- | --- |
| 继续 | 按当前阶段的下一步推进 |
| 你定 | 使用行业常规默认值并说明关键假设 |
| 少问 | 每轮最多 1 个问题，能默认就默认 |
| 展开 | 从当前结果进入更详细版本 |
| 收短 | 压缩成结论和下一步 |
| 给 3 个方向 | 进入创意方向，最多 3 个 |
| 对比一下 / 哪个更好 / 保留什么 | 对方向、分镜组或 deck 结构输出轻量 Compare Board，只收口保留/删除/下一版 |
| 选 A / 选 B / 选 C | 锁定方向并进入下一阶段 |
| 出海报方案 | 进入海报方案 |
| 出PPT方案 / 出deck | 进入 presentation/deck 方案，主责 `presentation-designer` |
| 出PPT大纲 | 进入 deck structure，先由 `presentation-designer` 给章节流和页面角色 |
| 评审PPT | 进入 presentation review，由 `presentation-designer` + `review-producer` 检查逻辑、层级、可读性和交付风险 |
| 出分镜 | 进入视频分镜 |
| 出剪辑表 | 进入剪辑方案 |
| 改海报 / 修图 / 出单张 / 出四版 / 照图二 | 进入海报快速改稿；优先输出图，不重跑完整项目 |
| 改PPT / 改分镜 / 改剪辑表 / 改提示词 | 进入 quick edit；最多问 1 个阻塞问题，只改选中页、镜头、时间段或参数 |
| 用这张 / 用这个镜头 / 选中这页 / 交给工具 | 生成轻量 Selected Asset Packet，再交给 `prompt-director` 或显式工具 |
| 出图片提示词 | 进入提示词专项，按图片规则输出 |
| 出视频提示词 | 进入提示词专项，按视频镜头规则输出 |
| 终审 | 进入终审，只找风险和必改项 |
| 改成... | 进入变更处理，判断 S/M/L/XL |
| 记住 / 写入 MEMORY / 保存项目规则 | 将上一条明确的重大确认简短追加到 `.sw/MEMORY.md`，不要扩写 |
| 归档 | 整理项目摘要、最终方案、提示词和变更记录 |

快捷口令只改变用户意图；具体岗位仍由 `Auto_Assignment_Rules.md` 根据项目类型、当前阶段和用户意图自动派单。

## 对话状态输出

Codex 不要每轮都展示完整状态卡。只有以下情况展示轻量状态：

- 新项目启动。
- 用户问“现在到哪了”。
- 阶段切换。
- 发生 L/XL 级变更。

轻量状态格式：

```text
当前阶段：[阶段]
已锁定：[最多 4 项]
默认假设：[最多 3 项]
下一步：[将产出的内容]
```

## 质量门

每个阶段退出前，Codex 需要默默检查质量门。只有用户要求终审或保存时才完整展示。

| 质量门 | 阶段 | 必须满足 | 未满足时 |
| --- | --- | --- | --- |
| G0 项目识别 | 启动 | 类型、目标、平台至少明确 2 项 | 只问最关键问题 |
| G1 Brief | Brief | 目标、受众、核心信息、必须出现 | 标注默认假设后继续 |
| G2 方向 | Direction | 不超过 3 个方向，有推荐项 | 不生成精修方案 |
| G2B 对比 | Direction/Storyboard/Presentation | 有明确 `Keep` / `Remove` / `Next version` | 先收口，不直接重写整套方案 |
| G3 制作方案 | Poster/Presentation/Storyboard/Edit | 可执行到软件层面 | 补齐文案、页面角色、镜头、素材或时间线 |
| G4 提示词 | Prompt | 有主体、构图、景别、光线、限制 | 按 `Prompt_Spec_Rules.md` 补齐参数 |
| G5 交付 | Review | 信息、版权、品牌、平台规格检查过 | 列出必改项，并用 `Review Delta Packet` 交给变更处理；不说“可交付” |

## 平台默认规则

这些是日常工作默认建议，不替代平台最新官方要求。真正上线前仍按平台后台和客户规范复核。

| 平台/场景 | 默认处理 | 重点风险 |
| --- | --- | --- |
| 小红书海报/封面 | 3:4 或 4:5；标题要在移动端一眼可读 | 字太小、信息太密、封面不抓眼 |
| 朋友圈海报 | 1:1 或 3:4；信息克制，适合快速扫读 | 文字堆叠、二维码太小 |
| 抖音短视频 | 9:16；前 3 秒必须有钩子；字幕避开底部 UI | 开场弱、字幕被遮挡、节奏拖 |
| 视频号短视频 | 9:16 优先；节奏可比抖音略稳 | 信息不清、标题封面弱 |
| B站视频 | 16:9 优先；更重结构和叙事 | 封面标题不清、节奏过碎 |
| 线下海报 | 先问印刷尺寸；默认提醒出血、分辨率、CMYK | 小字不可读、素材精度不足 |
| Canva 快速稿 | 强调模板可改、尺寸适配、多人协作 | 字体替换、品牌不一致 |
| PowerPoint/Keynote 汇报 | 默认先做章节流和页面角色，再做版式；保留可编辑 PPTX | 逻辑跳跃、字太小、图表不可读、导出字体丢失 |
| Adobe 精修稿 | 强调图层、源文件、素材授权、导出规范 | 图层混乱、后期不可改 |

## 交付物判断

Codex 先判断用户真正要的交付物，再决定阶段深度。

| 用户需求 | 交付物 | 默认深度 |
| --- | --- | --- |
| “帮我想想” | Brief + 3 个方向 | 低到中 |
| “做海报” | 海报文案 + 版式 + 主视觉说明 | 中 |
| “改这张海报” | 快速判断问题 + 直接改图/出图 + 3 条以内 QA 说明 | 低到中 |
| “做PPT/汇报/deck” | 章节流 + 页面角色 + 标题结论策略 + 版式方向 | 低到中 |
| “做视频” | 结构 + 分镜 + 剪辑表 | 中 |
| “给提示词” | 1 条主 prompt + 负面 prompt + 修改项 | 中 |
| “给最终效果” | 最终呈现说明 + 执行清单 | 中 |
| “给公司看” | 汇报版方案 + 风险 + 下一步 | 中到高 |

## 风险处理

出现以下情况时，Codex 先提醒风险，再给低成本替代方案：

- 使用真实名人、受版权保护角色或相似品牌资产。
- 要 AI 直接生成 logo、二维码、准确中文大段文字。
- 把海报主标题、发布标题、大数字、发光字、金属字等视觉文字用普通系统字体覆盖，导致画面变素。
- 用户要求照搬参考图。
- 产品形状、包装、标签可能被 AI 改变。
- 视频需要多镜头连续人物或产品一致性。
- 时间紧但需求仍频繁变化。

## 输出压缩规则

用户说“省 token / 收短 / 快速”时，使用这个格式：

```text
结论：
默认假设：
下一步：
需要你确认的 1 个问题：
```

用户说“精修 / 展开”时，使用这个格式：

```text
目标：
方案：
执行：
风险：
下一步：
```

## Poster Control Difference

Poster work should default to visual editing, not document-style text layout. Unlike PPT/deck pages or storyboard annotation sheets, a poster usually does not need system-font reconstruction. For poster requests, SW should mostly handle feedback, visual judgment, edit instructions, and QA. Use system/editable text only for exact information text, small copy, legal/logo/QR, or explicit editable-layer delivery.

## Compare Board And Quick Edit

When the user needs to compare directions, storyboard groups, or deck structures, use a lightweight Compare Board instead of expanding a new proposal:

```text
Compare Board:
- Keep:
- Remove:
- Next version:
```

Quick edit applies to existing poster/images, deck pages or outlines, storyboard groups or selected shots, edit-plan segments, and prompt refinements. Ask at most one blocking question and output the revised object first. If the change affects audience, core message, narrative structure, visual style, or delivery format, route through `change-manager` before rewriting.

When the user selects a concrete poster visual, deck page visual, storyboard shot/group, reference frame, local media file, public URL, generated image, or concept image for prompt/tool handoff, use a lightweight Selected Asset Packet before `prompt-director`, URL Relay, Banana, Seedance, Kling, DOCX, or Feishu:

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

Do not use it as a new planning stage; it only preserves the selected object, locks, reference roles, avoid list, next tool, and upload/cost decision.

## Reply-End Nudge

For ordinary project work, output the requested product first. Add at most one final light reminder only when it helps production:

- memory nudge for likely long-running projects or durable decisions
- lock nudge for character, scene, selected asset, reference role, style, or aspect ratio
- next-step nudge for the smallest useful next action
- risk nudge for copyright, logo, exact text, privacy, platform, or tool cost
- cost nudge before high-cost generation or broad expansion

Skip the nudge when there is no useful reminder. Do not add multiple reminders, do not expand into a checklist, and do not read extra files just to produce the nudge.

Midstream feedback should become a `Change Delta Packet` when it is more than a tiny wording tweak. If feedback arrives as a screen recording, meeting note, chat log, screenshot annotation, boss oral note, or client comment, first compress it into the packet before rewriting:

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

## V1.5 Historical Accuracy Controls

- `开启历史检查`, `要考据`, `按历史准确做`: enable `historical-consultant` for the current request/current visual-output chain.
- `本项目开启历史检查`, `全程开启历史检查`: keep historical checking on for the current conversation/project until closed.
- `只检查这张`, `只检查这一帧`: use historical checking for one image/frame only.
- `关闭历史检查`, `不用历史检查`, `恢复普通模式`, `只是古风`, `好看优先`: keep or turn historical checking off.
- If the setting was saved in `.sw/MEMORY.md`, permanent closure requires an explicit memory update/delete command.
- If clear historical risk appears but the user has not enabled it, add this line: `检测到历史准确性风险。是否开启历史准确性检查？默认不开启。`
- Continue normal low-cost project work unless the user confirms historical checking.
- Historical checking must judge final visible image/still results, not just the prompt.
- For video projects, check storyboard images, still references, visual assets, and representative Seedance output frames when available. Do not claim full automated video QA beyond visible frames/stills.
