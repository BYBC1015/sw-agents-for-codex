"""Offline contract tests for Kling's current API and explicit legacy support."""

from contextlib import redirect_stdout
import importlib.util
import io
import json
import os
from pathlib import Path
import tempfile
from types import SimpleNamespace
import unittest
from unittest.mock import MagicMock, patch
import urllib.error


SPEC = importlib.util.spec_from_file_location("kling_task", Path(__file__).parents[1] / "scripts" / "kling_task.py")
kling = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(kling)


def args(*values):
    return kling.build_parser().parse_args(values)


class KlingContractTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.directory = Path(temporary.name)
        for item in (
            patch.object(kling, "CONFIG_DIR", self.directory),
            patch.object(kling, "SECRETS_FILE", self.directory / "secrets.json"),
            patch.dict(os.environ, {}, clear=True),
            patch.object(kling.urllib.request, "build_opener", side_effect=AssertionError("Unexpected network")),
            patch.object(kling.urllib.request, "urlopen", side_effect=AssertionError("Unexpected network")),
        ):
            item.start()
            self.addCleanup(item.stop)

    def config(self, **values):
        kling.SECRETS_FILE.write_text(json.dumps(values), encoding="utf-8")

    def payload(self, *values):
        return kling.build_payload(args("dry-run", "--prompt", "A quiet landscape.", *values))

    def test_private_api_key_wins_over_all_stale_environment_credentials(self):
        self.config(api_key="private-new-key")
        with patch.dict(os.environ, {"KLING_API_KEY": "stale-key", "KLING_API_TOKEN": "stale-token",
                                     "KLING_ACCESS_KEY": "stale-ak", "KLING_SECRET_KEY": "stale-sk"}):
            self.assertEqual(kling.auth_header(), ("Authorization", "Bearer private-new-key"))
            self.assertEqual(kling.read_secrets()["auth_source"], "private_config")

    def test_credentials_are_never_spliced_between_sources(self):
        self.config(access_key="file-ak")
        with patch.dict(os.environ, {"KLING_SECRET_KEY": "env-sk"}):
            with self.assertRaises(kling.KlingError):
                kling.auth_header("legacy")
        with patch.dict(os.environ, {"KLING_ACCESS_KEY": "env-ak", "KLING_SECRET_KEY": "env-sk"}):
            with patch.object(kling, "create_jwt", return_value="signed") as create:
                self.assertEqual(kling.auth_header("legacy")[1], "Bearer signed")
                create.assert_called_once_with("env-ak", "env-sk")

    def test_complete_private_legacy_group_wins_over_environment_token(self):
        self.config(access_key="private-ak", secret_key="private-sk")
        with patch.dict(os.environ, {"KLING_API_TOKEN": "env-token"}):
            with patch.object(kling, "create_jwt", return_value="signed") as create:
                kling.auth_header("legacy")
                create.assert_called_once_with("private-ak", "private-sk")

    def test_api_key_supports_both_versions_but_jwt_is_legacy_only(self):
        self.config(api_key="new-key")
        self.assertEqual(kling.auth_header("legacy")[1], "Bearer new-key")
        self.config(access_key="old-ak", secret_key="old-sk")
        with self.assertRaises(kling.KlingError):
            kling.auth_header()
        with patch.dict(os.environ, {"KLING_API_KEY": "env-new-key"}):
            self.assertEqual(kling.auth_header()[1], "Bearer env-new-key")

    def test_missing_auth_is_reported_without_network(self):
        output = io.StringIO()
        with redirect_stdout(output):
            result = kling.cmd_doctor(args("doctor"))
        self.assertEqual(result, 2)
        self.assertIn("api_key: missing", output.getvalue())

    def test_doctor_never_shows_key_prefix_or_suffix(self):
        self.config(api_key="private-new-key")
        output = io.StringIO()
        with redirect_stdout(output):
            self.assertEqual(kling.cmd_doctor(args("doctor")), 0)
        self.assertIn("api_key: present", output.getvalue())
        self.assertNotIn("private-new-key", output.getvalue())
        self.assertNotIn("priv", output.getvalue().replace("private_config", ""))

    def test_setup_key_reads_stdin_without_logging_secret(self):
        output = io.StringIO()
        with patch.object(kling.sys, "stdin", io.StringIO("test-input-key\n")), redirect_stdout(output):
            self.assertEqual(kling.cmd_setup_key(args("setup-key", "--api-key-stdin")), 0)
        self.assertEqual(json.loads(kling.SECRETS_FILE.read_text())["api_key"], "test-input-key")
        self.assertNotIn("test-input-key", output.getvalue())
        self.assertFalse(list(self.directory.glob(".secrets-*.tmp")))

    def test_setup_preserves_other_credentials_but_drops_unknown_config_keys(self):
        self.config(access_key="legacy-ak", secret_key="legacy-sk", unknown_setting="unused")
        kling.write_secrets(api_key="new-key")
        stored = json.loads(kling.SECRETS_FILE.read_text())
        self.assertEqual(stored["access_key"], "legacy-ak")
        self.assertEqual(stored["secret_key"], "legacy-sk")
        self.assertNotIn("unknown_setting", stored)
        kling.write_secrets("replacement-ak", "replacement-sk")
        self.assertEqual(json.loads(kling.SECRETS_FILE.read_text())["api_key"], "new-key")

    def test_permission_failure_leaves_existing_secret_file_unchanged(self):
        self.config(api_key="original")
        with patch.object(kling, "restrict_private_file", side_effect=kling.KlingError("ACL failed")):
            with self.assertRaises(kling.KlingError):
                kling.write_secrets(api_key="replacement")
        self.assertEqual(json.loads(kling.SECRETS_FILE.read_text())["api_key"], "original")
        self.assertFalse(list(self.directory.glob(".secrets-*.tmp")))

    def test_windows_permissions_use_sid_remove_inheritance_and_no_secret_arguments(self):
        results = [SimpleNamespace(returncode=0, stdout='"user","S-1-5-21-1234-1001"'),
                   SimpleNamespace(returncode=0, stdout="processed")]
        with patch.object(kling.os, "name", "nt"), patch.object(kling.subprocess, "CREATE_NO_WINDOW", 0, create=True), \
                patch.object(kling.subprocess, "run", side_effect=results) as run:
            kling.restrict_private_file("temporary-secret-file")
        self.assertEqual(run.call_args.args[0], ["icacls", "temporary-secret-file", "/inheritance:r",
                                                "/grant:r", "*S-1-5-21-1234-1001:(F)"])

    def test_online_doctor_uses_free_read_only_cost_query_and_checks_both_codes(self):
        self.config(api_key="test-sensitive-key")
        for inner_code in (0, 1000):
            output = io.StringIO()
            with patch.object(kling, "request_json", return_value={"code": 0, "data": {"code": inner_code}}) as request, redirect_stdout(output):
                if inner_code == 0:
                    self.assertEqual(kling.cmd_doctor(args("doctor", "--online")), 0)
                else:
                    with self.assertRaises(kling.KlingError):
                        kling.cmd_doctor(args("doctor", "--online"))
            self.assertEqual(request.call_args.args[0], "GET")
            self.assertTrue(request.call_args.args[1].startswith("/account/costs?start_time="))
            self.assertNotIn("test-sensitive-key", output.getvalue())

    def test_invalid_key_whitespace_is_rejected_safely(self):
        self.config(api_key="first\nsecond")
        with self.assertRaisesRegex(kling.KlingError, "invalid whitespace"):
            kling.auth_header()

    def test_current_text_defaults_and_options_match_schema(self):
        payload = self.payload("--external-task-id", "shot-1", "--no-watermark")
        self.assertEqual(payload["settings"], {"resolution": "1080p", "duration": 5, "audio": "off",
                                               "multi_shot": False, "aspect_ratio": "16:9"})
        self.assertEqual(payload["options"], {"external_task_id": "shot-1", "watermark_info": {"enabled": False}})
        self.assertNotIn("model_name", payload)
        self.assertEqual(kling.endpoint_path("text"), "/text-to-video/kling-3.0")
        self.assertEqual(kling.endpoint_path("image"), "/image-to-video/kling-3.0")
        self.assertEqual(kling.endpoint_path("omni"), "/omni-video/kling-3.0-omni")

    def test_model_aliases_are_explicit_and_unknown_models_rejected(self):
        self.assertEqual(kling.model_default("text", "kling-v3"), "kling-3.0")
        self.assertEqual(kling.model_default("omni", "kling-v3-omni"), "kling-3.0-omni")
        with self.assertRaises(kling.KlingError):
            self.payload("--model-name", "kling-v2-6")

    def test_current_duration_bounds_and_integer_type(self):
        for value in ("3", "15"):
            self.assertEqual(self.payload("--duration", value)["settings"]["duration"], int(value))
        for value in ("2", "16", "3.5", "5.0", "garbage"):
            with self.subTest(value=value), self.assertRaises(kling.KlingError):
                self.payload("--duration", value)

    def test_image_to_video_first_last_frame_and_element_alias(self):
        payload = self.payload("--kind", "image", "--image-url", "https://example.com/first.png",
                               "--image-tail-url", "https://example.com/last.png", "--element-id", "e-1")
        self.assertEqual([item["type"] for item in payload["contents"]], ["prompt", "first_frame", "last_frame", "element"])
        self.assertEqual(payload["contents"][-1], {"type": "element", "element_id": "e-1", "id": "element_1"})
        self.assertNotIn("aspect_ratio", payload["settings"])

    def test_unused_or_excess_media_is_rejected(self):
        for values in (
            ("--video-url", "https://example.com/v.mp4"),
            ("--image-url", "https://example.com/i.png"),
            ("--kind", "image"),
            ("--kind", "image", "--image-url", "https://example.com/1.png", "--image-url", "https://example.com/2.png"),
            ("--kind", "multi-image"),
            ("--kind", "omni", "--video-url", "https://example.com/1.mp4", "--video-url", "https://example.com/2.mp4"),
        ):
            with self.subTest(values=values), self.assertRaises(kling.KlingError):
                self.payload(*values)

    def test_base_video_edit_follows_official_example(self):
        payload = self.payload("--kind", "omni", "--video-url", "https://example.com/v.mp4", "--audio", "original")
        self.assertEqual(payload["contents"][-1], {"type": "base_video", "url": "https://example.com/v.mp4", "id": "video_1"})
        self.assertEqual(payload["settings"], {"resolution": "1080p", "audio": "original", "multi_shot": False})
        for values in (("--multi-shot",), ("--sound", "on"),
                       ("--image-url", "https://example.com/i.png", "--omni-image-type", "first_frame")):
            with self.subTest(values=values), self.assertRaises(kling.KlingError):
                self.payload("--kind", "omni", "--video-url", "https://example.com/v.mp4", *values)

    def test_feature_video_uses_target_duration_but_cannot_generate_audio(self):
        common = ("--kind", "omni", "--video-url", "https://example.com/v.mp4", "--video-refer-type", "feature")
        payload = self.payload(*common, "--duration", "8", "--multi-shot")
        self.assertEqual(payload["contents"][-1]["type"], "feature_video")
        self.assertEqual(payload["settings"]["duration"], 8)
        self.assertTrue(self.payload(*common)["settings"]["multi_shot"])
        self.assertFalse(self.payload(*common, "--single-shot")["settings"]["multi_shot"])
        for audio in ("native", "original"):
            with self.assertRaises(kling.KlingError):
                self.payload(*common, "--audio", audio)

    def test_omni_reference_limits_include_elements(self):
        elements = sum((["--element-id", f"e-{i}"] for i in range(4)), [])
        self.payload("--kind", "omni", "--video-url", "https://example.com/v.mp4", *elements)
        with self.assertRaises(kling.KlingError):
            self.payload("--kind", "omni", "--video-url", "https://example.com/v.mp4", *elements,
                         "--image-url", "https://example.com/i.png")
        with self.assertRaises(kling.KlingError):
            self.payload("--kind", "omni", *elements, "--video-element-id", "video-role", "--image-url", "https://example.com/i.png")
        with self.assertRaises(kling.KlingError):
            self.payload("--kind", "omni", "--video-url", "https://example.com/v.mp4",
                         "--video-element-id", "video-role", "--element-id", "image-role")

    def test_current_rejects_legacy_only_settings(self):
        for values in (("--camera-type", "down_back"), ("--cfg-scale", "0.5"),
                       ("--multi-prompt-json", "[]"), ("--shot-type", "customize")):
            with self.subTest(values=values), self.assertRaises(kling.KlingError):
                self.payload(*values)

    def test_legacy_mode_sound_aliases_and_conflicts(self):
        payload = self.payload("--mode", "std", "--sound", "on")
        self.assertEqual(payload["settings"]["resolution"], "720p")
        self.assertEqual(payload["settings"]["audio"], "native")
        with self.assertRaises(kling.KlingError):
            self.payload("--mode", "std", "--resolution", "4k")
        with self.assertRaises(kling.KlingError):
            self.payload("--sound", "on", "--audio", "off")

    def test_explicit_legacy_retains_payload_and_route(self):
        payload = self.payload("--api-version", "legacy", "--model-name", "kling-v2-6", "--sound", "off")
        self.assertEqual(payload["model_name"], "kling-v2-6")
        self.assertEqual(payload["duration"], "5")
        self.assertEqual(payload["mode"], "pro")
        self.assertEqual(kling.endpoint_path("text", "task-1", "legacy"), "/v1/videos/text2video/task-1")
        with self.assertRaises(kling.KlingError):
            self.payload("--api-version", "legacy", "--video-url", "https://example.com/v.mp4")

    def test_dry_run_does_not_read_local_image_bytes_or_use_network(self):
        image = self.directory / "private.png"
        image.write_bytes(b"test-private-image-content")
        for version in ("current", "legacy"):
            output = io.StringIO()
            with patch.object(Path, "read_bytes", side_effect=AssertionError("dry-run read image bytes")), redirect_stdout(output):
                kling.cmd_dry_run(args("dry-run", "--api-version", version, "--kind", "image",
                                      "--image-file", str(image), "--prompt", "A scene"))
            self.assertIn("LOCAL_IMAGE_BASE64_REDACTED", output.getvalue())
            self.assertNotIn("test-private-image-content", output.getvalue())

    def test_real_generation_and_local_upload_guards_run_before_network(self):
        with self.assertRaisesRegex(kling.KlingError, "--yes"):
            kling.cmd_run(args("run", "--prompt", "A scene"))
        with self.assertRaisesRegex(kling.KlingError, "--confirm-upload"):
            kling.cmd_run(args("run", "--kind", "image", "--image-file", "private.png", "--yes"))

    def test_api_route_and_auth_version_cannot_be_mixed(self):
        with self.assertRaisesRegex(kling.KlingError, "do not match"):
            kling.request_json("POST", "/v1/videos/text2video")
        with self.assertRaisesRegex(kling.KlingError, "do not match"):
            kling.request_json("POST", "/text-to-video/kling-3.0", api_version="legacy")

    def test_http_and_api_errors_redact_credentials(self):
        key = "test-sensitive-key"
        self.config(api_key=key)
        opener = MagicMock()
        opener.open.side_effect = urllib.error.HTTPError("https://example.com", 401, "unauthorized", {},
                                                        io.BytesIO(f"denied Bearer {key}".encode()))
        with patch.object(kling.urllib.request, "build_opener", return_value=opener):
            with self.assertRaises(kling.KlingError) as raised:
                kling.request_json("GET", "/tasks?external_task_ids=test")
        self.assertNotIn(key, str(raised.exception))
        self.assertIn("REDACTED", str(raised.exception))
        opener.open.side_effect = None
        opener.open.return_value.__enter__.return_value.read.return_value = json.dumps({"code": 1000, "message": key}).encode()
        with patch.object(kling.urllib.request, "build_opener", return_value=opener):
            with self.assertRaises(kling.KlingError) as raised:
                kling.request_json("GET", "/tasks?external_task_ids=test")
        self.assertNotIn(key, str(raised.exception))

    def test_authenticated_redirect_is_refused(self):
        with self.assertRaises(kling.KlingError):
            kling.NoAuthRedirect().redirect_request(None, None, 302, "redirect", {}, "https://elsewhere.example")

    def test_task_query_encoding_and_exact_matching(self):
        self.assertEqual(kling.endpoint_path("omni", "id&other=1"), "/tasks?task_ids=id%26other%3D1")
        response = {"data": [{"id": "other"}, {"id": "wanted", "status": "processing"}]}
        self.assertEqual(kling.extract_data(response, "wanted")["status"], "processing")
        with self.assertRaises(kling.KlingError):
            kling.extract_data(response, "missing")

    def test_current_poll_downloads_only_matching_successful_task(self):
        response = {"code": 0, "data": [{"id": "task-1", "status": "succeeded",
                                          "outputs": [{"type": "video", "url": "https://example.com/final.mp4"}]}]}
        with patch.object(kling, "request_json", return_value=response) as request, patch.object(kling, "download_file") as download:
            manifest = kling.poll_task("omni", "task-1", self.directory / "output", 5, 60)
        request.assert_called_once_with("GET", "/tasks?task_ids=task-1", api_version="current")
        download.assert_called_once_with("https://example.com/final.mp4", self.directory / "output" / "final.mp4")
        self.assertEqual(manifest["api_version"], "current")

    def test_submit_only_saves_current_version_and_task_id(self):
        with patch.object(kling, "request_json", return_value={"code": 0, "data": {"id": "task-1", "status": "submitted"}}) as request:
            kling.cmd_run(args("run", "--prompt", "A scene", "--yes", "--submit-only", "--output-dir", str(self.directory)))
        self.assertEqual(request.call_args.args[1], "/text-to-video/kling-3.0")
        manifest = kling.load_manifest(self.directory)
        self.assertEqual((manifest["api_version"], manifest["task_id"]), ("current", "task-1"))

    def test_old_manifest_automatically_resumes_legacy_api(self):
        kling.save_manifest(self.directory, {"kind": "image", "task_id": "old-task"})
        with patch.object(kling, "poll_task", return_value={}) as poll:
            kling.cmd_poll(args("poll", "--output-dir", str(self.directory)))
        self.assertEqual(poll.call_args.args[-1], "legacy")


if __name__ == "__main__":
    unittest.main()
