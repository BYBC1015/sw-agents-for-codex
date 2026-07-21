# SW V1.12.13 项目经验简记

Date: 2026-06-07

## 当前项目

维护 `SW_V1.0` 设计工作室系统。当前运行版本为 `V1.12.13`，稳定入口仍是 `/sw`、`/SW_V1.0`、`@SW_V1.0`。本轮重点不是新增大框架，而是修正启动边界、工具执行速度、参考图角色和版本同步。

## 主要问题

- 启动漂移：普通“海报/PPT/分镜/提示词”等设计词曾容易误触发完整 SW。
- 版本漂移：本地运行版本、安装 skill、plugin manifest、分支名和历史回复可能不一致。
- 工具流程偏慢：显式调用 Banana/API 类 skill 时，流程会被重复 key check、doctor、参考文件读取和过多确认拖慢。
- 参考图混用：多参考图容易被全部当作全局风格，导致人物/产品长相、构图、风格、首尾帧互相串。
- 历史/文博题材：需要提醒准确性风险，但不能默认加载历史检查或扩大流程。
- 乱码误判：PowerShell 读取中文可能显示 mojibake，不能直接判断为文件损坏。

## 更新脉络

- `V1.12.10`：收窄启动门。只有 `/sw`、`@SW_V1.0`、`调用 SW_V1.0`、`拉取本项目架构`、`按本项目架构执行` 等显式入口才启动 SW。
- `V1.12.11`：增加历史/文博轻提醒和 Historical Drama Style Capsule。历史准确性仍需用户确认，不自动开启。
- `V1.12.12`：增加完整分镜规则。真实剧本镜头数优先，补充镜头必须有叙事功能，联系表按 3x3 分页，空/失败格保留黑槽。
- `V1.12.13`：优化 A6 参考角色和 Banana/API fast path。`Reference roles` 优先分为 `identity / structure / style / motion source`；Banana 明确生成一张草稿且 prompt/handoff 清楚时，直接用固定 fast 命令跑。

## 关键决策

- 不新增“大而全”的阶段；优先把闭环补到现有 `Selected Asset Packet`、`prompt-director` 和显式工具 skill。
- API key 不写入仓库、不写进交接文档、不打印完整值；用本机私密配置读取。
- 显式 “用 banana 生成一张草稿” 视为一次草稿确认；但不等于允许批量、私密素材上传、4K/final 输出或最终商用品牌/人脸/产品资产。
- API fast path 目标是少读文件、少 preflight、直接运行脚本；错误由 runner 返回后再处理。

## Banana Pro 经验

本机私密 key 设置：

```powershell
python banana-pro\scripts\generate_openrouter_image.py --setup-key
```

快速草稿生成：

```powershell
python banana-pro\scripts\generate_openrouter_image.py --fast --prompt-file <prompt.txt> --aspect-ratio "16:9"
```

实测：有效 OpenRouter key 下，`--fast` 生成 1K 图像约 25 秒完成。无效 key 会在约 1 秒内返回 `HTTP 401`，说明慢点不在 SW 流程，而在外部 API 认证或模型响应。

## 维护经验

- 修改架构/入口/skill/plugin 时必须升版本，并同步 `VERSION.md`、固定回复、README、安装 skill、plugin manifest、`Architecture_Update_Log.md`。
- 修改后先跑：

```powershell
python tools\sw_sync_installed.py
python tools\sw_consistency_check.py --scope all
python tools\sw_doctor.py --scope all
git diff --check
```

- `git diff --check` 可能提示 CRLF 将转 LF；这不等于 whitespace error。
- 发现乱码时优先用 UTF-8 读取，不做大范围编码重写。
- 真实生成资产、payload、response、API key、本地私密 config 不要提交。

## 交接提醒

- 当前推荐继续从 `V1.12.13` 分支接手。
- 下一步若继续优化，优先看 API 类工具的固定执行流和结果回注，不要先加新大阶段。
- 若要提交本经验文档，可作为单独文档提交，不需要再升版本。
