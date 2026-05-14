# 短视频项目测试样例

## 测试目标

验证模板能否从活动需求生成分镜、剪辑节奏、字幕和最终呈现说明。

## 原始需求

```text
要做一个 30 秒短视频，介绍一个周末艺术市集，风格要轻松、有城市感，主要发抖音和视频号，希望看完让大家想来现场。
```

## 建议测试步骤

1. 填写 `00_Brief/Brief.md`。
2. 在 `01_Research/Research_Board.md` 记录参考：城市漫步、市集摊位、手作、现场音乐、人群互动。
3. 用 `02_Direction/Creative_Direction.md` 生成 3 个方向。
4. 选定主方向后，用提示词 `8. 视频脚本与分镜`。
5. 把结果填入 `04_Storyboard/Storyboard.md` 或 `04_Storyboard/Storyboard.csv`。
6. 用提示词 `9. 剪辑节奏方案`，填入 `05_EditPlan/Edit_Plan.md`。
7. 用提示词 `10. 字幕优化` 和 `11. 音效与音乐建议`。
8. 最后用 `06_FinalReview/Final_Review_Checklist.md` 终审。

## 验收标准

- 前 3 秒钩子清楚。
- 每个镜头都有素材需求。
- 字幕和音乐策略可执行。
- 能区分 Premiere/AE 精剪与剪映快剪的执行方式。

