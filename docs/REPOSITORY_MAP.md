# Repository Map

This map explains the main files and folders so reviewers can inspect the SW workspace without reading every rule file first.

## Entry Files

| Path | Role |
| --- | --- |
| `AGENTS.md` | Root Codex instruction file. Defines explicit SW activation, project memory, routing, cost control, and tool boundaries. |
| `SW_V1.0.md` | Stable SW invocation entry. The name stays stable even as runtime versions change. |
| `sw_update.md` | Version synchronization entry for active conversations. |
| `sw_rescue.md` | Stale conversation/chip recovery entry. |
| `sw_help.md` | Low-cost feature help entry. |
| `PULL_ARCHITECTURE.md` | Minimal instruction for pulling the current architecture in a new conversation. |

## Runtime And Routing

| Path | Role |
| --- | --- |
| `SW_Runtime_Index.md` | Compact runtime index used before deeper files are loaded. |
| `Cost_Governor.md` | Cost lanes, high-cost gates, and output-depth rules. |
| `Stage_Runbook.md` | Stage-by-stage workflow rules for brief, direction, storyboard, prompt, review, change, and archive. |
| `Studio_Skill_Dispatch_Protocol.md` | Current dispatch protocol for selecting role skills. |
| `Auto_Assignment_Rules.md` | Fallback routing rules when the fast path is not enough. |
| `Production_Pipeline_Map.md` | Larger multi-stage production chain map. |
| `Studio_Role_Label_Protocol.md` | Rules for visible role/cost traces after SW is explicitly enabled. |

## Studio Roles

| Path | Role |
| --- | --- |
| `Studio_Skills/brief-strategist/SKILL.md` | Requirement compression and missing-info judgment. |
| `Studio_Skills/creative-director/SKILL.md` | Creative direction generation and selection. |
| `Studio_Skills/storyboard-director/SKILL.md` | Shot sequence and Storyboard Animatic Sheet planning. |
| `Studio_Skills/prompt-director/SKILL.md` | Image/video prompt writing and tool prompt conversion. |
| `Studio_Skills/review-producer/SKILL.md` | Final review and Review Delta Packet generation. |
| `Studio_Skills/finishing-producer/SKILL.md` | Packaging, export, and delivery checks. |

The directory contains additional specialist roles for layout, deck, sound, edit, cinematography, historical checks, and tool integration.

## Prompt Rules

| Path | Role |
| --- | --- |
| `Prompts/Prompt_Spec_Rules.md` | Canonical prompt rules and the full storyboard-to-Seedance execution template. |
| `Prompts/Tool_Official_Prompt_Deltas.md` | Tool-specific prompt deltas loaded only when needed. |
| `Prompts/Video_Motion_Edit_Prompt_Rules.md` | Video motion/edit prompt contract and references. |
| `Prompts/Visual_Development_Board_Rules.md` | Visual board, reference board, and Storyboard Animatic Sheet rules. |

## Tool Skills

| Path | Role |
| --- | --- |
| `banana-pro/` | Banana Pro / OpenRouter image generation skill and scripts. |
| `seedance-2-video/` | Seedance 2.0 / Volcano Ark video generation skill and scripts. |
| `url-relay/` | Public URL relay for local media files. |
| `black-background-cutout/` | Local simple-background cutout tool. |
| `storyboard-visual-word/` | DOCX visual director handoff generation. |
| `feishu-docs/` | Feishu/Lark Docs render and publish workflow. |
| `kling-api/` | Kling API integration skill. |

## Maintenance

| Path | Role |
| --- | --- |
| `tools/sw_bootstrap.py` | Installs/syncs SW local skills and reports feature readiness. |
| `tools/sw_consistency_check.py` | Repository and install consistency checks. |
| `tools/sw_doctor.py` | Broader local health check. |
| `tools/sw_sync_installed.py` | Syncs repo-controlled skills/plugin to local Codex paths. |
| `.github/workflows/sw-ci.yml` | GitHub Actions consistency check. |

## Version And Release Records

| Path | Role |
| --- | --- |
| `VERSION.md` | Current runtime version, bump policy, and version log. |
| `Architecture_Update_Log.md` | Detailed architecture update history. |
| `Release_Rules.md` | Release and publication rules. |
| `INSTALL_SW.md` | New-machine install and configuration guide. |

## Local Or Generated Content

These paths may exist locally but should not be treated as core framework source:

| Path | Role |
| --- | --- |
| `outputs/` | Local generated previews and test outputs. Ignored by Git. |
| `banana_outputs/` | Banana test/generated outputs. Ignored by Git. |
| `seedance_outputs/` | Seedance generated outputs. Ignored by Git. |
| `.sw/` | Optional per-project memory in downstream projects, not required in this framework repo. |
