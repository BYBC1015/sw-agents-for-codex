"""Real process lifecycle regressions; all data lives in temporary projects."""
import json
import os
from pathlib import Path
import signal
import socket
import subprocess
import sys
import tempfile
import time
import unittest
from urllib.request import urlopen

APP = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(APP))
from settings import VERSION


class LauncherTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(prefix='canvas-launch-')
        self.root = Path(self.tmp.name).resolve()
        # Include spaces, Unicode and shell metacharacters in the real WMI path.
        self.data = self.root / '项目 & $画布 data'
        with socket.socket() as probe:
            probe.bind(('127.0.0.1', 0))
            self.port = probe.getsockname()[1]
        self.url = f'http://127.0.0.1:{self.port}/api/health'
        self.command = [sys.executable, '-B', '-X', 'utf8', str(APP/'launcher.py'),
                        '--no-browser', '--port', str(self.port),
                        '--data-dir', str(self.data), '--registry', str(self.root/'catalog.sqlite3'),
                        '--workspace-root', str(self.root/'workspace')]
        self.env = dict(os.environ, MEDIA_CANVAS_MEDIA_ROOTS=json.dumps([str(self.root/'允许素材')]))

    def health(self):
        with urlopen(self.url, timeout=2) as response:
            return json.load(response)

    def launch(self, command=None):
        return subprocess.run(command or self.command, env=self.env, capture_output=True,
                              text=True, encoding='utf-8', timeout=40)

    def tearDown(self):
        pid_file = self.data/'server.pid'
        if pid_file.exists():
            pid = int(pid_file.read_text())
            if os.name == 'nt':
                subprocess.run(['taskkill', '/PID', str(pid), '/F'],
                               capture_output=True, timeout=10)
            else:
                os.kill(pid, signal.SIGTERM)
            for _ in range(50):
                try:
                    self.health()
                except OSError:
                    break
                time.sleep(.1)
        self.tmp.cleanup()

    def test_survives_launcher_exit_reuses_pid_and_preserves_state(self):
        first = self.launch()
        self.assertEqual(first.returncode, 0, first.stderr)
        first_pid = (self.data/'server.pid').read_text()
        health = self.health()
        self.assertEqual(health['version'], VERSION)
        self.assertEqual(Path(health['dataDir']), self.data)
        self.assertIn(str(self.root/'允许素材'), health['mediaRoots'])
        second = self.launch()
        self.assertEqual(second.returncode, 0, second.stderr)
        self.assertEqual(first_pid, (self.data/'server.pid').read_text())
        self.assertEqual(health['projectId'], self.health()['projectId'])
        self.assertIn('start pid=', (self.data/'server.log').read_text(encoding='utf-8'))

    def test_rejects_occupied_port_for_another_data_directory(self):
        first = self.launch()
        self.assertEqual(first.returncode, 0, first.stderr)
        before = self.health()
        other = self.command + ['--data-dir', str(self.root/'other')]
        refused = self.launch(other)
        self.assertNotEqual(refused.returncode, 0)
        self.assertIn('端口已有其他版本或项目服务', refused.stderr)
        self.assertEqual(before, self.health())
        self.assertFalse((self.root/'other').exists())

    @unittest.skipUnless(os.name == 'nt', 'Windows command-tree cleanup regression')
    def test_survives_termination_of_calling_process_tree(self):
        ready = self.root/'ready'
        script = (
            "import json,pathlib,subprocess,sys,time;"
            "r=subprocess.run(json.loads(sys.argv[1]),capture_output=True);"
            "pathlib.Path(sys.argv[2]).write_text(str(r.returncode));"
            "time.sleep(60)"
        )
        parent = subprocess.Popen([sys.executable, '-c', script, json.dumps(self.command), str(ready)],
                                  env=self.env, creationflags=subprocess.CREATE_NO_WINDOW)
        try:
            deadline = time.monotonic()+40
            while not ready.exists() and time.monotonic() < deadline:
                time.sleep(.1)
            self.assertTrue(ready.exists(), 'launcher did not return')
            self.assertEqual(ready.read_text(), '0')
            before = self.health()
            killed = subprocess.run(['taskkill', '/PID', str(parent.pid), '/T', '/F'],
                                    capture_output=True, timeout=10)
            self.assertEqual(killed.returncode, 0)
            parent.wait(timeout=10)
            self.assertEqual(before, self.health())
        finally:
            if parent.poll() is None:
                parent.terminate()
                parent.wait(timeout=10)


if __name__ == '__main__':
    unittest.main()
