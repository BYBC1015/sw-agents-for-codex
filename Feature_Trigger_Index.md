# Feature Trigger Index

This is SW's compact feature trigger index. Use it for `@sw_help`, `/sw_help`, feature discovery, and low-cost trigger checks.

## Banana Pro

Purpose: explicit image generation after SW prompt preparation.

Trigger only when the user explicitly asks for:

- `香蕉`
- `banana`
- `Banana Pro`
- `Nano Banana`
- `@banana-pro`
- OpenRouter image generation
- use Banana to generate/output an image

Default route:

```text
upstream Studio role if needed -> prompt-director -> banana-pro
```

Do not trigger for ordinary image prompt drafting.

## Historical Accuracy

Purpose: optional historical/civilization accuracy gate for visual outputs, especially poster key visuals, storyboard first frames, Banana-generated images, reference-image QA, and final image review.

Historical checking is not just prompt wording. When enabled, it checks the final visual asset/image for anachronism and credibility.

### Five Trigger Groups

1. Historical accuracy intent:
   - 历史准确, 考据, 严谨, 符合史实, 不要穿帮, 复原, 学术, 依据, 可考, 博物馆级, 纪录片级

2. Dynasty/period specificity:
   - 夏商周, 秦汉, 魏晋, 隋唐, 宋元明清, 民国
   - 初唐, 盛唐, 晚唐, 北宋, 南宋, 明代, 清代
   - 朝代考究, 时代背景, 某朝服饰, 某朝建筑

3. Civilization/archaeology/site:
   - 古埃及, 两河, 波斯, 希腊, 罗马, 玛雅, 印度河
   - 良渚, 古蜀, 三星堆, 殷墟, 敦煌, 龟兹, 楼兰
   - 考古, 遗址, 文物, 墓葬, 壁画, 器物复原

4. Material culture / production design:
   - 服饰, 甲胄, 官服, 冠帽, 发髻, 妆容
   - 建筑, 家具, 器物, 纹样, 兵器, 车马, 礼制, 祭祀
   - 道具, 场景复原, 历史人物造型

5. Serious historical project context:
   - 博物馆展陈, 文物宣传片, 历史纪录片, 文旅历史片
   - 非遗, 城市历史片, 历史人物专题, 学校/政府/院所汇报
   - 展览, 科普, 教材, 学术展示

### Non-Triggers

Do not trigger or remind for style-only phrases by themselves:

- 国风
- 古风
- 唐风
- 宋韵
- 东方美学
- 敦煌感
- 新中式
- 仙侠感

If the user says "只是氛围", "不要太考据", "好看优先", "商业感优先", or "随便古风", do not trigger historical checking.

### Reminder Threshold

Do not auto-load `historical-consultant`.

Add a one-line reminder when:

- group 1 is hit, or
- group 5 is hit, or
- a dynasty/civilization/site term is combined with a concrete visual object from group 4.

Reminder text:

```text
检测到历史准确性风险。是否开启历史准确性检查？默认不开启。
```

Load `historical-consultant` only after the user confirms with words such as:

- 开启
- 要考据
- 需要准确
- 是
- 按历史准确做

If the request is otherwise actionable, continue the normal low-cost route with historical checking off by default unless the user confirms.

### Scope And Close

Default scope is the current request or current visual-output chain only. It is not automatically permanent.

Scope commands:

- `开启历史检查`: enable for the current request/visual chain.
- `本项目开启历史检查`, `全程开启历史检查`: enable for the current conversation/project until closed.
- `只检查这张`, `只检查这一帧`: enable for one image/frame only.
- `记住历史检查规则`: only after explicit memory approval, write a short rule to `.sw/MEMORY.md` for long-term projects.

Close commands:

- `关闭历史检查`, `不用历史检查`, `恢复普通模式`: turn off historical checking for the current conversation/project.
- `本次不用考据`, `这张不用考据`: skip historical checking for the current request/image only.
- If the rule was saved in `.sw/MEMORY.md`, closing it permanently requires an explicit memory update/delete command.

### Output Quality Scope

When enabled, historical accuracy applies to:

- Period Lock Card before production
- prompt constraints before image generation
- Banana Pro generated image QA
- storyboard first-frame image QA
- poster/key visual QA
- reference-image review
- final delivery review

It does not assume any video-generation module exists. Video-stage historical quality currently focuses on still frames, storyboard images, and visual asset decisions.

## Help Entry

Use `@sw_help`, `/sw_help`, `SW_HELP`, or "SW 帮助 / 功能触发词" to show a short feature list.
