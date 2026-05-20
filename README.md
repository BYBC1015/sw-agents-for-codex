# Codex 设计全流程自动化模板

这是一套面向设计师个人日常工作的 Codex 项目模板，用来管理海报、PPT/deck、视频分镜、剪辑方案、最终效果说明、AI 生成资产、改稿记录和 token 成本。

第一版目标不是把创意变成僵硬流水线，而是让每个项目都有清楚的输入、确认点、版本记录和交付检查。你可以把 Codex 当作创意总控、PPT 策划、资料整理员、分镜助理、剪辑策划、终审检查员和变更管理员。

更推荐的使用方式是：每次新建一个对话，就当作新建一个项目。Codex 会读取 `AGENTS.md`，自动判断项目类型，少量追问，并在对话框里推进完整流程。

## 当前版本

- 当前运行版本：`V1.8.0`
- 稳定调用入口：`/sw`、`/SW_V1.0` 或 `@SW_V1.0`
- 版本同步入口：`@sw_update`
- 完整更新记录：[`VERSION.md`](VERSION.md) / [`Architecture_Update_Log.md`](Architecture_Update_Log.md)

## 更新日志

首页展示完整版本历史，方便打开仓库时快速判断当前能力和演进过程；更详细的影响范围以 `Architecture_Update_Log.md` 为准。

| 版本 | 日期 | 更新内容 |
| --- | --- | --- |
| V1.8.0 | 2026-05-20 | 新增视觉开发板流程：角色设定图、场景设定图和一体式分镜板。角色设定支持大人设、正背侧、表情、细节、剪影和色卡；一体式分镜默认 15s 一组、最多 9 镜头一张，超过即自动拆组，并保持 Banana/Seedance 不越级规则。 |
| V1.7.8 | 2026-05-20 | 增加轻量发布基础设施：GitHub Actions 仓库级 CI、本机 installed-entry 同步脚本、SW doctor 诊断、Release 规则、更多入口覆盖检查和 relay token 泄露扫描，降低版本错位和入口丢失风险。 |
| V1.7.7 | 2026-05-20 | 增加发布一致性检查脚本和系统自检记录，修复版本源漂移风险；新增图片审美提示词备用库、奥斯卡最佳影片画面语法参考（不保存版权截图），并强化一镜到底、子弹时间、英雄镜头、蒙太奇、match cut、speed ramp 等视频运镜/剪辑提示词规则。 |
| V1.7.6 | 2026-05-19 | URL Relay now uses a clear priority chain: SW media uploader first; if unreachable/server-failing, report the failure and use Litterbox/Catbox only when fallback is confirmed or enabled in private local config. Config/auth errors do not fallback. Added fallback flags to URL Relay and Seedance local-file uploads. |
| V1.7.5 | 2026-05-19 | Locked URL Relay to the configured SW media uploader by default. Seedance now rejects Catbox/Litterbox temporary relay URLs unless the user explicitly confirms that fallback, and SW stops before paid generation when the self-owned relay is unavailable. |
| V1.7.4 | 2026-05-19 | Added independent `sw-rescue` rescue entry: when old `SW_V1.0` or `SW Update` chips keep replaying stale versions, use `/sw-rescue`, `@sw_rescue`, or `SW_RESCUE` in the same conversation. It does not start projects, does not add cost to normal startup/sync, and includes a Seedance key-example cleanup to avoid false-positive secret scans. |
| V1.7.3 | 2026-05-19 | 将旧对话恢复策略改为“原地自愈优先”：旧对话遇到旧版本回复时，先在同一线程读取当前 `VERSION.md`、`SW_Runtime_Index.md` 和当前 loader/sync skill 覆盖旧快照；只有桌面端拒绝加载当前文件时才建议新建对话。 |
| V1.7.2 | 2026-05-19 | 新增旧快照防呆：当历史对话、压缩上下文或 UI skill 芯片混入 `V1.6.0` / `V1.5.3` 等旧回复时，强制以当前 `VERSION.md` / `SKILL.md` 为准；正常启动、同步仍保持一行热路径，不增加消耗。 |
| V1.7.1 | 2026-05-19 | 修复本地插件斜杠命令不可见问题：新增 `/sw`、`/sw-v1-0`、`/sw-update`、`/sw-help` 命令文件，补充插件默认入口，并将本地插件清单重写为无 BOM 的 UTF-8，便于桌面端稳定识别。 |
| V1.7.0 | 2026-05-19 | 新增 `url-relay` 公网 URL 中转工具层；本地图片/视频可先上传到 SW media uploader，再交给 Seedance/即梦2.0、Ark 或未来图生视频工具使用；服务器不可用时保留 prompt/payload，可切到安全临时中转或用户提供的公网 URL；脚本兼容 Windows UTF-8-BOM 配置文件。 |
| V1.6.0 | 2026-05-18 | 新增 `seedance-2-video` 即梦2.0/Seedance 2.0 视频生成工具成员；支持 Ark dry-run/run/poll、无 key 模拟验证、显式触发、不可越级和高消耗确认。 |
| V1.5.4 | 2026-05-18 | 拆分启动与同步路由，减少 skill 竞争触发；`sw-v1-0` 不再声明 `@sw_update`，`sw-update` 独立负责同步；loader skill 改为热路径来源说明并修复乱码片段。 |
| V1.5.3 | 2026-05-18 | 修复 SW Help 按钮响应慢：按钮默认提示不再递归调用 `@sw_help`，而是直接携带短答，并禁止普通帮助唤醒时读文件或跑命令。 |
| V1.5.2 | 2026-05-18 | 优化 SW 唤醒与维护成本：`@sw_help` 默认走内置短答，`@sw_update` 和纯启动只回固定短句；详细触发词、日志、全量回归改为按需读取。 |
| V1.5.1 | 2026-05-18 | 明确历史准确性检查的作用范围：普通开启只作用于本次请求/当前视觉链路；本项目开启需要明确口令；关闭口令可恢复普通模式。 |
| V1.5.0 | 2026-05-18 | 新增可选历史/文明准确性检查和 `@sw_help` 帮助入口；确认后重点检查最终视觉输出、Banana 生成图、分镜首帧和图片阶段资产。 |
| V1.4.0 | 2026-05-15 | 新增长期项目 `.sw/` 本地记忆层：项目可保存 `PROJECT.md`、`RULES.md`、`MEMORY.md` 等小文件；重大确认后只给一句短建议，用户说“记住”才写入。 |
| V1.3.5 | 2026-05-15 | 为 `banana-pro` 增加不可越级规则和草稿提速默认值：分镜/海报/PPT/场景等任务必须先走对应 Studio role 和 `prompt-director`，再生成选中画面；默认 1K 草稿、整理输出目录、提示词压缩、图片路径展示、减少重复 key 检查和无图重试。 |
| V1.3.4 | 2026-05-15 | 为 `banana-pro` 增加 Windows 用户级 `OPENROUTER_API_KEY` fallback，方便本机写入 key 后无需重启也能读取。 |
| V1.3.3 | 2026-05-15 | 将 `banana-pro` 正式打包为可执行图像生成 skill，新增 OpenRouter API 脚本；配置 `OPENROUTER_API_KEY` 后可真实出图，未配置时只 dry-run/payload。 |
| V1.3.2 | 2026-05-15 | 修正 `banana-pro` 派单显示和查找路径：它不再被当作 Studio role，而是单独显示为 Tool skill，并明确读取 `banana-pro/SKILL.md`、用户级或插件级 skill。 |
| V1.3.1 | 2026-05-15 | 校准 `banana-pro` 定位：它是提示词之后的图像生成/出图成员，作用类似 `imagegen`；触发词扩展为“香蕉 / banana / Banana Pro / Nano Banana”等。 |
| V1.3.0 | 2026-05-15 | 新增 `banana-pro` 图像生成成员和工具卡；仅在用户明确要求 Banana Pro / Nano Banana / OpenRouter 图像生成时调用，普通图片提示词仍走 `prompt-director`。 |
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
| V1.0.4 | 2026-05-11 | 增加历史对话恢复指南和 `SW_REFRESH`；早期以新对话为可靠路径，已在 V1.7.3 改为旧对话原地自愈优先。 |
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
SW loaded successfully. Current version: V1.8.0
```

Version synchronization uses a separate entry:

```text
@sw_update
```

Expected reply:

```text
SW version synchronized. Current version: V1.8.0
```

If old startup/update chips keep replaying stale versions, use the standalone rescue entry:

```text
/sw-rescue
```

or:

```text
@sw_rescue
```

Expected reply:

```text
SW rescue synchronized. Current version: V1.8.0
```

For other project folders, copy `SW_V1.0.md`, `sw_update.md`, and `sw_rescue.md`; copying only the startup file will not create the local update/rescue entries. For long-running projects, also copy `Project_Memory_Templates/.sw/` into that project folder.

Feature help:

```text
@sw_help
```

Default `@sw_help` and the SW Help button now use a hot-start short answer. Detailed trigger indexes load only when you ask for full triggers or debugging.

Seedance 2.0 Video is optional and explicit-only. Trigger it with `即梦2.0生成`, `即梦生成`, `Seedance 2.0`, or `@seedance-2-video`; SW will still run storyboard/prompt work first when needed, then generate only the selected clip/shot.

URL Relay is the media bridge for tools that need public URLs. Trigger it with `URL中转`, `公网URL`, `上传参考图`, `上传参考视频`, or `@url-relay`; Seedance can use it automatically when a local reference file needs a public `http(s)` URL. The priority is SW media uploader first, then confirmed/configured temporary fallback only if the SW server is unreachable.

Historical Accuracy is optional. Plain `开启历史检查` applies only to the current request/visual chain; `本项目开启历史检查` or `全程开启历史检查` keeps it on for the current conversation/project; `关闭历史检查`, `不用历史检查`, or `恢复普通模式` turns it off.

长期项目记忆层建议：

```text
.sw/
  PROJECT.md
  RULES.md
  MEMORY.md
  CHANGELOG.md
  ASSETS.md
```

重大确认后，SW 只会用一句短提示建议写入，例如：`记忆建议：可写入 MEMORY.md：品牌调性=克制电影感。回复“记住”即可。`

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
- `Command_Aliases.md`：备用文本快捷调用入口；日常优先使用 `/sw`、`/SW_V1.0` 或 `@SW_V1.0`。
- `Studio_Professional_Standards.md`：专业设计工作室输出标准。
- `Stage_Runbook.md`：每个阶段的进入条件、输出、退出条件和消耗等级。
- `Project_Control_Rules.md`：对话快捷口令、工作模式、质量门和平台默认规则。
- `Studio_Skill_Map.md`：小型工作室岗位分工和 skill 路由，包含 `presentation-designer` PPT/deck 岗位。
- `Auto_Assignment_Rules.md`：根据项目类型、阶段和用户意图自动分配岗位 skill。
- `AI_Tool_Integration_Rules.md`：AI/设计工具适配、工具版 prompt 转换和新增工具流程。
- `AI_Tool_Prompt_Profiles.md`：不同 AI 工具类型的提示词剖面。
- `Tool_Registry.md`：工具注册表，未来接入工具时先登记工具卡。
- `banana-pro/`：显式调用的 Banana Pro / Nano Banana 图像生成 skill，包含 OpenRouter API 执行脚本；补齐 `OPENROUTER_API_KEY` 后可在提示词后真实生成图片。
- `seedance-2-video/`：显式调用的 Seedance 2.0 / 即梦2.0 视频生成 skill，包含 Ark API dry-run/run/poll 脚本；补齐 `ARK_API_KEY` 或本地私密 key 后可在提示词后真实生成视频。
- `url-relay/`：公网 URL 中转 skill，优先使用 SW media uploader 服务器把本地图片/视频上传成下游 AI 工具可抓取的 `http(s)` URL；自有服务器不可用时可按确认/配置切到临时中转；上传 token 只存本机私密配置，不进入仓库。
- `Seedance_URL_Relay_Codex_Handoff.md`：只迁移即梦2.0与 URL Relay 中转策略的标准接入指令，不包含完整 SW 框架。
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
- `Prompts/Image_Aesthetic_Prompt_Reference.md`：图片审美、减少 AI 感、电影画面语言的按需参考。
- `Prompts/Video_Motion_Edit_Prompt_Rules.md`：一镜到底、子弹时间、英雄镜头、复杂运镜和剪辑手法的按需参考。
- `Prompts/Visual_Development_Board_Rules.md`：角色设定图、场景设定图和一体式分镜板的按需参考。
- `01_Research/Oscar_Best_Picture_Visual_Reference.md`：奥斯卡最佳影片画面语法暂存参考，不保存版权截图。
- `SW_System_Self_Check.md` / `tools/sw_consistency_check.py` / `tools/sw_doctor.py`：维护发布前检查入口、版本一致性、安装入口同步诊断和密钥泄露预检。
- `tools/sw_sync_installed.py`：把仓库里的 SW 入口、工具 skill 和插件命令同步到本机 Codex 用户级 skill 与本地插件。
- `Release_Rules.md` / `.github/workflows/sw-ci.yml`：轻量发布规则和 GitHub Actions 仓库级自检。
- `Examples/`：海报、视频、PPT/deck 和改稿测试样例。
- `Examples/Regression_Test_Suite.md`：维护和升级后用于检查路由、版本、UTF-8 校验和高成本门的回归测试。

## 使用习惯

每个新项目可以复制整套模板，也可以只复制需要的文件夹。建议保留 `Change_Log.md` 和 `Token_Budget.md`，它们是控制反复改稿和 AI 消耗的核心。
