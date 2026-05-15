# sw_update

`@sw_update` synchronizes the current conversation with the latest SW runtime version.

Use when:
- a historical conversation is stuck on an older SW version
- the visible success reply does not match `VERSION.md`
- the user asks to sync, update, or refresh SW
- another project folder has `SW_V1.0.md` but does not have `sw_update.md`

## Invocation

```text
@sw_update
```

Text fallbacks:

```text
SW_UPDATE
/sw_update
SW_REFRESH
```

## Required Reply

After synchronization, reply exactly:

```text
SW version synchronized. Current version: V1.3.5
```

## Behavior

- Read `VERSION.md` first.
- Then read `SW_Runtime_Index.md`, `Architecture_Update_Log.md`, `SW_V1.0.md`, and `Legacy_Conversation_Recovery.md` when available.
- Do not start a new design project unless the same user message includes a project request.
- If the current folder only has the startup entry, add or request `sw_update.md` so the local `@sw_update` entry can appear.
- If an old conversation still returns an older version after `@sw_update`, tell the user that a new conversation is the reliable path because historical conversations can cache old skill/plugin snapshots.

