from __future__ import annotations

import contextlib
import importlib.util
import io
import json
import subprocess
import sys
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest import mock


ROOT = Path(__file__).resolve().parents[1]


def load_tool_module(name: str):
    path = ROOT / "tools" / f"{name}.py"
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class ConsistencyCheckProfileTests(unittest.TestCase):
    def test_hot_profile_runs_as_a_compact_repo_check(self) -> None:
        result = subprocess.run(
            [
                sys.executable,
                str(ROOT / "tools" / "sw_consistency_check.py"),
                "--profile",
                "hot",
            ],
            cwd=ROOT,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )

        self.assertEqual(result.returncode, 0, result.stderr + result.stdout)
        self.assertIn("profile=hot", result.stdout)

    def test_tool_registry_lite_is_compact_and_actionable(self) -> None:
        registry_path = ROOT / "tools" / "sw_tool_registry_lite.json"
        data = json.loads(registry_path.read_text(encoding="utf-8"))
        tools = data.get("tools", [])
        by_id = {tool.get("id"): tool for tool in tools}
        required_ids = {
            "black-background-cutout",
            "banana-pro",
            "dreamina-cli",
            "seedance-2-video",
            "url-relay",
            "kling-api",
            "storyboard-visual-word",
            "feishu-docs",
        }

        self.assertEqual(set(by_id), required_ids)
        self.assertLess(registry_path.stat().st_size, 10000)

        for tool_id, tool in by_id.items():
            with self.subTest(tool_id=tool_id):
                for field in [
                    "name",
                    "capability",
                    "skill_path",
                    "loads_as",
                    "trigger_mode",
                    "configured_by",
                    "cost_lane",
                    "confirmation_required",
                    "fallback",
                ]:
                    self.assertIn(field, tool)
                self.assertEqual(tool["loads_as"], "tool_skill")
                self.assertIn(tool["cost_lane"], {"low", "medium", "high"})
                self.assertTrue((ROOT / tool["skill_path"]).exists())
                self.assertIsInstance(tool["configured_by"], list)
                self.assertIsInstance(tool["confirmation_required"], list)
                self.assertIsInstance(tool["fallback"], list)

        for high_cost_id in ["banana-pro", "dreamina-cli", "seedance-2-video", "kling-api"]:
            self.assertIn("real_generation", by_id[high_cost_id]["confirmation_required"])

    def test_repo_text_scan_skips_local_codex_cache(self) -> None:
        checker = load_tool_module("sw_consistency_check")

        files = checker.iter_text_files([ROOT])

        self.assertFalse(any(".codex" in path.relative_to(ROOT).parts for path in files))


class DoctorGitStatusTests(unittest.TestCase):
    def test_run_prints_label_instead_of_python_command(self) -> None:
        doctor = load_tool_module("sw_doctor")

        output = io.StringIO()
        with mock.patch.object(
            doctor.subprocess,
            "run",
            return_value=SimpleNamespace(returncode=0),
        ):
            with contextlib.redirect_stdout(output):
                code = doctor.run([sys.executable, "tool.py"], label="consistency check")

        text = output.getvalue()
        self.assertEqual(code, 0)
        self.assertIn("check: consistency check", text)
        self.assertNotIn("python", text.lower())
        self.assertNotIn("tool.py", text)

    def test_default_git_status_prints_summary_not_raw_file_list(self) -> None:
        doctor = load_tool_module("sw_doctor")

        def fake_run(command, **_kwargs):
            if command[:2] == ["git", "branch"]:
                return SimpleNamespace(stdout="feature/demo\n")
            if command[:2] == ["git", "status"]:
                return SimpleNamespace(stdout=" M AGENTS.md\n?? docs/new.md\n")
            raise AssertionError(f"unexpected command: {command}")

        output = io.StringIO()
        with mock.patch.object(doctor.subprocess, "run", side_effect=fake_run):
            with contextlib.redirect_stdout(output):
                doctor.git_status(details=False)

        text = output.getvalue()
        self.assertIn("git branch: feature/demo", text)
        self.assertIn("git status summary:", text)
        self.assertIn("modified=1", text)
        self.assertIn("untracked=1", text)
        self.assertIn("staged=0", text)
        self.assertNotIn("AGENTS.md", text)

    def test_details_git_status_keeps_raw_file_list(self) -> None:
        doctor = load_tool_module("sw_doctor")

        def fake_run(command, **_kwargs):
            if command[:2] == ["git", "branch"]:
                return SimpleNamespace(stdout="feature/demo\n")
            if command[:2] == ["git", "status"]:
                return SimpleNamespace(stdout=" M AGENTS.md\n?? docs/new.md\n")
            raise AssertionError(f"unexpected command: {command}")

        output = io.StringIO()
        with mock.patch.object(doctor.subprocess, "run", side_effect=fake_run):
            with contextlib.redirect_stdout(output):
                doctor.git_status(details=True)

        text = output.getvalue()
        self.assertIn("git status:", text)
        self.assertIn("AGENTS.md", text)
        self.assertIn("docs/new.md", text)


if __name__ == "__main__":
    unittest.main()
