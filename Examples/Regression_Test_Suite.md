# SW Regression Test Suite

Use this suite after SW architecture, routing, cost, prompt, or skill updates.

## Environment

On Windows, run skill validation with UTF-8 enabled to avoid false decode failures:

```powershell
$env:PYTHONUTF8='1'
```

## Static Checks

```powershell
$env:PYTHONUTF8='1'
Get-ChildItem .\Studio_Skills -Directory | ForEach-Object {
  python "$env:USERPROFILE\.codex\skills\.system\skill-creator\scripts\quick_validate.py" $_.FullName
}
```

Check version consistency:

```powershell
python .\tools\sw_consistency_check.py --scope repo
python .\tools\sw_sync_installed.py --dry-run
python .\tools\sw_doctor.py
rg "SW loaded successfully. Current version: V1.9.1|SW version synchronized. Current version: V1.9.1|SW rescue synchronized. Current version: V1.9.1|Current runtime version: V1.9.1" .
rg "<previous-version>" . --glob "!VERSION.md" --glob "!Architecture_Update_Log.md"
```

Feature trigger checks:

```powershell
rg "Feature_Trigger_Index|sw_help|Historical Accuracy|historical-consultant" .
rg "@sw_update|SW_UPDATE|/sw_update|SW_REFRESH" "$env:USERPROFILE\.codex\skills\sw-v1-0" "$env:USERPROFILE\plugins\sw-v1-0\skills\sw-v1-0"
rg "sw-rescue|@sw_rescue|SW_RESCUE|SW rescue synchronized" . "$env:USERPROFILE\.codex\skills\sw-rescue" "$env:USERPROFILE\plugins\sw-v1-0\skills\sw-rescue"
```

Check plugin manifest:

```powershell
Get-Content "$env:USERPROFILE\plugins\sw-v1-0\.codex-plugin\plugin.json" -Raw | ConvertFrom-Json
```

Prompt reference checks:

```powershell
Test-Path .\Prompts\Image_Aesthetic_Prompt_Reference.md
Test-Path .\Prompts\Video_Motion_Edit_Prompt_Rules.md
Test-Path .\Prompts\Visual_Development_Board_Rules.md
Test-Path .\01_Research\Oscar_Best_Picture_Visual_Reference.md
Test-Path .\01_Research\Aesthetic_Daily_Selected\Daily_Selected_Index.md
rg "Image_Aesthetic_Prompt_Reference|Video_Motion_Edit_Prompt_Rules|Visual_Development_Board_Rules|Oscar_Best_Picture_Visual_Reference|Daily_Selected_Index" .\Prompts\Prompt_Spec_Rules.md .\Studio_Skills\prompt-director\SKILL.md
```

Storyboard Visual Word checks:

```powershell
Test-Path .\storyboard-visual-word\SKILL.md
Test-Path .\storyboard-visual-word\scripts\build_scene_visual_docx.py
python "$env:USERPROFILE\.codex\skills\.system\skill-creator\scripts\quick_validate.py" .\storyboard-visual-word
rg "storyboard-visual-word|Storyboard Visual Word|视觉方案文件" .\Tool_Registry.md .\SW_Runtime_Index.md .\Studio_Skill_Dispatch_Protocol.md .\AI_Tool_Integration_Rules.md
```

Expected:

- `storyboard-visual-word` is present as a tool skill, not a Studio role.
- It triggers only for explicit visual方案文件 / Word-DOCX handoff requests.
- It routes after selected storyboard, scene, or concept images exist.

Visual development board checks:

```text
做一个角色设定图：现代女性书店店员，后面要用于 4 个镜头，先不要出图。
```

Expected:

- `production-designer` leads.
- Output is a compact Character Sheet Handoff.
- No Banana generation unless explicitly requested.

```text
把这个 30 秒脚本做成一体式分镜板，先给分组表。
```

Expected:

- `storyboard-director` leads.
- Group A covers 0-15s and Group B starts after 15s.
- Each group has at most 9 shots.
- No prompt/image generation until a group is selected.

Banana Pro runner checks:

```powershell
python .\banana-pro\scripts\generate_openrouter_image.py --help
python .\banana-pro\scripts\generate_openrouter_image.py --prompt "cinematic storyboard frame, one clear subject, no text" --dry-run --output-root "$env:TEMP\banana-regression"
$env:BANANA_PRO_DISABLE_USER_ENV_FALLBACK='1'; Remove-Item Env:OPENROUTER_API_KEY -ErrorAction SilentlyContinue; python .\banana-pro\scripts\generate_openrouter_image.py --prompt "missing key test" --output-root "$env:TEMP\banana-regression"; Remove-Item Env:BANANA_PRO_DISABLE_USER_ENV_FALLBACK -ErrorAction SilentlyContinue
```

Expected:

- help exits cleanly
- dry-run writes payload plus full/used prompt files
- missing-key returns `missing-key` without exposing secrets or claiming generation
- default Banana Pro image size is `2K`; use `1K` only for explicit fast drafts

Seedance 2.0 runner checks:

```powershell
python .\seedance-2-video\scripts\seedance_task.py --help
python .\seedance-2-video\scripts\seedance_task.py dry-run --prompt "15秒，电影感文旅镜头，晨光中古城街巷缓慢推进，石板路反光，人物自然穿行，暖色低对比，无文字，无logo。" --ratio 16:9 --duration 15 --resolution 720p --image-url https://example.com/source.png
Remove-Item Env:ARK_API_KEY -ErrorAction SilentlyContinue; python .\seedance-2-video\scripts\seedance_task.py doctor
python .\url-relay\scripts\url_relay.py doctor
python .\seedance-2-video\scripts\seedance_task.py dry-run --prompt "relay policy test" --image-url https://litterbox.catbox.moe/example.png
$env:SW_RELAY_TEMPORARY_FALLBACK='none'; python .\seedance-2-video\scripts\seedance_task.py dry-run --prompt "relay policy test" --image-url https://litterbox.catbox.moe/example.png; Remove-Item Env:SW_RELAY_TEMPORARY_FALLBACK -ErrorAction SilentlyContinue
$tmpRelay = Join-Path $env:TEMP "sw-relay-regression.png"; Set-Content -LiteralPath $tmpRelay -Value "relay-regression" -Encoding ASCII; python .\seedance-2-video\scripts\seedance_task.py doctor --image-file $tmpRelay; Remove-Item -LiteralPath $tmpRelay -Force
```

Expected:

- help exits cleanly
- dry-run prints a sanitized Ark payload without submitting
- missing-key doctor reports no usable key without exposing secrets or claiming generation
- temporary relay URL is accepted only when fallback is configured/confirmed, and rejected when fallback is forced to `none`

## Behavior Cases

Poster:

```text
/poster 做一个新品咖啡小红书海报，高级但年轻，不要太花。
```

Expected:

- Fast Path unless route is unclear.
- `brief-strategist` or `creative-director` first, not all roles.
- No detailed image prompt before direction is locked.

Presentation:

```text
/ppt 做一份给老板看的新品发布方案 PPT，希望批准 6 月上线预算。
```

Expected:

- `presentation-designer` after intake.
- No full long deck before structure/source material is confirmed.

Local tourism film proposal:

```text
/ppt 做一份地方文旅局城市形象宣传片提案 PPT，给领导汇报。
```

Expected:

- `presentation-designer`.
- Load proposal/tourism references only if needed.
- Output client decision outcome before slide copy.

Video:

```text
/video 做一个艺术市集 30 秒短视频，发抖音和视频号。
```

Expected:

- Structure before storyboard.
- Edit/sound/color roles not loaded too early.

Storyboard + Banana:

```text
/video 设计一个 15 秒咖啡广告分镜，并使用 banana 生成第一镜头。
```

Expected:

- `storyboard-director` owns the shot design first.
- `prompt-director` converts the selected shot to a visual prompt.
- `banana-pro` loads only after the prompt handoff.
- Only the first/selected frame is generated by default; no batch storyboard rendering without confirmation.

Storyboard + Seedance:

```text
/video 设计一个 15 秒文旅短片分镜，并用即梦2.0生成第一条镜头。先模拟验证。
```

Expected:

- `storyboard-director` owns the shot design first.
- `prompt-director` converts the selected shot to a Seedance-ready video prompt.
- `seedance-2-video` loads only after the prompt handoff.
- With no `ARK_API_KEY`, only dry-run/payload is produced; no real video generation is claimed.
- Only the first/selected clip is generated by default; no batch shot generation without confirmation.

Storyboard Visual Word:

```text
把这 6 张已选场景图整理成视觉方案文件，给客户看的 Word 版。
```

Expected:

- Upstream visual selection is assumed only if image paths already exist.
- `finishing-producer` can prepare handoff naming and structure.
- `storyboard-visual-word` loads as a separate Tool skill.
- Formal DOCX hides prompts, local paths, tool parameters, and generation-result tables unless the user asks for an internal appendix.

Prompt-only:

```text
/prompt-image 做一张草原城市形象片提案封面图，电影感。
```

Expected:

- `prompt-director`.
- Translate vague words into controllable visual parameters.

One-take video prompt:

```text
/prompt-video 做一个 8 秒一镜到底英雄镜头，产品从暗处被灯光扫出来，准备用即梦2.0生成。
```

Expected:

- `prompt-director` plus motion/camera support if needed.
- Read `Prompts/Video_Motion_Edit_Prompt_Rules.md`.
- Output one continuous clip prompt with start frame, 2-4 beats, camera path, end frame, continuity locks, and no visible cuts.
- Do not submit Seedance until the selected prompt/public reference URL/key/cost gate is satisfied.

Oscar/classic film visual reference:

```text
/prompt-image 给我一张电影感主视觉，参考奥斯卡最佳影片的画面语言，但不要复刻具体电影。
```

Expected:

- Read `Prompts/Image_Aesthetic_Prompt_Reference.md`.
- Read `01_Research/Oscar_Best_Picture_Visual_Reference.md` only if the answer needs a specific reference family.
- Extract visual grammar only; no copied actors, frames, logos, costumes, or protected scene replicas.

Project memory:

```text
在一个长期项目文件夹中创建 .sw/MEMORY.md 和 .sw/RULES.md 后，输入：继续做这套主视觉，客户确认品牌调性是克制电影感。
```

Expected:

- Read only relevant `.sw/` files.
- Current user request remains highest priority.
- Output may include one short line only: `记忆建议：可写入 MEMORY.md：品牌调性=克制电影感。回复“记住”即可。`
- Do not write `MEMORY.md` unless the user explicitly says `记住` or equivalent.

Change:

```text
客户说不要这么厚重，想更年轻一点。
```

Expected:

- `change-manager` first.
- S/M/L/XL classification before rewriting.

## Pass Criteria

- One visible role trace for project work.
- English-only role labels and skill IDs.
- Default 3 questions, max 5 for complex/blocked work, max 1 for low-token or "you decide".
- High-cost outputs pause for confirmation.
- Optional references are loaded only when their trigger matches.
- Startup-only and sync-only replies stay one fixed English line.
