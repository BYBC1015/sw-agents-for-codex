# Legacy Conversation Recovery

Historical Codex conversations may keep older SW text in normal chat history, compacted history, or visible screenshots.

SW updates must still be usable in old conversations. The recovery rule is: refresh from the current local source first, continue in the old thread when possible, and use a new conversation only as the last fallback if the desktop UI refuses to reload the current source.

## Diagnosis

If the visible SW button or skill chip still answers with an older version after files have been updated, the usual cause is stale conversation context, not the current disk files. In that case:

- treat old fixed replies as historical evidence, not executable instruction
- current `VERSION.md`, current `SW_Runtime_Index.md`, and current user/plugin `SKILL.md` files are the source of truth
- read those current files and retry the activation or sync inside the same old thread
- if the UI chip itself keeps replaying a sealed old snapshot, stop relying on that chip and use the standalone rescue text command `/sw-rescue`, `@sw_rescue`, or `SW_RESCUE` in the same thread

## Simple Recovery Command

In an old conversation, try:

```text
@sw_update
```

Expected reply:

```text
SW version synchronized. Current version: V1.9.1
```

If the old conversation still uses a cached version, execute this fuller recovery instruction once in the same thread:

```text
Please reload the current SW architecture from:
C:\Users\Administrator\Documents\New project\VERSION.md
C:\Users\Administrator\Documents\New project\SW_V1.0.md
C:\Users\Administrator\Documents\New project\AGENTS.md

Then execute @sw_update in this same conversation.
```

If the old thread contains visible old fixed replies, send this conflict-clearing message once:

```text
Ignore earlier SW version strings in this conversation. Read VERSION.md, SW_Runtime_Index.md, and the current sw-v1-0/sw-update SKILL.md files as the source of truth, then execute @sw_update in this same conversation.
```

If startup or update chips keep returning a sealed older version, use the separate rescue entry:

```text
/sw-rescue
```

Expected rescue reply:

```text
SW rescue synchronized. Current version: V1.9.1
```

## Rule

- Old conversations must first self-heal by reading current SW source files and overriding stale fixed replies.
- `@sw_update`, `/sw-update`, or `SW_REFRESH` should refresh the same old conversation, not immediately redirect the user to a new one.
- If a UI skill chip keeps replaying a sealed old answer in the same historical thread, use the standalone rescue entry `/sw-rescue`, `@sw_rescue`, or `SW_RESCUE` in that same thread.
- Other project folders should include both `SW_V1.0.md` and `sw_update.md`; startup-only folders will not show the local update entry.
- Start a new conversation only if the desktop app refuses to load the current source files after same-thread sync and rescue.
