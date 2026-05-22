# SW Version

Current runtime version: V1.9.1
Stable invocation name: SW_V1.0
Stable invocation aliases: `/sw`, `/SW_V1.0`, `@SW_V1.0`, `/sw_v1.0`, `/sw-v1-0`
Version sync aliases: `@sw_update`, `SW_UPDATE`, `/sw_update`, `/sw-update`, `SW_REFRESH`
Rescue aliases: `@sw_rescue`, `/sw-rescue`, `/sw_rescue`, `SW_RESCUE`, `SW_REPAIR`, `SW_FORCE_UPDATE`

## Version Rule

Whenever Codex updates any SW design studio architecture file, it must update the version in the same turn.

This includes changes to:
- `AGENTS.md`
- `SW_V1.0.md`
- `SW_Runtime_Index.md`
- `Project_Memory_Rules.md`
- `Project_Memory_Templates/*`
- `Feature_Trigger_Index.md`
- `sw_help.md`
- `sw_rescue.md`
- `sw-rescue` entries when stale-chat rescue behavior changes
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
- user-level rescue skill: `C:\Users\Administrator\.codex\skills\sw-rescue\SKILL.md`
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
- `sw-rescue` user/plugin skill and command when stale-chip rescue behavior changes
- `Project_Minimal_Entry_Pack.md` when cross-project entry behavior changes
- `Studio_Skill_Dispatch_Protocol.md` when studio skill dispatch behavior changes
- `Studio_Role_Label_Protocol.md` when role label, trace, or title behavior changes
- `Production_Pipeline_Map.md` when poster, video, film, prompt, or finishing pipeline behavior changes
- `Agent_Skill_Tech_Principles.md` when handoff, guardrail, eval, progressive-disclosure, or tool/script architecture changes
- `Cost_Governor.md` when cost, token, output-depth, or high-cost gate behavior changes
- `SW_Runtime_Index.md` when compact runtime behavior changes
- the version log below
- release maintenance files when infrastructure changes: `SW_System_Self_Check.md`, `Release_Rules.md`, `tools/sw_consistency_check.py`, `tools/sw_sync_installed.py`, `tools/sw_doctor.py`, and `.github/workflows/sw-ci.yml`

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
| V1.9.1 | 2026-05-21 | Replaced the Banana image-generation backend with Banana Pro using OpenRouter `google/gemini-3-pro-image-preview`, added private `~/.config/banana-pro/openrouter.env` key lookup, kept the existing SW-compatible runner entry, and preserved no-bypass/cost guardrails. |
| V1.9.0 | 2026-05-21 | Added `storyboard-visual-word` as an explicit downstream DOCX handoff tool for visual方案文件 / 视觉导演方案 / Word视觉方案 requests. It packages already-selected storyboard, scene, or concept images into a clean Word visual director document without replacing storyboard design, prompt generation, or image generation. |
| V1.8.1 | 2026-05-21 | Expanded the Oscar Best Picture visual-language reference from 20 to 30 films and added a local Daily Selected aesthetic index for user-supplied PDFs. Extracted images/contact sheets stay ignored locally; tracked files store only prompt-safe usage rules and compact indexes. |
| V1.8.0 | 2026-05-20 | Added visual-development board workflow for character setting sheets, scene setting sheets, and integrated storyboard sheets. Storyboard boards now default to 15 seconds per group, maximum 9 shots per board, with upstream handoff before Banana/Seedance generation. |
| V1.7.8 | 2026-05-20 | Added lightweight release infrastructure: repository-only CI checks for GitHub Actions, local installed-entry sync, compact SW doctor diagnostics, release rules, broader installed skill coverage, and relay-token leak scanning. |
| V1.7.7 | 2026-05-20 | Added a release consistency checker, documented root causes for entry/version mismatches, added low-token aesthetic image prompt references, added Oscar Best Picture visual-language study notes without storing copyrighted frames, and upgraded video motion/edit prompt rules for one-take, bullet-time, hero-shot, montage, match cuts, and Seedance-ready single-clip handoffs. |
| V1.7.6 | 2026-05-19 | Changed URL Relay from a hard self-host-only stop to a priority fallback chain: try the configured SW media uploader first, report when it is unreachable or server-failing, then use Litterbox/Catbox only when the user confirms fallback or local private config enables it; config/auth errors do not fallback. Added relay fallback CLI options to URL Relay and Seedance local-file upload while keeping paid generation blocked until a public URL exists. |
| V1.7.5 | 2026-05-19 | Locked URL Relay to the configured SW media uploader by default. Seedance now rejects Catbox/Litterbox-style temporary relay URLs unless the user explicitly confirms that fallback, and SW rules now stop before paid generation when the self-owned relay is unavailable. |
| V1.7.4 | 2026-05-19 | Added a standalone `sw-rescue` entry (`/sw-rescue`, `@sw_rescue`, `SW_RESCUE`) for stale or sealed SW chips. It reports the current runtime from a separate skill id, bypasses old startup/update snapshots, does not start projects, keeps normal startup/sync hot paths unchanged, and replaces a Seedance key-assignment example with a non-secret local-config reminder. |
| V1.7.3 | 2026-05-19 | Changed legacy-conversation recovery from "new conversation is reliable" to same-thread self-heal first: old conversations must read current `VERSION.md`, `SW_Runtime_Index.md`, and current loader/sync skills, override stale fixed replies in place, and recommend a new conversation only if the desktop app refuses current files. |
| V1.7.2 | 2026-05-19 | Added stale snapshot guards for old conversations and UI skill chips so current `VERSION.md` / `SKILL.md` values override cached `V1.6.0` / `V1.5.3` replies without adding normal startup or sync cost. |
| V1.7.1 | 2026-05-19 | Restored plugin slash-command discoverability by adding local `/sw`, `/sw-v1-0`, `/sw-update`, and `/sw-help` command files, expanding plugin default prompts, and rewriting the local plugin manifest as UTF-8 without BOM so the desktop loader can parse it reliably. |
| V1.7.0 | 2026-05-19 | Added `url-relay` as a public URL handoff tool for local media, integrated Seedance with `--image-file` relay uploads, documented fallback-to-temporary-relay behavior, and updated routing so local files go `prompt-director` -> `url-relay` -> downstream generator instead of blocking on missing public URLs. Relay and Seedance runners now also accept UTF-8-BOM JSON configs for Windows compatibility. |
| V1.6.0 | 2026-05-18 | Added `seedance-2-video` as an explicit-call Seedance 2.0 / 即梦2.0 video-generation tool skill with Ark dry-run/run/poll scripts, public-image-URL checks, no-key dry-run fallback, tool trace rules, and no-bypass routing after upstream Studio roles and `prompt-director`. |
| V1.5.4 | 2026-05-18 | Split startup and sync routing to reduce trigger competition: `sw-v1-0` no longer advertises `@sw_update` aliases, `sw-update` owns sync-only behavior and UI prompts, user/plugin loader skills use hot-path source guidance instead of long architecture-file lists, and garbled memory/historical help snippets in loader skills were repaired. |
| V1.5.3 | 2026-05-18 | Fixed SW Help button latency: `agents/openai.yaml` now uses a direct embedded reply instead of a recursive `@sw_help` prompt, and hot-start rules explicitly forbid shell/file reads for normal help wake-up. |
| V1.5.2 | 2026-05-18 | Added hot-start and maintenance cost controls: `@sw_help`, activation-only, and sync-only turns now use embedded fixed replies first; detailed trigger indexes, architecture logs, and full maintenance checks load only when the user asks for details, troubleshooting, publishing, or deep regression. |
| V1.5.1 | 2026-05-18 | Clarified Historical Accuracy scope controls: plain enable applies to the current request/visual chain, project-level enable requires explicit wording, close commands disable current project-level checking, and persistent long-term scope requires explicit MEMORY approval. |
| V1.5.0 | 2026-05-18 | Added optional historical/civilization accuracy checking and `sw-help`. Historical checking uses five trigger groups, gives only a low-cost reminder by default, loads `historical-consultant` only after user confirmation, and focuses on final visual output/image QA, including Banana-generated images and storyboard first frames. |
| V1.4.0 | 2026-05-15 | Added the project-local `.sw/` memory layer for long-running projects, including lightweight read priority, short MEMORY.md suggestion wording after major confirmations, write-by-explicit-user-command rules, and reusable `.sw` templates. |
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
| V1.0.4 | 2026-05-11 | Added legacy conversation recovery guidance and `SW_REFRESH`; this early strategy favored new conversations, then V1.7.3 changed recovery to same-thread self-heal first. |
| V1.0.3 | 2026-05-11 | Changed the required invocation success reply from Chinese to ASCII English to prevent mojibake; no invocation change. |
| V1.0.2 | 2026-05-11 | Added detailed update content recording rule and `Architecture_Update_Log.md`; no invocation change. |
| V1.0.1 | 2026-05-11 | Added automatic version bump rule; clarified stable invocation name stays `SW_V1.0` while runtime version can increment. |
| V1.0 | 2026-05-11 | Initial design studio workflow architecture and invocation protocol. |
