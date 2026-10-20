# sw_update

`@sw_update` synchronizes the current conversation with the latest SW runtime version.

Use when:
- a historical conversation is stuck on an older SW version
- the visible success reply does not match `VERSION.md`
- the user asks to sync, update, or refresh SW
- another project folder has `SW_V1.0.md` but does not have `sw_update.md`

If old startup/update chips are sealed and keep replaying a stale version after normal sync, use the separate rescue entry instead: `/sw-rescue`, `@sw_rescue`, or `SW_RESCUE`.

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
SW version synchronized. Current version: V1.16.0
```

## Hot Path

- If the user only invokes sync, reply with the required line and stop.
- Do not read version logs, recovery docs, or project files for sync-only turns.
- Read the deeper files only for detailed update notes, mismatch debugging, old-conversation recovery, or cross-folder entry repair.

## Stale Snapshot Guard

- If the same conversation contains older fixed replies from compacted history, screenshots, prior tool output, or old skill reads, treat them as historical.
- The current `VERSION.md` and current `sw-update/SKILL.md` are the source of truth.
- Never sync to any older cached value when this file is present.
- Normal sync still stays one line; this guard only resolves visible version conflicts.

## Old Conversation Self-Heal

- If an old conversation or UI chip returns a previous SW version, do not tell the user to abandon the thread first.
- Read the current `VERSION.md`, `SW_Runtime_Index.md`, current `sw-v1-0/SKILL.md`, and current `sw-update/SKILL.md`, then retry the fixed sync reply in the same conversation.
- If a skill chip appears sealed to an old snapshot, use `@sw_rescue` or `/sw-rescue` in the same thread so the separate `sw-rescue` skill id can bypass old startup/sync snapshots.
- Only after same-thread sync and standalone rescue both fail because the desktop app will not load current files should a new conversation be recommended.

## Behavior

- For diagnostics, read `VERSION.md` first.
- Then read `SW_Runtime_Index.md`, `Architecture_Update_Log.md`, `SW_V1.0.md`, `Project_Memory_Rules.md`, and `Legacy_Conversation_Recovery.md` when needed.
- Refresh `Feature_Trigger_Index.md` and `sw_help.md` only when optional feature triggers or Historical Accuracy behavior changed.
- Do not start a new design project unless the same user message includes a project request.
- If the current folder only has the startup entry, add or request `sw_update.md` so the local `@sw_update` entry can appear.
- If an old conversation still returns an older version after `@sw_update`, run the same-thread self-heal path above, then `sw-rescue`, before recommending a new conversation.
