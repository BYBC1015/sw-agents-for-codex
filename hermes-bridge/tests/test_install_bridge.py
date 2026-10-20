import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

MODULE_PATH = Path(__file__).resolve().parents[1] / "scripts" / "install_bridge.py"
SPEC = importlib.util.spec_from_file_location("install_bridge", MODULE_PATH)
bridge = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(bridge)


class BridgeInstallTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        base = Path(self.tmp.name)
        self.project = base / "SW project"
        self.home = base / "Hermes home"
        (self.home / "skills" / "unrelated").mkdir(parents=True)
        (self.home / "skills" / "unrelated" / "SKILL.md").write_text("preserve", encoding="utf-8")
        for relative, text in {
            "VERSION.md": "V1.15.0",
            "AGENTS.md": "rules",
            "kling-api/scripts/kling_task.py": "runner",
            "hermes-bridge/SKILL.md": "---\nname: hermes-bridge\ndescription: Bridge.\n---\nShared work.",
            "hermes-bridge/references/collaboration.md": "handoff",
            "private/secrets.json": "must-never-be-copied",
        }.items():
            path = self.project / relative
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(text, encoding="utf-8")
        self.target = self.home / "skills" / "hermes-bridge"

    def test_preview_writes_nothing(self):
        result = bridge.install(self.project, self.home)
        self.assertEqual(result["mode"], "preview")
        self.assertFalse(self.target.exists())

    def test_install_preserves_unrelated_and_only_copies_allowlist(self):
        bridge.install(self.project, self.home, execute=True)
        files = {str(p.relative_to(self.target)).replace("\\", "/") for p in self.target.rglob("*") if p.is_file()}
        self.assertEqual(files, {"SKILL.md", "references/collaboration.md", "references/runtime.json", bridge.MANAGED})
        runtime = json.loads((self.target / "references/runtime.json").read_text(encoding="utf-8"))
        self.assertEqual(runtime["kling_runner"], str(self.project.resolve() / "kling-api/scripts/kling_task.py"))
        self.assertEqual((self.home / "skills/unrelated/SKILL.md").read_text(), "preserve")
        self.assertNotIn("must-never-be-copied", "".join(p.read_text(encoding="utf-8") for p in self.target.rglob("*") if p.is_file()))

    def test_install_is_idempotent_and_allows_source_refresh(self):
        bridge.install(self.project, self.home, execute=True)
        self.assertEqual(bridge.install(self.project, self.home, execute=True)["changed_files"], [])
        (self.project / "hermes-bridge/references/collaboration.md").write_text("new protocol", encoding="utf-8")
        self.assertEqual(bridge.install(self.project, self.home, execute=True)["changed_files"], ["references/collaboration.md"])

    def test_refuses_overwrite_of_local_changes(self):
        bridge.install(self.project, self.home, execute=True)
        skill = self.target / "SKILL.md"
        skill.write_text("user edit", encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "locally modified"):
            bridge.install(self.project, self.home, execute=True)
        self.assertEqual(skill.read_text(), "user edit")

    def test_refuses_unmanaged_skill_and_missing_home(self):
        self.target.mkdir()
        with self.assertRaisesRegex(ValueError, "unmanaged"):
            bridge.install(self.project, self.home, execute=True)
        with self.assertRaisesRegex(ValueError, "does not exist"):
            bridge.install(self.project, self.home / "missing", execute=True)


if __name__ == "__main__":
    unittest.main()
