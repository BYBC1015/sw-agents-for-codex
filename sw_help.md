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
- Historical Accuracy: reminder appears only for clear accuracy risk. Say "开启历史检查" for the current request/visual chain; "本项目开启历史检查" or "全程开启历史检查" for the current conversation/project; "关闭历史检查" / "不用历史检查" / "恢复普通模式" to turn it off.

This only shows help and does not start a project.
```

## Cost Rule

Default `@sw_help` cost is one embedded answer and zero project-file reads.
