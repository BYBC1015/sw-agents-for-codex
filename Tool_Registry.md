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
接入状态：本地 skill 已接入；定位等同 `imagegen` 类出图成员；已打包 OpenRouter API 执行脚本；补齐 `OPENROUTER_API_KEY` 后可在确认后真实生成图片
触发说法：香蕉、banana、@banana-pro、Banana Pro、Nano Banana、Nano Banana 2、google/gemini-3.1-flash-image-preview、OpenRouter 图像生成、用 banana-pro 生成/出图/转换
最适合：海报主视觉、分镜首帧、产品或道具概念图、角色设定图、场景底图、多参考图像提示词包
不适合：普通图片提示词的默认处理、准确中文文字、logo/二维码、未确认版权或客户敏感素材的自动上传、未经确认的额度消耗、未配置 `OPENROUTER_API_KEY` 时假装已生成图片
输入需要：用途、主体、画幅、image_size、参考图角色、风格、连续性锁定、必须避免项
输出格式：生成后的图片路径、payload、response 和 QA；未配置 key 时输出 dry-run payload
提示词格式：由 `prompt-director` 先产出通用视觉 prompt，再交给 Banana Pro 作为生成/出图环节
不可越级：若同一需求包含分镜、视频/电影镜头、海报、PPT/deck/slide、版式、角色、产品、道具或场景设计，先由对应 Studio role 产出 handoff，再由 `prompt-director` 生成最终 prompt，最后交给 Banana Pro；默认只生成选中的一张/一帧
提示词剖面：图像生成 / 图像编辑 / 多参考图像
关键参数：model `google/gemini-3.1-flash-image-preview`、modalities `["image", "text"]`、aspect_ratio、image_size、reference image roles、`OPENROUTER_API_KEY`
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
