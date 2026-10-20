---
name: media-canvas
description: SW Canvas 项目协作：明确选择后绑定、导入、版本回写与完整交接；启动用 sw-canvas。
---

# SW Canvas 协作 · 0.4.0

CLI：{{CANVAS_ROOT}}\canvas_cli.py，使用 {{PYTHON}} -B -X utf8。
软件与 SW 工作室独立；软件维护、打开或交接不授权媒体制作。

## 定位与低消耗读取

- 对话编号只取实际 CODEX_THREAD_ID。先用 --conversation CID binding 核对绑定；不从最近浏览页面猜目标。无绑定时按用户长期偏好用 --conversation CID launch 自动新建并绑定独立空画布，不再询问项目名；返回后重新读 binding。无真实对话编号时仅打开未绑定空白页。
- 所有对话操作固定 --conversation CID --project PID；写入另带本轮 binding 返回的 --binding-version N，全局参数放在子命令前。冲突时核对目标，不移除防护重试。
- 开始协作只读 summary。保留返回的 cursor；同项目再次检查用 summary --since CURSOR，unchanged 时不重复读。短摘要会标明截断字段。
- 对选区/指定任务工作，用 packet --nodes NODE 或 packet --task T001 --limit 3；需要完整路径、圈注或结果时再 detail。执行前必须读完相关任务要求与约束，不能用截断摘要代替。
- 不默认读取整项目、旧聊天、所有图片或反复截图。仅当用户明确接续/完整交接时读取 project-handoff；按实际问题展开对应 section 和分页，保留完整信息。
- 本地 CLI 可直接用，避免为一个操作重复发现全部网页工具。网页默认仅 5 项轻量工具，需要操作时调用一次 enable_canvas_actions；普通读取不展开写入工具。

## 写入与接续

首次写入时按需读 [接口参考](references/api.md)，不要每轮重读。
用户指定项目名时精确搜索（--limit 3）；有歧义才列候选。新建后绑定当前对话。项目文件默认在 T:\Work素材\项目名\过程、交付、.canvas；原项目不迁移。
导入助手直接处理，临时附件用 copy 保留原件。执行任务固定输入；已有结果用 result 一次登记文件、来源版本和说明，进入待确认。纯讨论 intent=discuss，不能附制作媒体结果；不自动跑队列。
记录用户确认的版本取舍、决定和下一步；不把假设写成确认。完整交接先更新已确认信息，再 checkpoint 和 handoff --checkpoint ID；恢复时核对当前修订与输出，避免重复制作。快照包含完整文字和引用，不复制媒体。
写入用 UTF-8 JSON 文件和稳定 requestId；响应不明时原样重试。不要把画布状态写进无关 SW MEMORY。

## 镜头与连续性

用户要求保存、修改或验收分镜时，按需读取接口参考中的 0.4.0 分镜章节。`storyboard` 读取镜头或实体；`storyboard-impact` 在改公共资产前列出受影响镜头；`shot-packet` 固定生成所用的版本和锁定项。`storyboard-edit` 只更新指定对象，保存版本历史。新版本的输出必须重新验收；写 pass 前看实际图片并记录依据。`storyboard-export --final` 会拒绝缺图、依赖过期或未通过验收的镜头。软件操作不自动授权生成、上传或费用。

## 画布优先回传

结果登记到画布后，聊天默认只回项目/节点/任务编号、版本、短结论与画布链接。不手动重复嵌入生成图片、原图或整板截图；用户明确要求在对话看图时才按需展示。生成工具自身必须展示的输出仍遵循工具规则，不再手动发第二遍。不得声称能删除旧对话图片、隐藏工具自动输出，或保证消除上下文卡顿。
只有视觉判断需要时才读取选定的必要预览，不把全项目图片加入上下文。不要每次回复截图整块画布。
