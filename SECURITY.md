# Security

## Secrets

Do not commit API keys, relay tokens, private environment files, generated payloads that contain credentials, client files, or private media.

The framework expects secrets to live in local user configuration paths or local environment variables, such as:

- `OPENROUTER_API_KEY`
- `ARK_API_KEY`
- local URL Relay token config
- local Feishu/Lark app credentials

Setup scripts may write private config outside the repository. They must not write real secrets into tracked files.

## Reporting Issues

If you find a leaked credential, unsafe upload behavior, or a rule that could expose private client material, open a private report if available. If private reporting is not available, open a minimal public issue without the secret value and rotate the affected credential immediately.

## Safe Defaults

- External generation and publishing tools are explicit-only.
- Missing keys should produce dry-run/payload behavior, not fake success.
- Temporary upload fallback must be confirmed or configured before use.
