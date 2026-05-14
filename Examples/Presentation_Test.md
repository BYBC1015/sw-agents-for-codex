# Presentation / PPT Test

Use this as a lightweight regression case for SW presentation routing.

## Input

```text
/ppt
我要做一份给老板看的新品发布方案 PPT，核心是让老板批准 6 月上线预算。已有产品卖点和竞品截图，但还没有完整文案。
```

## Expected Routing

```text
Studio roles: Studio Orchestrator / `studio-orchestrator` + Brief Strategist / `brief-strategist` (loaded). Cost lane: intake.
```

Then the next production turn should route to:

```text
Studio roles: Presentation Designer / `presentation-designer` (loaded). Cost lane: production.
```

## Expected Behavior

- Identify project type as `presentation/deck/PPT`.
- Ask no more than 3 useful questions unless the delivery is blocked.
- Produce a low-cost brief first, then a deck structure or section flow.
- Do not generate a full long deck, batch slide copy, or tool-specific Canva/PowerPoint output before the structure is confirmed.
- Preserve handoff to `copywriter`, `layout-designer`, `asset-producer`, `review-producer`, and `finishing-producer`.

## Pass Criteria

- `presentation-designer` is selected for deck structure, slide outline, section flow, speaker flow, and title takeaway strategy.
- `layout-designer` is selected only when the request is specifically about grid, type hierarchy, spacing, or visual layout execution.
- `review-producer` is selected for final PPT review, delivery risk, accessibility, and export checks.

## Specialized Case

```text
/ppt
做一份地方文旅局城市形象宣传片提案 PPT，给领导汇报，希望能说明为什么要拍、拍成什么样、如何体现城市价值和交付标准。
```

Expected:

- Route to `presentation-designer`.
- Load `references/client-facing-proposal.md` and `references/local-tourism-film-proposal.md` only if the turn needs specialized proposal logic.
- Keep research to the smallest useful amount, usually 1-2 pages.
- Output client decision outcome, film task, positioning, structure, image method, and delivery standard before visual polish.
