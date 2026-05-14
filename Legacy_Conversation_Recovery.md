# Legacy Conversation Recovery

Historical Codex conversations may keep the SW skill/plugin snapshot that was loaded when that conversation started.

New SW updates are guaranteed for new conversations. Old conversations may not hot-reload automatically.

## Simple Recovery Command

In an old conversation, try:

```text
@sw_update
```

Expected reply:

```text
SW version synchronized. Current version: V1.2.2
```

If the old conversation still uses a cached version, send this fuller recovery message once:

```text
Please reload the current SW architecture from:
C:\Users\Administrator\Documents\New project\VERSION.md
C:\Users\Administrator\Documents\New project\SW_V1.0.md
C:\Users\Administrator\Documents\New project\AGENTS.md

Then execute @sw_update.
```

## Rule

- New conversations are the reliable activation path after every SW update.
- Old conversations may require `@sw_update` or the `SW_REFRESH` fallback.
- Other project folders should include both `SW_V1.0.md` and `sw_update.md`; startup-only folders will not show the local update entry.
- If an old conversation still answers with a previous version after `@sw_update`, start a new conversation to guarantee the latest SW runtime.

