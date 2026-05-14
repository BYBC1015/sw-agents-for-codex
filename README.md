# Codex 设计全流程自动化模板

这是一套面向设计师个人日常工作的 Codex 项目模板，用来管理海报、PPT/deck、视频分镜、剪辑方案、最终效果说明、AI 生成资产、改稿记录和 token 成本。

第一版目标不是把创意变成僵硬流水线，而是让每个项目都有清楚的输入、确认点、版本记录和交付检查。你可以把 Codex 当作创意总控、PPT 策划、资料整理员、分镜助理、剪辑策划、终审检查员和变更管理员。

更推荐的使用方式是：每次新建一个对话，就当作新建一个项目。Codex 会读取 `AGENTS.md`，自动判断项目类型，少量追问，并在对话框里推进完整流程。

## 当前版本

- 当前运行版本：`V1.2.5`
- 稳定调用入口：`/SW_V1.0` 或 `@SW_V1.0`
- 版本同步入口：`@sw_update`
- 完整更新记录：[`VERSION.md`](VERSION.md) / [`Architecture_Update_Log.md`](Architecture_Update_Log.md)

## 更新日志

首页展示完整版本历史，方便打开仓库时快速判断当前能力和演进过程；更详细的影响范围以 `Architecture_Update_Log.md` 为准。

| 版本 | 日期 | 更新内容 |
| --- | --- | --- |
| V1.2.5 | 2026-05-14 | 加入 OpenAI Agents SDK-inspired dispatch pattern，用 handoff、guardrails、tracing 和 session/state 思路增强 SW 岗位派单，同时记录真实 SDK 接入的依赖、隐私和过度派单风险。 |
| V1.2.4 | 2026-05-14 | 将 README 首页更新日志扩展为完整版本历史，不再只展示最近几条，方便 GitHub 首页直接查看全部演进记录。 |
| V1.2.3 | 2026-05-14 | 在 README 首页增加当前版本和最近更新日志，打开 GitHub 仓库即可看到运行版本、调用入口和完整日志入口。 |
| V1.2.2 | 2026-05-14 | 增加 Fast Path 派单，减少常规项目的路由文件读取；补充 UTF-8 校验和统一回归测试。 |
| V1.2.1 | 2026-05-14 | 升级 `presentation-designer`，强化客户提案型 PPT、地方文旅/城市形象片提案、电影感视觉和交付检查。 |
| V1.2.0 | 2026-05-14 | 新增独立 `presentation-designer` 岗位，加入 PPT/deck 命令别名、阶段规则和自动派单。 |
| V1.1.2 | 2026-05-12 | 增加 presentation/PPT/deck 路由和审查支持，可通过现有工作室岗位处理。 |
| V1.1.1 | 2026-05-11 | 增加 agent/skill 技术原则：渐进式读取、handoff packet、guardrail gate、状态延续、可观测 trace、eval loop 和脚本/工具设计规则。 |
| V1.1.0 | 2026-05-11 | 重磅扩展为海报、视频、电影/品牌片全流程工作室；新增英文岗位标注、制作链路图和 3-5 个关键问题规则。 |
| V1.0.8 | 2026-05-11 | 增加紧凑运行索引和 UTF-8 fallback 指南，让新对话加载 SW 更省 token，并减少编码异常。 |
| V1.0.7 | 2026-05-11 | 增加 runtime cost governor、英文 role trace、高消耗确认门和自检规则，让低消耗使用更稳定。 |
| V1.0.6 | 2026-05-11 | 增加强制 Studio 子 skill 派单协议，要求真实项目读取对应岗位 skill，并显示轻量岗位痕迹。 |
| V1.0.5 | 2026-05-11 | 增加 `@sw_update` 版本同步入口、独立 `sw-update` skill 和跨项目最小入口包。 |
| V1.0.4 | 2026-05-11 | 增加历史对话恢复指南和 `SW_REFRESH`，说明新对话是更新后的可靠路径。 |
| V1.0.3 | 2026-05-11 | 将调用成功回复改为 ASCII 英文，避免新对话出现中文乱码。 |
| V1.0.2 | 2026-05-11 | 增加详细更新内容记录规则和 `Architecture_Update_Log.md`。 |
| V1.0.1 | 2026-05-11 | 增加自动版本号升级规则，并明确入口名 `SW_V1.0` 保持稳定。 |
| V1.0 | 2026-05-11 | 初始设计工作室自动化架构和调用协议。 |

## 对话式启动

每次新建对话时，最推荐先调用：

```text
/SW_V1.0
```

或：

```text
@SW_V1.0
```

调用成功后，Codex 应回复：

```text
SW loaded successfully. Current version: V1.2.5
```

Version synchronization uses a separate entry:

```text
@sw_update
```

Expected reply:

```text
SW version synchronized. Current version: V1.2.5
```

For other project folders, copy both `SW_V1.0.md` and `sw_update.md`; copying only the startup file will not create the local update entry.

Project work now uses visible Studio role dispatch. For real deliverables, SW should read the selected `Studio_Skills/<skill>/SKILL.md` files and include a compact trace such as:

```text
Studio roles: Brief Strategist / `brief-strategist` + Storyboard Director / `storyboard-director` (loaded). Cost lane: intake.
```

然后你再发送项目诉求，Codex 会按本项目的设计工作室架构执行。

完整写法也可以：

```text
请读取本项目的 AGENTS.md，把这个对话当作一个新的设计项目来跑。
我的需求是：
[粘贴客户/老板/自己的原话]
```

更短的版本：

```text
按 AGENTS.md 跑一个新设计项目：
[需求原话]
```

如果你只是在对话里完成项目，不需要每次手动填写所有模板。模板文件用于保存、归档、复盘或团队化。

其他命令别名只是备用，不需要记。

## 快速开始

1. 在 `00_Brief/Brief.md` 填入客户或老板的原始需求。
2. 让 Codex 根据 Brief 输出 `02_Direction/Creative_Direction.md`，最多只保留 3 个方向。
3. 确认方向后，再进入 `03_Poster/Poster_Workflow.md` 或 `04_Storyboard/Storyboard.md`。
4. 每次需求变化都先写进 `Change_Log.md`，再决定是否重做、局部修改或保留旧版。
5. 每次准备调用高成本任务前，先检查 `Token_Budget.md`。
6. 完成前用 `06_FinalReview/Final_Review_Checklist.md` 做品牌、版权、平台和交付检查。
7. 交付后按 `99_Archive/Archive_Guide.md` 归档。

## 推荐工作流

```text
需求澄清
  -> 风格研究
  -> 创意方向
  -> 海报方案 / 视频脚本
  -> 分镜与剪辑方案
  -> AI 资产生成或人工制作
  -> 终审检查
  -> 交付归档
```

## 成本控制原则

- 低成本阶段：只做需求拆解、方向、结构、清单、短文案。
- 中成本阶段：做海报版式、分镜表、镜头语言、剪辑节奏、字幕和音效建议。
- 高成本阶段：做长篇方案、批量变体、图像生成、视频生成、复杂重写。
- 任何高成本任务开始前，必须先有明确方向、尺寸、风格、品牌限制和验收标准。

## 文件说明

- `AGENTS.md`：Codex 自动运行的对话规则，每个新对话按它启动项目。
- `SW_V1.0.md`：`/SW_V1.0` 与 `@SW_V1.0` 调用协议。
- `PULL_ARCHITECTURE.md`：新对话拉取本项目架构的最简入口。
- `Command_Aliases.md`：备用文本快捷调用入口；日常优先使用 `/SW_V1.0` 或 `@SW_V1.0`。
- `Studio_Professional_Standards.md`：专业设计工作室输出标准。
- `Stage_Runbook.md`：每个阶段的进入条件、输出、退出条件和消耗等级。
- `Project_Control_Rules.md`：对话快捷口令、工作模式、质量门和平台默认规则。
- `Studio_Skill_Map.md`：小型工作室岗位分工和 skill 路由，包含 `presentation-designer` PPT/deck 岗位。
- `Auto_Assignment_Rules.md`：根据项目类型、阶段和用户意图自动分配岗位 skill。
- `AI_Tool_Integration_Rules.md`：AI/设计工具适配、工具版 prompt 转换和新增工具流程。
- `AI_Tool_Prompt_Profiles.md`：不同 AI 工具类型的提示词剖面。
- `Tool_Registry.md`：工具注册表，未来接入工具时先登记工具卡。
- `Studio_Skills/`：每个岗位一个 project-local `SKILL.md`。
- `Start_New_Project.md`：新项目启动语和最小输入示例。
- `00_Brief/Brief.md`：项目需求入口。
- `01_Research/Research_Board.md`：风格、竞品、参考、素材风险整理。
- `02_Direction/Creative_Direction.md`：最多 3 个创意方向。
- `03_Poster/Poster_Workflow.md`：海报创作与交付模板。
- `04_Storyboard/Storyboard.md`：视频分镜与镜头规划。
- `05_EditPlan/Edit_Plan.md`：剪辑节奏、音效、字幕和最终呈现说明。
- `06_FinalReview/Final_Review_Checklist.md`：交付前检查表。
- `Change_Log.md`：需求变化和改稿记录的唯一入口。
- `Token_Budget.md`：AI 消耗分级、确认点和预算记录。
- `Prompts/Prompt_Library.md`：日常可复制的提示词库。
- `Examples/`：海报、视频、PPT/deck 和改稿测试样例。
- `Examples/Regression_Test_Suite.md`：维护和升级后用于检查路由、版本、UTF-8 校验和高成本门的回归测试。

## 使用习惯

每个新项目可以复制整套模板，也可以只复制需要的文件夹。建议保留 `Change_Log.md` 和 `Token_Budget.md`，它们是控制反复改稿和 AI 消耗的核心。
