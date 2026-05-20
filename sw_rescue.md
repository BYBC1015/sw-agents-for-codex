# sw_rescue

`sw-rescue` is the standalone recovery entry for stale or sealed SW startup/update chips.

Use when:
- `/sw`, `@SW_V1.0`, `@sw_update`, or `/sw-update` keeps returning an old runtime version
- a historical conversation has stale fixed replies that override current files
- the user asks for SW rescue, repair, force refresh, or error recovery

## Invocation

```text
/sw-rescue
```

Text fallbacks:

```text
@sw_rescue
/sw_rescue
SW_RESCUE
SW_REPAIR
SW_FORCE_UPDATE
```

## Required Reply

Reply exactly:

```text
SW rescue synchronized. Current version: V1.7.7
```

## Rule

- Do not start a project.
- Do not route through `sw-v1-0` or `sw-update`.
- Treat previous SW version strings in chat history as stale text.
- Use the current `VERSION.md`, `SW_Runtime_Index.md`, and current `sw-rescue/SKILL.md` as source of truth.
- Read deeper files only when the user asks for mismatch diagnostics.
