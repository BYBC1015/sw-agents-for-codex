---
name: hermes-bridge
description: "Connect Hermes with SW and Codex for shared video work."
metadata:
  version: "1.15.0"
---

# Hermes / SW collaboration

Use for a requested Hermes–Codex handoff, shared SW project work, or running SW's Kling tools from Hermes. This bridge adds local skills and a handoff convention; it does not establish an automatic agent-to-agent service.

## Resolve the shared workspace

Read `references/runtime.json` when installed. It records `sw_project_root`, `source_skill`, and `kling_runner` as non-secret local paths. In the SW repository, the workspace is the parent of this skill folder. Read the current workspace's `VERSION.md`; do not treat this skill's version as the live SW version.

For collaboration, read `references/collaboration.md`. In Hermes use `read_file`, `search_files`, and `terminal`; in Codex use the available file and command tools. Follow the working project's `AGENTS.md`. Loading this bridge does not itself enable SW: the explicit `/sw` activation gate still applies. Load only the project rules or role skills relevant to an authorized task.

## Shared Kling execution

- Read the live `kling-api/SKILL.md` in `sw_project_root` before using Kling. Reuse its `scripts/kling_task.py`; do not maintain a second API client in Hermes.
- Ordinary videos use Kling 3.0. Video reference, element replacement, and scene changes use Kling 3.0 Omni. Resolve the exact model identifier and reference mode from the live Kling skill and runner help.
- Both agents use the runner's existing private configuration at `~/.config/kling-api/secrets.json`. Do not read its values into conversation, copy it into Hermes skills, or copy it into a project handoff.
- Build one selected prompt and a dry run first. Submit generation or upload reference media only within the user's authorized scope. An integration test is not authorization for a paid generation.
- Record a task's output directory and task ID in its handoff so the other agent can resume polling. Check existing task state before resubmitting after an interruption.

## Install / refresh / check

From the SW workspace, the following helper only installs this local bridge and prints non-secret paths:

```text
python hermes-bridge/scripts/install_bridge.py
python hermes-bridge/scripts/install_bridge.py --execute
```

The first command previews; the second writes to the detected Hermes home. Pass `--hermes-home` for a named profile. It preserves unrelated skills and model configuration, and refuses to overwrite untracked or locally modified bridge files. Refresh after changing the bridge; Kling and SW documentation stay current through their shared source paths.

## Verification and limits

Check that Hermes discovers `hermes-bridge` and that `runtime.json` points at the current SW workspace. In Hermes, `skill_view(name="hermes-bridge")` explicitly loads it. New sessions can preload it with `hermes --in <workspace> --skills hermes-bridge`; do not launch a session merely to test installation.

This provides shared files and tools. It does not claim that an existing Hermes chat has received Codex's conversation or that either agent is listening in the background. A live MCP/ACP transport is separate and should be configured only when that form of collaboration is requested.
