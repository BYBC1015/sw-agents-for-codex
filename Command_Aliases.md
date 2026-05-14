# Command Aliases 快捷调用入口

本文件定义“文本型斜杠命令”和“文本型 @ 调用”。目标是让用户不用每次粘贴完整启动语。

注意：这些命令是本项目规则识别的文本别名，不等同于宿主 UI 原生注册的斜杠菜单。只要新对话能读取 `AGENTS.md`，Codex 就应按这些别名执行。

## 新项目启动

### SW_V1.0 主入口

以下命令用于调用本项目架构：

```text
/SW_V1.0
```

```text
@SW_V1.0
```

调用成功后必须先回复：

```text
SW loaded successfully. Current version: V1.2.5
```

如果只输入调用命令，回复成功语后停止等待诉求。如果调用命令后附带需求，先回复成功语，再继续执行项目流程。

Version sync:

```text
@sw_update
```

Required reply:

```text
SW version synchronized. Current version: V1.2.5
```

Historical conversation fallback:

```text
SW_REFRESH
```

Use this only when an old conversation is stuck on a previous cached SW version. New conversations are the reliable path after updates.

以下命令等价于：

```text
请读取当前项目的 AGENTS.md，把这个对话当作一个新的设计工作室项目来跑。
需求是：
[用户输入]
```

## 项目类型快捷启动

### 海报

```text
/poster [需求原话]
```

等价规则：

```text
按 AGENTS.md 跑一个新的设计工作室项目。项目类型默认是海报。
需求是：[需求原话]
```

### 视频

```text
/video [需求原话]
```

等价规则：

```text
按 AGENTS.md 跑一个新的设计工作室项目。项目类型默认是视频。
需求是：[需求原话]
```

### 海报 + 视频

```text
/campaign [需求原话]
```

等价规则：

```text
按 AGENTS.md 跑一个新的设计工作室项目。项目类型默认是海报+视频整合传播。
需求是：[需求原话]
```

### PPT / Presentation / Deck

```text
/ppt [需求原话]
```

```text
/deck [需求原话]
```

```text
/slides [需求原话]
```

等价规则：

```text
按 AGENTS.md 跑一个新的设计工作室项目。项目类型默认是 presentation/deck/PPT。
需求是：[需求原话]
```

## 阶段快捷命令

这些命令不一定新建立项；如果已有上下文，就按当前项目继续推进。

| 命令 | 等价意图 | 主责岗位 |
| --- | --- | --- |
| `/brief [需求]` | 压缩成可执行 Brief | `brief-strategist` |
| `/directions` | 给 3 个以内创意方向 | `creative-director` |
| `/deck-plan [需求]` | 出 PPT 结构、章节流和页面角色 | `presentation-designer` |
| `/slide-review` | 检查 PPT 逻辑、层级、可读性和交付风险 | `presentation-designer` + `review-producer` |
| `/poster-plan` | 出海报文案、版式、主视觉说明 | `poster-art-director` |
| `/storyboard` | 出视频结构和分镜表 | `storyboard-director` |
| `/edit-plan` | 出剪辑时间线、字幕、BGM、音效 | `edit-director` |
| `/prompt-image [需求]` | 出图片生成提示词 | `prompt-director` |
| `/prompt-video [需求]` | 出视频镜头提示词 | `prompt-director` |
| `/review` | 终审检查 | `review-producer` |
| `/change [反馈]` | 改稿影响评估 | `change-manager` |
| `/tool [工具说明]` | 新增或适配 AI/设计工具 | `tool-integrator` |

## 工作模式快捷命令

| 命令 | 行为 |
| --- | --- |
| `/lite` | 切到省 token 模式 |
| `/standard` | 切到标准模式 |
| `/polish` | 切到精修模式 |
| `/company` | 切到公司交付模式 |

## 解析规则

- 命令后的全部内容都视为用户原始需求，不要求用户再填表。
- 新项目统一使用 `/SW_V1.0` 或 `@SW_V1.0`；旧入口不再推荐，避免插件列表出现多个工作室入口。
- `/poster`、`/video`、`/campaign`、`/ppt`、`/deck`、`/slides` 会预设项目类型，但仍按 `Auto_Assignment_Rules.md` 自动派单。
- 如果命令和上下文冲突，以用户命令为准。
- 如果用户只输入命令、没有需求，Codex 默认问 3 个关键问题；复杂整案、电影、工具风险或交付阻塞最多问 5 个；若用户同时写“少问/省 token/你定”，最多问 1 个。
