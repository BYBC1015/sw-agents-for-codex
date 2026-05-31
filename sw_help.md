# sw_help

`@sw_help` / `/sw_help` shows a short list of SW optional features and trigger rules.

## Hot Path

For normal help wake-up, do not read extra files. Answer from the embedded short help below and stop.

For the SW Help UI button, `agents/openai.yaml` should contain the final short reply directly rather than `@sw_help`; this avoids recursive skill lookup and file reads in fresh conversations.

Read `Feature_Trigger_Index.md` only when the user asks for:

- detailed trigger words
- one feature's full rules
- help-system troubleshooting
- a feature audit before release

Do not start a project. Do not load Studio roles. Do not run shell commands for normal help.

## Embedded Short Help

```text
SW Help:
- Banana Pro: trigger with 香蕉 / banana / Banana Pro / Nano Banana / @banana-pro / 用 banana 出图.
- Seedance 2.0 Video: trigger with 即梦2.0生成 / 即梦生成 / Seedance 2.0 / @seedance-2-video / 用即梦生成视频.
- URL Relay: trigger with URL中转 / 公网URL / 上传参考图 / 上传参考视频 / @url-relay. Used before Seedance when local files need public URLs. Priority: SW media uploader first; if unreachable, use confirmed/configured temporary fallback.
- Black Background Cutout: trigger with 抠图 / 扣图 / 去底 / 去黑底 / 黑底转透明 / 透明底 PNG / @black-background-cutout. Fast local transparent PNG preview for black/simple solid backgrounds; not finishing-grade.
- Storyboard Visual Word: trigger with 视觉方案文件 / 视觉导演方案 / Word视觉方案 / DOCX视觉方案 / @storyboard-visual-word after selected storyboard or scene images are ready.
- Feishu Docs: trigger with 转到飞书 / 同步到飞书 / 发布到飞书 / 飞书视觉方案 / 飞书分镜 / Lark Docs / @feishu-docs after the visual plan or storyboard handoff is ready.
- Aesthetic Decision: trigger with /aesthetic, "SW decide the look", 自动选择审美, 审美画像, or moodboard direction. Reads the compact decision index first and does not load raw images by default.
- Obsidian Aesthetic Vault: trigger with Obsidian审美库 / 整理审美库 / 筛选审美图片 / 打开审美资料库. Syncs the active Obsidian vault with embedded local preview images; normal SW work still uses the compact index.
- SW Rescue: trigger with /sw-rescue / @sw_rescue / SW_RESCUE when old SW chips keep returning stale versions.
- Historical Accuracy: reminder appears only for clear accuracy risk. Say "开启历史检查" for the current request/visual chain; "本项目开启历史检查" or "全程开启历史检查" for the current conversation/project; "关闭历史检查" / "不用历史检查" / "恢复普通模式" to turn it off.

This only shows help and does not start a project.
```

## Cost Rule

Default `@sw_help` cost is one embedded answer and zero project-file reads.
