# Project Minimal Entry Pack

Use this when preparing another project folder for SW.

## Required Root Files

Copy these three files into the root of each project folder:

- `SW_V1.0.md`
- `sw_update.md`
- `sw_rescue.md`

These two files create the expected local entries:

- `@SW_V1.0` starts or loads the SW design studio workflow.
- `@sw_update` synchronizes the current conversation with the latest SW runtime version.
- `@sw_rescue` or `/sw-rescue` force-refreshes stale/sealed startup or update chips.

## Optional Root Files

Copy these when you want version history and troubleshooting available inside that folder:

- `SW_Runtime_Index.md`
- `Agent_Skill_Tech_Principles.md`
- `Studio_Role_Label_Protocol.md`
- `Production_Pipeline_Map.md`
- `01_Research/HQ_Aesthetic_References/Aesthetic_Decision_Index.md`
- `VERSION.md`
- `Architecture_Update_Log.md`
- `Legacy_Conversation_Recovery.md`
- `Feature_Trigger_Index.md`
- `sw_help.md`

## Expected Replies

Startup:

```text
SW loaded successfully. Current version: V1.10.5
```

Version sync:

```text
SW version synchronized. Current version: V1.10.5
```

Rescue:

```text
SW rescue synchronized. Current version: V1.10.5
```

## Optional Project Memory Pack

For long-running client/internal projects, add this folder inside that project root:

```text
.sw/
  PROJECT.md
  RULES.md
  MEMORY.md
  CHANGELOG.md
  ASSETS.md
```

Use `Project_Memory_Templates/.sw/` as the copy source.

SW will read only relevant local memory files. After major confirmations it may add one short suggestion, such as:

```text
记忆建议：可写入 MEMORY.md：品牌调性=克制电影感。回复“记住”即可。
```

SW must not write `MEMORY.md` unless the user explicitly says to remember/save it.

## Rule

Every future SW update must keep `SW_V1.0.md`, `sw_update.md`, `sw_rescue.md`, the optional `SW_Runtime_Index.md`, and the project memory template guidance aligned, because other project folders may only copy the entry pack instead of the whole studio template.

Default help and sync entries should use hot-start behavior: fixed short reply first, no shell/file reads for normal help, detailed files only when requested.

If a long-running project has its own visual references, keep them in `.sw/ASSETS.md` or a project-local reference folder and mention the rule in `.sw/RULES.md`. SW should use those project references before the global aesthetic library.

Installed SW entries created by `tools/sw_sync_installed.py` include a compact runtime pack beside the loader skill. This lets another project folder or a newly synced computer run quick poster/image edits without searching for the original repository path. If a user clicks the SW skill chip and asks for a clear existing-poster/image tweak, the chip itself is the load acknowledgement; SW should edit first and explain only the changed layer or QA risk.
