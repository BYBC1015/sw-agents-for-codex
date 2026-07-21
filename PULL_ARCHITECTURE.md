# 拉取本项目架构

新建对话后，只需要发送：

```text
拉取本项目架构，并按设计工作室流程执行。
我的诉求是：
[把客户/老板/自己的原话贴在这里]
```

Codex 应该自动执行以下动作：

1. 读取 `AGENTS.md`。
2. 按 `SW_Runtime_Index.md` 和 `Cost_Governor.md` 先走 Fast Path。
3. 按 `Studio_Skill_Dispatch_Protocol.md` 读取本轮选中的 `Studio_Skills/<skill-id>/SKILL.md`。
4. 路线不清、阶段冲突或复杂项目时，再按 `Auto_Assignment_Rules.md` 判断项目类型、阶段和主责岗位。
5. 多阶段交接或完整流程才读取 `Production_Pipeline_Map.md`；`Studio_Skill_Map.md` 只在岗位边界冲突时作为参考，不作为默认派单入口。
6. 如需图片或视频提示词，按 `Prompts/Prompt_Spec_Rules.md` 和工具适配规则执行。
7. 每轮最多问 3 个关键问题；如果用户说“少问”，最多问 1 个。

## 最短可用写法

```text
拉取本项目架构：
[需求原话]
```

## 示例

```text
拉取本项目架构：
做一个新品咖啡小红书海报，高级但年轻，不要太花。
```

```text
拉取本项目架构：
做一个艺术市集 30 秒短视频，发抖音和视频号，要轻松、有城市感。
```

## 注意

这是“项目内架构拉取”，不是复杂插件命令。只要新对话的工作目录是本项目，Codex 就能按这些文件执行。当前默认派单链路以 `SW_Runtime_Index.md`、`Studio_Skill_Dispatch_Protocol.md` 和 `Auto_Assignment_Rules.md` 为准。
