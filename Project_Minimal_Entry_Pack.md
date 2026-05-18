# Project Minimal Entry Pack

Use this when preparing another project folder for SW.

## Required Root Files

Copy these two files into the root of each project folder:

- `SW_V1.0.md`
- `sw_update.md`

These two files create the expected local entries:

- `@SW_V1.0` starts or loads the SW design studio workflow.
- `@sw_update` synchronizes the current conversation with the latest SW runtime version.

## Optional Root Files

Copy these when you want version history and troubleshooting available inside that folder:

- `SW_Runtime_Index.md`
- `Agent_Skill_Tech_Principles.md`
- `Studio_Role_Label_Protocol.md`
- `Production_Pipeline_Map.md`
- `VERSION.md`
- `Architecture_Update_Log.md`
- `Legacy_Conversation_Recovery.md`
- `Feature_Trigger_Index.md`
- `sw_help.md`

## Expected Replies

Startup:

```text
SW loaded successfully. Current version: V1.6.0
```

Version sync:

```text
SW version synchronized. Current version: V1.6.0
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

Every future SW update must keep `SW_V1.0.md`, `sw_update.md`, the optional `SW_Runtime_Index.md`, and the project memory template guidance aligned, because other project folders may only copy the entry pack instead of the whole studio template.

Default help and sync entries should use hot-start behavior: fixed short reply first, no shell/file reads for normal help, detailed files only when requested.
