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

## Expected Replies

Startup:

```text
SW loaded successfully. Current version: V1.2.3
```

Version sync:

```text
SW version synchronized. Current version: V1.2.3
```

## Rule

Every future SW update must keep `SW_V1.0.md`, `sw_update.md`, and the optional `SW_Runtime_Index.md` aligned, because other project folders may only copy the entry pack instead of the whole studio template.

