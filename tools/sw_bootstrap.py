#!/usr/bin/env python3
"""Bootstrap SW on a freshly cloned computer.

The script is dependency-free and intentionally conservative:
- sync user-level skills and the local plugin from this repository
- run the existing lightweight SW doctor
- check private key/config presence without printing secrets
- summarize which SW features are ready and which need local setup
"""

from __future__ import annotations

import argparse
import json
import os
import platform
import re
import shutil
import subprocess
import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
USERPROFILE = Path(os.environ.get("USERPROFILE", str(Path.home())))

USER_SKILLS = USERPROFILE / ".codex" / "skills"
PLUGIN_ROOT = USERPROFILE / "plugins" / "sw-v1-0"

BANANA_ENV_FILE = Path.home() / ".config" / "banana-pro" / "openrouter.env"
SEEDANCE_KEY_FILE = Path.home() / ".config" / "codex-seedance-2-video" / "secrets.json"
RELAY_CONFIG_FILE = Path.home() / ".config" / "sw-media-uploader" / "config.json"
FEISHU_CONFIG_FILE = Path.home() / ".config" / "sw-feishu" / "config.json"
DREAMINA_CONFIG_DIR = Path.home() / ".dreamina_cli"
DREAMINA_DEFAULT_EXE = USERPROFILE / "bin" / "dreamina.exe"
KLING_CREDENTIALS_FILE = Path.home() / ".kling" / ".credentials"

SW_UPLOAD_URL = "http://123.56.255.86/upload"
SW_PUBLIC_BASE = "http://123.56.255.86/u"

READY = "ready"
NEEDS_CONFIG = "needs_config"
WARNING = "warning"
FAILED = "failed"
SKIPPED = "skipped"


def configure_stdio() -> None:
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8")
        except Exception:
            pass


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8-sig")


def read_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    return json.loads(read_text(path))


def active_obsidian_vault() -> Path | None:
    config_candidates = []
    for base_name in ("APPDATA", "LOCALAPPDATA"):
        base = os.environ.get(base_name)
        if not base:
            continue
        config_candidates.extend(
            [
                Path(base) / "obsidian" / "obsidian.json",
                Path(base) / "Obsidian" / "obsidian.json",
            ]
        )
    for config_path in config_candidates:
        if not config_path.exists():
            continue
        try:
            data = read_json(config_path)
        except (OSError, json.JSONDecodeError):
            continue
        vaults = data.get("vaults") or {}
        candidates = []
        for item in vaults.values():
            path = item.get("path")
            if not path:
                continue
            candidates.append((bool(item.get("open")), int(item.get("ts") or 0), Path(path)))
        if candidates:
            candidates.sort(key=lambda item: (item[0], item[1]), reverse=True)
            return candidates[0][2]
    return None


def obsidian_vault_path() -> Path:
    return Path(os.environ.get("SW_OBSIDIAN_AESTHETIC_VAULT") or active_obsidian_vault() or ROOT / "Obsidian_Aesthetic_Vault").expanduser()


def parse_version() -> str:
    version_file = ROOT / "VERSION.md"
    if not version_file.exists():
        return "unknown"
    match = re.search(r"Current runtime version:\s*(V\d+\.\d+\.\d+)", read_text(version_file))
    return match.group(1) if match else "unknown"


def secret_state(value: str | None) -> str:
    value = (value or "").strip()
    return "missing" if not value else f"present:{len(value)}chars"


def env_file_value(path: Path, key_name: str) -> str | None:
    if not path.exists():
        return None
    for raw_line in read_text(path).splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        if key.strip() == key_name:
            cleaned = value.strip().strip('"').strip("'")
            if cleaned:
                return cleaned
    return None


def windows_user_env_value(key_name: str) -> str | None:
    if os.name != "nt":
        return None
    try:
        import winreg  # type: ignore

        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, "Environment") as env_key:
            value, _ = winreg.QueryValueEx(env_key, key_name)
        if isinstance(value, str) and value.strip():
            return value.strip()
    except OSError:
        return None
    return None


def seedance_key_value() -> str | None:
    env_value = os.environ.get("ARK_API_KEY", "").strip()
    if env_value:
        return env_value
    data = read_json(SEEDANCE_KEY_FILE)
    for key in ("ark_api_key", "ARK_API_KEY"):
        value = str(data.get(key) or "").strip()
        if value:
            return value
    return None


def relay_config() -> tuple[dict[str, Any], Path]:
    path = Path(os.environ.get("SW_RELAY_CONFIG") or RELAY_CONFIG_FILE).expanduser()
    data = read_json(path)
    upload_url = (os.environ.get("SW_RELAY_UPLOAD_URL") or data.get("upload_url") or "").strip()
    public_base = (os.environ.get("SW_RELAY_PUBLIC_BASE") or data.get("public_base") or "").strip()
    token = (os.environ.get("SW_RELAY_TOKEN") or data.get("token") or "").strip()
    temporary = (
        os.environ.get("SW_RELAY_TEMPORARY_FALLBACK")
        or data.get("temporary_fallback")
        or data.get("temporary_relay_fallback")
        or "none"
    )
    return {
        "upload_url": upload_url,
        "public_base": public_base,
        "token": token,
        "temporary_fallback": str(temporary).strip() or "none",
        "max_bytes": data.get("max_bytes"),
        "managed_by": data.get("managed_by"),
    }, path


def command_result(command: list[str], timeout: int) -> dict[str, Any]:
    env = os.environ.copy()
    env.setdefault("PYTHONUTF8", "1")
    try:
        completed = subprocess.run(
            command,
            cwd=ROOT,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=timeout,
            env=env,
        )
        return {
            "command": command,
            "ok": completed.returncode == 0,
            "returncode": completed.returncode,
            "stdout_tail": tail(completed.stdout),
            "stderr_tail": tail(completed.stderr),
        }
    except FileNotFoundError as exc:
        return {"command": command, "ok": False, "returncode": None, "error": str(exc)}
    except subprocess.TimeoutExpired as exc:
        return {
            "command": command,
            "ok": False,
            "returncode": None,
            "error": f"timed out after {timeout}s",
            "stdout_tail": tail(exc.stdout or ""),
            "stderr_tail": tail(exc.stderr or ""),
        }


def tail(value: str, limit: int = 12) -> str:
    lines = [line.rstrip() for line in str(value or "").splitlines() if line.strip()]
    return "\n".join(lines[-limit:])


def detect_system() -> dict[str, Any]:
    return {
        "os": platform.system(),
        "release": platform.release(),
        "machine": platform.machine(),
        "python": sys.version.split()[0],
        "executable": sys.executable,
        "repo_root": str(ROOT),
        "user_profile": str(USERPROFILE),
    }


def path_exists(path: Path) -> bool:
    return path.exists()


def installed_paths() -> dict[str, bool]:
    checks = {
        "user_sw": USER_SKILLS / "sw-v1-0" / "SKILL.md",
        "user_update": USER_SKILLS / "sw-update" / "SKILL.md",
        "user_help": USER_SKILLS / "sw-help" / "SKILL.md",
        "user_rescue": USER_SKILLS / "sw-rescue" / "SKILL.md",
        "user_banana": USER_SKILLS / "banana-pro" / "SKILL.md",
        "user_dreamina": USER_SKILLS / "dreamina-cli" / "SKILL.md",
        "user_kling": USER_SKILLS / "kling-cli" / "SKILL.md",
        "user_seedance": USER_SKILLS / "seedance-2-video" / "SKILL.md",
        "user_url_relay": USER_SKILLS / "url-relay" / "SKILL.md",
        "user_black_background_cutout": USER_SKILLS / "black-background-cutout" / "SKILL.md",
        "user_storyboard_visual_word": USER_SKILLS / "storyboard-visual-word" / "SKILL.md",
        "user_feishu_docs": USER_SKILLS / "feishu-docs" / "SKILL.md",
        "plugin_manifest": PLUGIN_ROOT / ".codex-plugin" / "plugin.json",
        "plugin_sw_command": PLUGIN_ROOT / "commands" / "sw.md",
        "plugin_update_command": PLUGIN_ROOT / "commands" / "sw-update.md",
    }
    return {name: path_exists(path) for name, path in checks.items()}


def check_banana() -> dict[str, Any]:
    env_key = os.environ.get("OPENROUTER_API_KEY", "").strip()
    file_key = env_file_value(BANANA_ENV_FILE, "OPENROUTER_API_KEY")
    registry_key = windows_user_env_value("OPENROUTER_API_KEY")
    source = None
    value = None
    for candidate_source, candidate_value in [
        (str(BANANA_ENV_FILE), file_key),
        ("env:OPENROUTER_API_KEY", env_key),
        ("windows_user_env:OPENROUTER_API_KEY", registry_key),
    ]:
        if candidate_value:
            source = candidate_source
            value = candidate_value
            break
    return {
        "name": "Banana Pro image generation",
        "status": READY if value else NEEDS_CONFIG,
        "key_state": secret_state(value),
        "key_source": source,
        "config_path": str(BANANA_ENV_FILE),
        "setup_hint": "Run: python banana-pro/scripts/generate_openrouter_image.py --setup-key",
    }


def check_seedance() -> dict[str, Any]:
    key = seedance_key_value()
    source = "env:ARK_API_KEY" if os.environ.get("ARK_API_KEY", "").strip() else None
    if key and not source:
        source = str(SEEDANCE_KEY_FILE)
    return {
        "name": "Seedance 2.0 video generation",
        "status": READY if key else NEEDS_CONFIG,
        "key_state": secret_state(key),
        "key_source": source,
        "config_path": str(SEEDANCE_KEY_FILE),
        "setup_hint": "Run: python seedance-2-video/scripts/seedance_task.py setup-key",
    }


def check_dreamina() -> dict[str, Any]:
    command = shutil.which("dreamina")
    if not command and DREAMINA_DEFAULT_EXE.exists():
        command = str(DREAMINA_DEFAULT_EXE)
    return {
        "name": "Dreamina/Jimeng official CLI",
        "status": READY if command else NEEDS_CONFIG,
        "command": command,
        "session_state": "unchecked",
        "config_path": str(DREAMINA_CONFIG_DIR),
        "setup_hint": (
            "Only after confirmation: run the official installer from "
            "https://jimeng.jianying.com/cli, then run dreamina login."
        ),
        "detail": "Bootstrap checks only whether the local dreamina command exists; it does not install, login, or generate.",
    }


def check_kling() -> dict[str, Any]:
    command = shutil.which("kling") or shutil.which("kling.cmd")
    credentials_present = KLING_CREDENTIALS_FILE.exists()
    status = READY if command and credentials_present else NEEDS_CONFIG
    return {
        "name": "Kling official CLI / MCP",
        "status": status,
        "command": command,
        "credentials_state": "present" if credentials_present else "missing",
        "credentials_path": str(KLING_CREDENTIALS_FILE),
        "setup_hint": "Install the region-matched @klingai CLI package, then run kling login.",
        "detail": "Bootstrap checks only whether the kling command and OAuth credentials file exist; it does not read credentials or generate.",
    }


def check_feishu() -> dict[str, Any]:
    data = read_json(FEISHU_CONFIG_FILE)
    app_id = os.environ.get("FEISHU_APP_ID") or str(data.get("app_id") or "")
    app_secret = os.environ.get("FEISHU_APP_SECRET") or str(data.get("app_secret") or "")
    folder_token = os.environ.get("FEISHU_FOLDER_TOKEN") or str(data.get("folder_token") or "")
    base_url = os.environ.get("FEISHU_BASE_URL") or str(data.get("base_url") or "https://open.feishu.cn/open-apis")
    has_core_config = bool(app_id and app_secret)
    return {
        "name": "Feishu Docs handoff",
        "status": READY if has_core_config else NEEDS_CONFIG,
        "app_id_state": secret_state(app_id),
        "app_secret_state": secret_state(app_secret),
        "folder_token_state": secret_state(folder_token),
        "base_url": base_url,
        "config_path": str(FEISHU_CONFIG_FILE),
        "setup_hint": "Run: python feishu-docs/scripts/feishu_doc_cli.py setup --app-id <app_id> --folder-token <folder_token>",
    }


def check_obsidian_vault() -> dict[str, Any]:
    vault = obsidian_vault_path()
    home = vault / "Home.md"
    router = vault / "00_Index" / "Profile Router.md"
    config = vault / "obsidian-vault-config.json"
    ready = home.exists() and router.exists() and config.exists()
    return {
        "name": "Obsidian Aesthetic Vault",
        "status": READY if ready else NEEDS_CONFIG,
        "vault": str(vault),
        "home": str(home),
        "setup_hint": "Run: python tools/sync_obsidian_aesthetic_vault.py",
        "detail": "Markdown-only aesthetic browsing vault; no API key required and no heavy images are copied.",
    }


def health_url_from_upload(upload_url: str) -> str | None:
    if not upload_url:
        return None
    parsed = urllib.parse.urlparse(upload_url)
    if not parsed.scheme or not parsed.netloc:
        return None
    return urllib.parse.urlunparse((parsed.scheme, parsed.netloc, "/health", "", "", ""))


def probe_url(url: str, timeout: int) -> dict[str, Any]:
    req = urllib.request.Request(url, headers={"Accept": "application/json"}, method="GET")
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            body = resp.read(300).decode("utf-8", errors="replace")
            return {"ok": True, "status": getattr(resp, "status", 200), "url": url, "body": body}
    except urllib.error.HTTPError as exc:
        return {"ok": False, "status": exc.code, "url": url, "error": exc.reason}
    except urllib.error.URLError as exc:
        return {"ok": False, "status": None, "url": url, "error": str(exc.reason)}
    except OSError as exc:
        return {"ok": False, "status": None, "url": url, "error": str(exc)}


def check_url_relay(no_network: bool, timeout: int) -> dict[str, Any]:
    cfg, path = relay_config()
    has_core_config = bool(cfg["upload_url"] and cfg["public_base"] and cfg["token"])
    report: dict[str, Any] = {
        "name": "SW URL Relay",
        "status": READY if has_core_config else NEEDS_CONFIG,
        "config_file": str(path),
        "upload_url": cfg["upload_url"] or None,
        "public_base": cfg["public_base"] or None,
        "token_state": secret_state(cfg["token"]),
        "temporary_fallback": cfg["temporary_fallback"],
        "setup_hint": (
            "Run: python url-relay/scripts/url_relay.py setup "
            f"--upload-url {SW_UPLOAD_URL} --public-base {SW_PUBLIC_BASE} "
            "--temporary-relay-fallback none"
        ),
    }
    if not has_core_config:
        report["note"] = "URL Relay can still use existing public URLs, but local file upload needs this config."
        return report
    if no_network:
        report["network"] = {"status": SKIPPED, "reason": "--no-network"}
        return report
    health_url = health_url_from_upload(cfg["upload_url"])
    if not health_url:
        report["network"] = {"status": WARNING, "reason": "could not infer health URL"}
        return report
    probe = probe_url(health_url, timeout)
    report["network"] = probe
    if not probe["ok"]:
        report["status"] = WARNING
        report["note"] = "Config exists, but the relay health check did not pass. Upload may still need repair."
    return report


def feature_status(
    installed: dict[str, bool],
    keys: dict[str, Any],
    relay: dict[str, Any],
    obsidian: dict[str, Any],
) -> list[dict[str, Any]]:
    return [
        {
            "name": "SW core workflow (/sw, @SW_V1.0)",
            "status": READY if installed["user_sw"] and installed["plugin_manifest"] else FAILED,
            "detail": "Core loader and local plugin manifest are installed.",
        },
        {
            "name": "SW update/help/rescue entries",
            "status": READY if installed["user_update"] and installed["user_help"] and installed["user_rescue"] else FAILED,
            "detail": "Version sync, help, and stale-chat rescue entries are installed.",
        },
        {
            "name": "Banana Pro",
            "status": keys["banana"]["status"] if installed["user_banana"] else FAILED,
            "detail": "Image generation is ready when the private Banana env file or OPENROUTER_API_KEY is configured; otherwise dry-run/payload only.",
        },
        {
            "name": "Dreamina CLI",
            "status": keys["dreamina"]["status"] if installed["user_dreamina"] else FAILED,
            "detail": "Official Jimeng/Dreamina CLI route is available when the dreamina command is installed; login/generation are confirmed at use time.",
        },
        {
            "name": "Kling CLI / MCP",
            "status": keys["kling"]["status"] if installed["user_kling"] else FAILED,
            "detail": "Official Kling CLI route is available when the kling command is installed and OAuth credentials exist; generation is confirmed at use time.",
        },
        {
            "name": "Seedance 2.0",
            "status": keys["seedance"]["status"] if installed["user_seedance"] else FAILED,
            "detail": "Video generation is ready when ARK_API_KEY is configured; otherwise dry-run/payload only.",
        },
        {
            "name": "URL Relay",
            "status": relay["status"] if installed["user_url_relay"] else FAILED,
            "detail": "Local media can become public URLs when SW media uploader config and token are present.",
        },
        {
            "name": "Black Background Cutout",
            "status": READY if installed["user_black_background_cutout"] else FAILED,
            "detail": "Local black/simple solid-background cutout tool is installed; no API key or upload required.",
        },
        {
            "name": "Storyboard Visual Word",
            "status": READY if installed["user_storyboard_visual_word"] else FAILED,
            "detail": "DOCX visual方案 handoff tool is installed; no API key required.",
        },
        {
            "name": "Feishu Docs",
            "status": keys["feishu"]["status"] if installed["user_feishu_docs"] else FAILED,
            "detail": "Feishu visual-plan/storyboard handoff is installed; real publishing needs local Feishu app credentials.",
        },
        {
            "name": "Aesthetic decision index",
            "status": READY if (ROOT / "01_Research" / "HQ_Aesthetic_References" / "Aesthetic_Decision_Index.md").exists() else WARNING,
            "detail": "Compact aesthetic routing index is present.",
        },
        {
            "name": "Obsidian Aesthetic Vault",
            "status": obsidian["status"],
            "detail": obsidian["detail"],
        },
    ]


def collect_needs(features: list[dict[str, Any]], key_reports: dict[str, Any], relay: dict[str, Any]) -> list[str]:
    needs: list[str] = []
    for feature in features:
        if feature["status"] in {NEEDS_CONFIG, FAILED, WARNING}:
            needs.append(f"{feature['name']}: {feature['status']}")
    if key_reports["banana"]["status"] == NEEDS_CONFIG:
        needs.append("Banana Pro key: set ~/.config/banana-pro/openrouter.env or OPENROUTER_API_KEY.")
    if key_reports["dreamina"]["status"] == NEEDS_CONFIG:
        needs.append("Dreamina CLI: install the local dreamina command and login only after explicit confirmation.")
    if key_reports["kling"]["status"] == NEEDS_CONFIG:
        needs.append("Kling CLI: install the region-matched kling command and run kling login only after explicit confirmation.")
    if key_reports["seedance"]["status"] == NEEDS_CONFIG:
        needs.append("Seedance key: run seedance_task.py setup-key or set ARK_API_KEY locally.")
    if relay["status"] == NEEDS_CONFIG:
        needs.append("URL Relay: configure upload URL, public base, and upload token in ~/.config/sw-media-uploader/config.json.")
    elif relay["status"] == WARNING:
        needs.append("URL Relay: config exists, but network/health check needs attention.")
    if key_reports["feishu"]["status"] == NEEDS_CONFIG:
        needs.append("Feishu Docs: configure FEISHU_APP_ID/FEISHU_APP_SECRET locally, or use render/dry-run only.")
    return needs


def print_human(report: dict[str, Any]) -> None:
    print(f"SW bootstrap complete. Current version: {report['version']}")
    print(f"System: {report['system']['os']} {report['system']['release']} / Python {report['system']['python']}")
    print(f"Repository: {report['system']['repo_root']}")
    print()
    print("Available features:")
    for feature in report["features"]:
        print(f"- [{feature['status']}] {feature['name']} - {feature['detail']}")
    print()
    if report["needs_config"]:
        print("Needs local configuration:")
        for item in report["needs_config"]:
            print(f"- {item}")
    else:
        print("Needs local configuration: none.")
    print()
    print("Private config state:")
    print(f"- Banana Pro key: {report['keys']['banana']['key_state']}")
    print(f"- Dreamina CLI: {'installed' if report['keys']['dreamina']['command'] else 'missing'}")
    print(f"- Kling CLI: {'installed' if report['keys']['kling']['command'] else 'missing'}, credentials {report['keys']['kling']['credentials_state']}")
    print(f"- Seedance key: {report['keys']['seedance']['key_state']}")
    print(f"- URL Relay token: {report['url_relay']['token_state']}")
    print(f"- Feishu app secret: {report['keys']['feishu']['app_secret_state']}")
    if report.get("sync") and report["sync"]["status"] != SKIPPED:
        print(f"- Sync: {report['sync']['status']}")
    if report.get("doctor") and report["doctor"]["status"] != SKIPPED:
        print(f"- Doctor: {report['doctor']['status']}")
    if report.get("obsidian_sync") and report["obsidian_sync"]["status"] != SKIPPED:
        print(f"- Obsidian vault sync: {report['obsidian_sync']['status']}")
    if report.get("obsidian"):
        print(f"- Obsidian vault: {report['obsidian']['vault']}")
    print()
    print("No secrets were printed or written to the repository.")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Install and diagnose SW on this computer.")
    parser.add_argument("--no-sync", action="store_true", help="Only inspect; do not synchronize user/plugin entries.")
    parser.add_argument("--skip-doctor", action="store_true", help="Skip sw_doctor.py after sync.")
    parser.add_argument("--no-network", action="store_true", help="Skip URL Relay health network probe.")
    parser.add_argument("--json", action="store_true", help="Print machine-readable JSON only.")
    parser.add_argument("--timeout", type=int, default=10, help="Timeout seconds for local commands and relay health probe.")
    return parser.parse_args()


def main() -> int:
    configure_stdio()
    args = parse_args()
    version = parse_version()
    report: dict[str, Any] = {
        "ok": True,
        "version": version,
        "system": detect_system(),
    }

    if args.no_sync:
        report["sync"] = {"status": SKIPPED, "reason": "--no-sync"}
    else:
        sync = command_result([sys.executable, str(ROOT / "tools" / "sw_sync_installed.py")], max(args.timeout, 60))
        report["sync"] = {"status": READY if sync["ok"] else FAILED, **sync}
        if not sync["ok"]:
            report["ok"] = False

    if args.skip_doctor:
        report["doctor"] = {"status": SKIPPED, "reason": "--skip-doctor"}
    else:
        doctor = command_result(
            [sys.executable, str(ROOT / "tools" / "sw_doctor.py"), "--scope", "all"],
            max(args.timeout, 60),
        )
        report["doctor"] = {"status": READY if doctor["ok"] else FAILED, **doctor}
        if not doctor["ok"]:
            report["ok"] = False

    if args.no_sync:
        report["obsidian_sync"] = {"status": SKIPPED, "reason": "--no-sync"}
    else:
        obsidian_sync = command_result(
            [sys.executable, str(ROOT / "tools" / "sync_obsidian_aesthetic_vault.py"), "--json"],
            max(args.timeout, 30),
        )
        report["obsidian_sync"] = {"status": READY if obsidian_sync["ok"] else FAILED, **obsidian_sync}
        if not obsidian_sync["ok"]:
            report["ok"] = False

    installed = installed_paths()
    keys = {
        "banana": check_banana(),
        "dreamina": check_dreamina(),
        "kling": check_kling(),
        "seedance": check_seedance(),
        "feishu": check_feishu(),
    }
    relay = check_url_relay(args.no_network, args.timeout)
    obsidian = check_obsidian_vault()
    features = feature_status(installed, keys, relay, obsidian)
    needs = collect_needs(features, keys, relay)
    if any(feature["status"] == FAILED for feature in features):
        report["ok"] = False

    report.update(
        {
            "installed_paths": installed,
            "keys": keys,
            "url_relay": relay,
            "obsidian": obsidian,
            "features": features,
            "needs_config": needs,
        }
    )

    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        print_human(report)
        if not report["ok"]:
            print("\nBootstrap found install issues. Re-run after repairing the items above.")
    return 0 if report["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
