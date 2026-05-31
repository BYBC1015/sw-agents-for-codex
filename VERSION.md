# SW Version

Current runtime version: V1.12.10
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
- release maintenance files when infrastructure changes: `INSTALL_SW.md`, `SW_System_Self_Check.md`, `Release_Rules.md`, `tools/sw_consistency_check.py`, `tools/sw_sync_installed.py`, `tools/sw_bootstrap.py`, `tools/sw_doctor.py`, and `.github/workflows/sw-ci.yml`

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
| V1.12.10 | 2026-06-01 | Narrowed SW activation to explicit invocation only. Ordinary design-topic wording such as poster, PPT, deck, storyboard, image prompt, video prompt, review, or revision no longer starts the full SW framework by itself. `/poster`, `/video`, `/ppt`, `/storyboard`, `/prompt-image`, and similar project aliases now apply only after SW has already been activated or when combined with `/sw`, `@SW_V1.0`, `调用 SW_V1.0`, `拉取本项目架构`, or `按本项目架构执行`. Skill metadata and installed plugin descriptions were narrowed to avoid implicit cross-device auto-entry. |
| V1.12.9 | 2026-06-01 | Added `black-background-cutout` as a narrow local cutout tool skill. Explicit 抠图/扣图/去底/去黑底/黑底转透明/透明底 PNG requests now route to a local Pillow-based pixel workflow for black or simple solid-background transparent PNG previews. It does not use prompt writing, AI generation, upload, or full project routing, and it must warn that quick cutouts may have slight fringing and are not finishing-grade assets. |
| V1.12.8 | 2026-06-01 | Clarified lightweight async feedback intake without adding a new lane or packet. Screen recordings, meeting notes, chat logs, screenshot annotations, boss oral comments, and client comments now route into the existing `Change Delta Packet` before rewrite/classification, preserving `Keep unchanged` and the smallest affected object. |
| V1.12.7 | 2026-06-01 | Added a lightweight reply-end nudge habit without adding a new workflow lane or default file read. Normal project replies now put the deliverable first and may add at most one short reminder for memory, locking, next step, risk, or cost only when it prevents a likely mistake. Long-running project signals are now explicit in `Project_Memory_Rules.md`, and mojibake examples in the memory rules were repaired. |
| V1.12.6 | 2026-05-31 | Standardized the `Selected Asset Packet` as a lightweight selected-object handoff between poster, deck, storyboard, edit, asset planning, prompt conversion, URL relay, generation tools, DOCX packaging, and Feishu publishing. The packet records object id, source stage, asset type, purpose, selected input, reference roles, locked items, avoid list, next tool, and privacy/cost gate so selected URLs, frames, references, and shots no longer travel as loose prose. |
| V1.12.5 | 2026-05-29 | Added the feedback standardization pass. Direction, storyboard group, and deck structure stages can now use a lightweight `Compare Board` with only `Keep`, `Remove`, and `Next version`; quick edit now covers S/M-level deck, storyboard, edit-plan, and prompt refinements in addition to poster/image edits; midstream feedback can become a `Change Delta Packet` before routing so local comments keep `Keep unchanged` and do not become accidental rebriefs. |
| V1.12.4 | 2026-05-27 | Added compact official prompt deltas for Seedance/Jimeng, Kling, Banana Pro/Gemini image, and OpenAI image, loaded only when a named tool or official-case prompt conversion needs them. Fixed the A1 review-feedback loop by requiring `review-producer` to output a `Review Delta Packet` for must-fix items and `change-manager` to consume it before rewriting, keeping revisions scoped and low-cost. |
| V1.12.3 | 2026-05-27 | Added storyboard reference angle frames. When the user asks Banana/image to assist a storyboard, SW can generate one selected still reference for a specific shot angle, scene geometry, subject scale, or lighting direction, then return to storyboard planning. This does not confirm every-shot generation, full storyboard-board generation, Seedance generation, or batch outputs. |
| V1.12.2 | 2026-05-27 | Improved Obsidian aesthetic browsing and storyboard board rules. Obsidian notes now embed local preview/contact-sheet images instead of showing only links, while still not copying heavy media. Integrated storyboard sheets now treat 15 seconds as the maximum group duration, allow slight shot-duration adjustments around segment boundaries, and treat 9 shots/3x3 as an upper limit rather than a target. |
| V1.12.1 | 2026-05-26 | Fixed Obsidian vault sync for real desktop usage: the sync script now detects the currently open Obsidian vault when no explicit path is provided and supports Windows cross-drive links, so a vault on another drive can link back to SW indexes without failing. |
| V1.12.0 | 2026-05-26 | Added a Markdown-only Obsidian Aesthetic Vault and sync script for browsing and curating SW aesthetic references without copying large images. Bootstrap now checks/syncs the vault, tool registry/help triggers document it, and normal SW runtime still reads only the compact aesthetic decision index. |
| V1.11.0 | 2026-05-26 | Added `feishu-docs` as an explicit Feishu/Lark Docs handoff tool for visual plans and storyboard packages. It renders Feishu-friendly Markdown locally, can dry-run publish plans, and can publish through Feishu Open Platform only after local private app credentials and explicit `--execute` are provided. Bootstrap, sync, and release checks now include Feishu readiness without printing secrets. |
| V1.10.5 | 2026-05-26 | Added portable install/bootstrap infrastructure: `INSTALL_SW.md` explains the one-command new-computer setup, and `tools/sw_bootstrap.py` detects the system, syncs user skills and the local plugin, runs SW doctor, checks Banana/Seedance keys, checks URL Relay config/health without printing secrets, and reports which features are ready versus needing local configuration. |
| V1.10.4 | 2026-05-26 | Poster image-native typography patch: poster hero titles, launch titles, large numerals, and stylized display lettering default to image/visual-model handling instead of system-font overlays. SW's poster role now emphasizes feedback judgment, precise edit instructions, and QA; editable/system text is reserved for exact information text, small copy, legal/logo/QR, or explicit editable-layer requests. |
| V1.10.3 | 2026-05-26 | Poster quick-edit performance patch: SW skill-chip invocation plus a clear existing-poster/image edit now goes straight to output-first editing without separate startup narration, runtime-file searching, or full project routing. Installed loader skills now carry a compact runtime pack and Studio skill pack so synced computers and other project folders do not have to rediscover the SW repository path for routine work. |
| V1.10.2 | 2026-05-25 | Poster quick-edit correction: existing-poster revisions now use a short output-first route instead of the full brief/direction pipeline, and poster display lettering such as hero titles, launch titles, big numerals, glow/metal/3D/neon type is treated as visual art rather than plain system-font text. Exact information text remains controlled and QA'd. |
| V1.10.1 | 2026-05-25 | Deep maintenance update: added UTF-8-safe text integrity scanning for real mojibake/private-use character leaks, blocked tracked aesthetic media files in release checks, validated all Studio/tool skills under UTF-8 mode, fixed Seedance prompt-only dry-run so text-to-video is not blocked by missing image URLs, and expanded the HQ aesthetic resource map plus future interactive-browser planning without increasing normal SW startup cost. |
| V1.10.0 | 2026-05-25 | Added the `aesthetic-director` studio role, compact `Aesthetic_Decision_Index.md` for automatic visual-taste selection, portable aesthetic-library storage config, library doctor, and top-tier collection queue. Normal projects use the tiny decision layer first; raw HQ images/contact sheets stay local-only and load only on explicit reference/moodboard/library-maintenance requests. |
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
