# INSTALL_SW

This file is the portable installation guide for SW. Use it after cloning the repository on a new computer, or when Codex needs to repair a local SW install without reading the whole project.

## Fast Install

From the cloned repository root:

```powershell
python .\tools\sw_bootstrap.py
```

If Windows uses the Python launcher instead:

```powershell
py -3 .\tools\sw_bootstrap.py
```

The bootstrap script will:

- detect the current OS, Python, repository path, and Codex user folders
- synchronize SW skills into `~/.codex/skills`
- synchronize the local plugin into `~/plugins/sw-v1-0`
- run the SW doctor and consistency checks
- check whether Banana Pro, Seedance 2.0, URL Relay, Storyboard Visual Word, Feishu Docs, the aesthetic index, and the Obsidian aesthetic vault are usable
- check whether local private keys/configs are present without printing secrets
- report what is ready and what still needs local configuration

## Codex Instruction

If using Codex instead of running the command manually, give Codex this instruction:

```text
Please read INSTALL_SW.md and run the SW bootstrap check. Do not read the full project unless bootstrap reports an issue. Summarize which SW features are ready and which need local configuration.
```

## What Gets Installed

The installer copies repository-controlled skills and plugin entries to local Codex paths:

| Target | Purpose |
| --- | --- |
| `~/.codex/skills/sw-v1-0` | SW runtime loader and compact runtime pack |
| `~/.codex/skills/sw-update` | Version synchronization entry |
| `~/.codex/skills/sw-rescue` | Stale chat/chip rescue entry |
| `~/.codex/skills/sw-help` | Low-cost feature help entry |
| `~/.codex/skills/banana-pro` | Banana Pro / OpenRouter image generation tool |
| `~/.codex/skills/seedance-2-video` | Seedance 2.0 / 即梦2.0 video generation tool |
| `~/.codex/skills/url-relay` | Public URL relay for local media files |
| `~/.codex/skills/black-background-cutout` | Local black/simple solid-background cutout tool |
| `~/.codex/skills/feishu-docs` | Feishu/Lark Docs visual handoff tool |
| `~/.codex/skills/storyboard-visual-word` | DOCX visual方案 handoff tool |
| `~/plugins/sw-v1-0` | Slash/chip plugin entry pack |

The script does not write API keys into the repository.

## Private Configuration

Some tools install successfully but remain in dry-run or payload-only mode until local private credentials are configured.

### Banana Pro

Required for real image generation:

```text
OPENROUTER_API_KEY
```

Recommended private file:

```text
~/.config/banana-pro/openrouter.env
```

File content:

```text
OPENROUTER_API_KEY=<your OpenRouter key>
```

### Seedance 2.0 / 即梦2.0

Required for real video generation:

```text
ARK_API_KEY
```

Recommended setup command:

```powershell
python .\seedance-2-video\scripts\seedance_task.py setup-key
```

This stores the key in a local private file outside the shareable skill files.

### URL Relay

Required when a downstream AI tool needs a public URL but the source image/video is a local file.

Recommended setup command:

```powershell
python .\url-relay\scripts\url_relay.py setup --upload-url http://123.56.255.86/upload --public-base http://123.56.255.86/u --temporary-relay-fallback none
```

When prompted, paste the SW media uploader token. The token is an upload credential for the relay server, not a model token, and must remain local/private.

### Feishu Docs

Local render and publish dry-run work without credentials. Real Feishu/Lark publishing needs a local private app config:

```powershell
python .\feishu-docs\scripts\feishu_doc_cli.py setup --app-id <your app id> --folder-token <optional folder token>
```

The app secret is stored only in `~/.config/sw-feishu/config.json` or read from local environment variables.

### Obsidian Aesthetic Vault

The Obsidian layer is local and Markdown-only. It does not need API keys and does not copy heavy images.

Sync or rebuild it with:

```powershell
python .\tools\sync_obsidian_aesthetic_vault.py
```

Then open this folder as a vault in Obsidian:

```text
Obsidian_Aesthetic_Vault
```

If you keep the vault on another drive, open that vault in Obsidian before running the sync script, set `SW_OBSIDIAN_AESTHETIC_VAULT`, or pass `--vault <path>` explicitly.

## Bootstrap Options

```powershell
python .\tools\sw_bootstrap.py --json
python .\tools\sw_bootstrap.py --no-sync
python .\tools\sw_bootstrap.py --skip-doctor
python .\tools\sw_bootstrap.py --no-network
```

Use `--json` when another script or Codex workflow needs a machine-readable report. Use `--no-network` if the computer is offline or URL Relay health checks should be skipped.

## Expected Result

The final report should look like:

```text
SW bootstrap complete. Current version: Vx.x.x
Available features:
- [ready] SW core workflow (/sw, @SW_V1.0)
- [ready] SW update/help/rescue entries
- [ready or needs_config] Banana Pro
- [ready or needs_config] Seedance 2.0
- [ready or needs_config] URL Relay
- [ready] Storyboard Visual Word
- [ready or needs_config] Feishu Docs
- [ready] Obsidian Aesthetic Vault
```

`needs_config` is normal on a new computer until local keys and relay token are added.

## Token Cost

Daily SW use does not consume extra model tokens because of this installer. The script runs locally. It reduces future token use by avoiding repeated manual checks of paths, versions, plugin files, keys, and URL Relay state.

## Troubleshooting

If SW chips show stale versions:

```powershell
python .\tools\sw_bootstrap.py
```

Then in Codex use:

```text
/sw-rescue
```

If the bootstrap report says URL Relay needs configuration, configure the relay token first. Missing token or missing upload URL should not fall back to Catbox/Litterbox automatically.

If real image/video generation is unavailable, check `OPENROUTER_API_KEY` for Banana Pro and `ARK_API_KEY` for Seedance. The tools can still generate dry-run payloads without keys.
