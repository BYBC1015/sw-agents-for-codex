# SW Version

Current runtime version: V1.3.5
Stable invocation name: SW_V1.0
Stable invocation aliases: `/SW_V1.0`, `@SW_V1.0`, `/sw_v1.0`, `/sw-v1-0`
Version sync aliases: `@sw_update`, `SW_UPDATE`, `/sw_update`, `SW_REFRESH`

## Version Rule

Whenever Codex updates any SW design studio architecture file, it must update the version in the same turn.

This includes changes to:
- `AGENTS.md`
- `SW_V1.0.md`
- `SW_Runtime_Index.md`
- `Agent_Skill_Tech_Principles.md`
- `Command_Aliases.md`
- `README.md`
- `Start_New_Project.md`
- `Project_Control_Rules.md`
- `Stage_Runbook.md`
- `Studio_Skill_Map.md`
- `Studio_Skill_Dispatch_Protocol.md`
- `Studio_Role_Label_Protocol.md`
- `Production_Pipeline_Map.md`
- `Cost_Governor.md`
- `Auto_Assignment_Rules.md`
- `Studio_Professional_Standards.md`
- `AI_Tool_Integration_Rules.md`
- `AI_Tool_Prompt_Profiles.md`
- `Tool_Registry.md`
- `Prompts/*`
- `Studio_Skills/*/SKILL.md`
- user-level skill: `C:\Users\Administrator\.codex\skills\sw-v1-0\SKILL.md`
- user-level sync skill: `C:\Users\Administrator\.codex\skills\sw-update\SKILL.md`
- user-level plugin: `C:\Users\Administrator\plugins\sw-v1-0`

## Bump Policy

- Patch version: wording, small rules, prompt refinements, minor compatibility fixes.
- Minor version: new workflow stage, new studio role, new tool integration layer, or meaningful routing change.
- Major version: breaking invocation change, incompatible architecture change, or company/team SOP rewrite.

## Required Sync Points

When the version changes, update:
- this file's `Current runtime version`
- all success replies: `SW loaded successfully. Current version: Vx.x.x`
- user-level skill success reply
- user-level plugin `plugin.json` version
- `Architecture_Update_Log.md` detailed update entry
- `Legacy_Conversation_Recovery.md` when historical conversation compatibility changes
- `sw_update.md` when version sync behavior changes
- `Project_Minimal_Entry_Pack.md` when cross-project entry behavior changes
- `Studio_Skill_Dispatch_Protocol.md` when studio skill dispatch behavior changes
- `Studio_Role_Label_Protocol.md` when role label, trace, or title behavior changes
- `Production_Pipeline_Map.md` when poster, video, film, prompt, or finishing pipeline behavior changes
- `Agent_Skill_Tech_Principles.md` when handoff, guardrail, eval, progressive-disclosure, or tool/script architecture changes
- `Cost_Governor.md` when cost, token, output-depth, or high-cost gate behavior changes
- `SW_Runtime_Index.md` when compact runtime behavior changes
- the version log below

## Update Content Recording

Every version bump must record update content in `Architecture_Update_Log.md`.

Each entry must include:
- what changed
- why it changed
- affected files or modules
- invocation impact
- token/cost impact when relevant
- backward compatibility note

## Version Log

| Version | Date | Change |
| --- | --- | --- |
| V1.3.5 | 2026-05-15 | Added Banana Pro no-bypass routing and draft-speed defaults: storyboard/poster/PPT/scene design must hand off through the responsible Studio role and `prompt-director` before Banana generation; Banana drafts now default to 1K, use organized output folders, prompt compression, inline markdown paths, no repeated key-check preflight, and one retry for no-image responses. |
| V1.3.4 | 2026-05-15 | Added a Windows user-environment fallback for `OPENROUTER_API_KEY` in the Banana Pro runner so locally saved keys can be read without requiring a Codex restart. |
| V1.3.3 | 2026-05-15 | Packaged `banana-pro` as an executable OpenRouter image-generation skill with a bundled standard-library Python script; generation works after `OPENROUTER_API_KEY` is configured, while missing-key runs only create dry-run payloads. |
| V1.3.2 | 2026-05-15 | Fixed `banana-pro` dispatch display and lookup rules so it is shown as a separate Tool skill, not a Studio role, and loaded from the project, user-level, or plugin-level Banana Pro skill path. |
| V1.3.1 | 2026-05-15 | Corrected `banana-pro` positioning as a post-prompt image-generation member similar to `imagegen`, and expanded explicit triggers to include 香蕉 / banana / Banana Pro / Nano Banana. |
| V1.3.0 | 2026-05-15 | Added the explicit-call `banana-pro` image-generation member, registered its Banana Pro / Nano Banana / OpenRouter tool card, and updated routing/cost rules so it only loads when the user explicitly requests it. |
| V1.2.5 | 2026-05-14 | Added an OpenAI Agents SDK-inspired dispatch pattern for role handoffs, blocking guardrails, lightweight tracing, session/state carryover, and tool-boundary safety, with drawbacks documented. |
| V1.2.4 | 2026-05-14 | Expanded the README homepage changelog to include the complete version history instead of only recent entries. |
| V1.2.3 | 2026-05-14 | Added a README homepage changelog and current-version block so GitHub visitors can see the active runtime, recent updates, and full log entry points immediately. |
| V1.2.2 | 2026-05-14 | Added Fast Path dispatch to reduce routing file reads, added UTF-8 validation guidance, and introduced a unified regression test suite for safer maintenance. |
| V1.2.1 | 2026-05-14 | Upgraded `presentation-designer` with progressive references for client-facing proposal decks, local tourism/city image film proposal PPTs, cinematic visual rules, layer/overlay QA, and proposal cost gates. |
| V1.2.0 | 2026-05-14 | Added dedicated `presentation-designer` role, PPT/deck command aliases, presentation stage rules, and auto-assignment routing based on researched presentation structure, accessibility, and PPTX placeholder practices. |
| V1.1.2 | 2026-05-12 | Added presentation/PPT/deck routing and review support without adding new roles; decks now route through copy, layout, asset, review, and finishing roles. |
| V1.1.1 | 2026-05-11 | Added agent/skill technical principles from official research: progressive disclosure, handoff packets, guardrail gates, state continuation, observability trace, eval loop, and script/tool design rules. |
| V1.1.0 | 2026-05-11 | Major studio-role update: added poster/video/film full-pipeline roles, English-only role labels, production pipeline map, role trace protocol, and 3-5 question guidance while preserving low-token gates. |
| V1.0.8 | 2026-05-11 | Added compact runtime index and UTF-8 fallback guidance so new conversations can load SW with lower token use and fewer encoding issues. |
| V1.0.7 | 2026-05-11 | Added runtime cost governor, English role trace, high-cost gate, and self-check rules for smoother low-consumption use. |
| V1.0.6 | 2026-05-11 | Added mandatory scoped Studio sub-skill dispatch protocol with visible role trace; clarified minimum project-folder entry pack behavior. |
| V1.0.5 | 2026-05-11 | Added `@sw_update` version synchronization entry, separate user-level `sw-update` skill, and minimum project-folder entry pack; kept project invocation unchanged. |
| V1.0.4 | 2026-05-11 | Added legacy conversation recovery guidance and `SW_REFRESH`; clarified that new conversations are the reliable path after updates. |
| V1.0.3 | 2026-05-11 | Changed the required invocation success reply from Chinese to ASCII English to prevent mojibake; no invocation change. |
| V1.0.2 | 2026-05-11 | Added detailed update content recording rule and `Architecture_Update_Log.md`; no invocation change. |
| V1.0.1 | 2026-05-11 | Added automatic version bump rule; clarified stable invocation name stays `SW_V1.0` while runtime version can increment. |
| V1.0 | 2026-05-11 | Initial design studio workflow architecture and invocation protocol. |
