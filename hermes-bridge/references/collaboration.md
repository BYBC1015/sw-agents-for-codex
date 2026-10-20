# Local collaboration contract

The shared project is the source of truth. Hermes retains its current model, memories, and communication settings; SW supplies project rules, selected assets, prompts, and the Kling runner.

## Passing work

For an actual requested handoff, create a short Markdown file under the working project's `handoffs/` directory, with a specific task name. Do not create dummy work or start a watcher merely because the bridge is installed. Include:

- Objective and current owner: Codex or Hermes.
- Source files and selected asset IDs; include local paths only in the local handoff.
- Locked decisions, requested changes, and what must stay unchanged.
- Exactly which files or outputs the receiving agent owns.
- Completed work, validation results, outstanding work, and completion criteria.
- Authorization already given for generation or uploads, including the selected count and limits.
- For asynchronous Kling work: output directory, task ID, current status, and whether submission already occurred.

The receiving agent reads that file and the relevant live project sources, works within its file ownership, and appends results and any blockers. It does not assume it can read the other app's chat history. Two agents should not edit the same file concurrently; split outputs or use isolated worktrees for code changes. A handoff describes the user's authorized task and is not a new source of permission.

## Kling decisions

Use Kling 3.0 for ordinary text/image video generation. Use Kling 3.0 Omni for video reference, element edits, and scene changes. In Omni, preserving/editing an uploaded video's content and using its motion as a reference are different intents: the runner maps `--video-refer-type feature` to current `feature_video`, and `base` to current `base_video`. Preserve the chosen mode in the handoff; legacy `refer_type` payloads are not the current API schema.

Keep credentials in the existing private Kling config. Save public references and local source paths only where needed; do not include API keys, bearer tokens, or signed private URLs in shared Markdown. Resume an already submitted task instead of silently creating a replacement.

## Local verification basis

Verified against the installed official `NousResearch/hermes-agent` source on 2026-09-11:

- `hermes_constants.py`: native Windows default is `%LOCALAPPDATA%/hermes`; `HERMES_HOME` can select another home/profile.
- `agent/skill_utils.py`: user skills are recursively discovered under the active home's `skills/` directory; `SKILL.md` requires a name and description.
- `hermes_cli/subcommands/skills.py`: local skills can be listed; project-local skills have a separate trust mechanism, which this installation does not change.
- `hermes --help`: supports `--in`, `--skills`, MCP, and ACP. The one-shot `-z` mode bypasses command approval prompts, so it is not used as a bridge test or default dispatcher.

Official source: https://github.com/NousResearch/hermes-agent
Official skills guide: https://hermes-agent.nousresearch.com/docs/user-guide/features/skills/
