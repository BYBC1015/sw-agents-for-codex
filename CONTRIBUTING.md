# Contributing

This repository is a Codex skill/runtime framework, so changes should be small, traceable, and version-aware.

## Before Editing

- Keep SW explicit-only. Do not make ordinary design words start the full framework.
- Keep API keys and private local config out of the repository.
- Prefer updating the canonical source instead of copying the same rule into many files.
- If you change runtime behavior, routing, prompt contracts, tool integrations, or installed skill entry files, update the runtime version according to `VERSION.md`.

## Recommended Checks

```powershell
python .\tools\sw_consistency_check.py --scope repo
python .\tools\sw_doctor.py --scope all
```

Run install sync when a change affects user-level skills or plugin entries:

```powershell
python .\tools\sw_sync_installed.py
```

## Pull Request Checklist

- [ ] The change has a clear scope.
- [ ] No real API keys, tokens, private URLs, or private client files are included.
- [ ] Canonical prompt/routing files are not duplicated unnecessarily.
- [ ] Version files are updated when runtime behavior changes.
- [ ] Repository checks pass, or failures are explained.
