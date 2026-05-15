# AI Tool Prompt Profiles AI工具提示词剖面

本文件定义不同类型 AI 工具的 prompt 结构。`prompt-director` 和 `tool-integrator` 在输出工具版 prompt 前，先选择对应剖面。

## 通用 Prompt 内核

所有工具都从同一个内核出发：

```text
目标：
受众：
平台/画幅/时长：
主体：
场景：
构图/镜头：
光线/色彩：
动作/变化：
风格/材质：
必须保留：
禁止出现：
后期处理：
质检项：
```

## 图像生成剖面

适合：主视觉、背景、氛围图、产品情绪图、分镜参考。

必须包含：

- 用途
- 主体和主体占比
- 构图和留白
- 景别或焦段效果
- 光线方向
- 色彩和材质
- 画幅
- 负面提示词
- 后期文字/logo区域

不适合：

- 准确中文大段文字
- 精确 logo
- 二维码
- 严格不变形的产品标签

### Banana Pro / OpenRouter 图像生成补充

仅在用户明确要求香蕉、banana、Banana Pro、Nano Banana、OpenRouter 图像生成或 `@banana-pro` 时使用。它是 `prompt-director` 之后的图像生成/出图环节，作用类似 `imagegen`，不能替代上游的分镜、版式、海报、PPT 页面、角色、产品或场景设计岗位。

输出必须包含：

- model：`google/gemini-3.1-flash-image-preview`
- modalities：`["image", "text"]`
- image_config：`aspect_ratio` 与 `image_size`
- reference roles：仅在用户提供参考图时列出，如 character reference、product reference、scene reference、composition reference
- QA checklist：主体一致性、画幅、文字/logo 风险、额外物体、可排版性

不要在普通图像提示词里自动切换到 Banana Pro；先保留通用 prompt，用户确认使用该成员后再进入生成/执行。若用户同时要求“设计分镜/海报/PPT 页面并用 banana 出图”，先产出对应设计 handoff，再转最终 prompt，再生成选中的一张/一帧。Banana Pro 已打包 OpenRouter 执行脚本；如果 `OPENROUTER_API_KEY` 未配置，只输出 dry-run payload，不声称已出图。

## 图像编辑剖面

适合：局部替换、扩图、去背景、补背景、风格统一。

必须包含：

- 原图保留项
- 修改区域
- 修改目标
- 不可改变项
- 边缘/材质/光线衔接
- 输出尺寸
- 失败判断

修改示例：

```text
只修改背景，不改变产品形状、标签位置、颜色和反光；新增背景光线方向与原图一致。
```

## 视频生成剖面

适合：短镜头、动态氛围、产品动效、分镜验证。

必须包含：

- 镜头编号
- 时长
- 起始画面
- 主体动作
- 运镜
- 结束画面
- 运动速度
- 连续性锁定
- 禁止变形/闪烁/跳切

不适合：

- 单条 prompt 生成复杂多镜头剧情
- 准确文字和 logo
- 长时间稳定人物一致性

## 视频编辑剖面

适合：自动剪辑、字幕、节奏、音乐、转场、包装。

必须包含：

- 输入素材列表
- 目标平台和时长
- 时间线结构
- 字幕策略
- BGM/音效点
- 转场规则
- 保留和删除标准
- 导出规格

## 版式/设计工具剖面

适合：Canva、在线设计、模板改版、尺寸适配。

必须包含：

- 画布尺寸
- 信息层级
- 文案分层
- 字体气质
- 颜色
- 图片区域
- logo/二维码位置
- 导出格式

不适合：

- 让生成模型直接决定最终文字准确性
- 没有品牌限制时批量套模板

## 音频/配音剖面

适合：旁白、BGM、音效、口播节奏。

必须包含：

- 使用场景
- 情绪
- 语速/BPM
- 时间点
- 音量层级
- 授权要求
- 留白位置
- 与画面动作的对应关系

## 工具版 Prompt 输出格式

```text
工具类型：
使用剖面：
通用版 Prompt：
工具版 Prompt：
关键参数：
负面/禁止项：
不可改变项：
生成后质检：
失败替代方案：
```
