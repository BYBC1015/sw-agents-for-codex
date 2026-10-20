---
name: sw-canvas
description: SW Canvas 快速启动；新对话自动新建并绑定独立空画布，已有绑定则恢复对应项目。
---

# SW Canvas · 0.4.1

单独启动只执行以下轻量入口，不加载其他 skill、项目列表、完整交接或图片：
```powershell
$canvasRoot='{{CANVAS_ROOT}}'
& "$canvasRoot\start.ps1" -NoBrowser | Out-Null
if ([string]::IsNullOrWhiteSpace($env:CODEX_THREAD_ID)) { 'http://127.0.0.1:8961/' } else {
  & '{{PYTHON}}' -B -X utf8 "$canvasRoot\canvas_cli.py" --conversation $env:CODEX_THREAD_ID launch
}
```

用返回的 url 在当前 Codex 对话打开/复用浏览器页面。不要根据最近打开的标签页继承项目。真实对话编号不可用时只打开 http://127.0.0.1:8961/ 空白页。

- 新对话未绑定：按用户的长期偏好自动新建并绑定独立空画布，不询问项目名，不列旧项目、不沿用最近标签页；launch 按真实对话编号幂等创建。用户说明制作目标后可据此命名。
- 同一对话已有明确绑定：恢复对应画布；仅打开时不自动读取项目内容。
- 用户明确指定新建、切换、导入、处理或交接时，再读 ~/.codex/skills/media-canvas/SKILL.md。
- 启动后一句短答即可。不启动 SW 工作室，不执行媒体队列。
- 旧画布出现 `ERR_CONNECTION_REFUSED` 时，先运行上述 `start.ps1 -NoBrowser` 恢复服务；这不需要 `launch`，不会新建或改绑项目。然后刷新用户明确指定的原画布 URL。Windows 后台服务独立于启动命令；电脑重启后仍需启动一次，网页刷新本身不能启动本机程序。

## 画布优先回传

结果登记到画布后，聊天默认只回项目/节点/任务编号、版本、短结论与画布链接。不手动重复嵌入生成图片、原图或整板截图；用户明确要求在对话看图时才按需展示。生成工具自身必须展示的输出仍遵循工具规则，不再手动发第二遍。不得声称能删除旧对话图片、隐藏工具自动输出，或保证消除上下文卡顿。
只有视觉判断需要时才读取选定的必要预览，不把全项目图片加入上下文。不要每次回复截图整块画布。
