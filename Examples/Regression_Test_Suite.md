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
rg "Current version: V1.2.5|Current runtime version: V1.2.5" .
rg "V1.2.5" .
rg "<previous-version>" . --glob "!VERSION.md" --glob "!Architecture_Update_Log.md"
```

Check plugin manifest:

```powershell
Get-Content "$env:USERPROFILE\plugins\sw-v1-0\.codex-plugin\plugin.json" -Raw | ConvertFrom-Json
```

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

Prompt-only:

```text
/prompt-image 做一张草原城市形象片提案封面图，电影感。
```

Expected:

- `prompt-director`.
- Translate vague words into controllable visual parameters.

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
