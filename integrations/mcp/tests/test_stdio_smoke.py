"""stdio subprocess smoke test (skipped when the MCP SDK is not installed).

Launches the real server as a subprocess and speaks MCP JSON-RPC over stdio:
initialize → initialized → tools/list → tools/call. Asserts:
- stdout contains protocol frames ONLY (a stray print corrupts the wire), and
- the full stack works end to end against a synthetic local checkout
  (DEVSNIPS_MCP_SOURCE=local — no network).
"""
from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from support import SRC, make_synth_checkout


def mcp_sdk_available() -> bool:
    try:
        import mcp  # noqa: F401
        return True
    except ImportError:
        return False


class StdioSmokeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        if not mcp_sdk_available():
            raise unittest.SkipTest("mcp SDK not installed")
        cls.checkout = make_synth_checkout()
        cls.cache = Path(tempfile.mkdtemp(prefix="devsnips-mcp-stdio-"))
        env = dict(os.environ)
        env["PYTHONPATH"] = str(SRC)
        env["DEVSNIPS_MCP_SOURCE"] = "local"
        env["DEVSNIPS_MCP_LOCAL_ROOT"] = str(cls.checkout)
        env["DEVSNIPS_MCP_CACHE_DIR"] = str(cls.cache)
        env["DEVSNIPS_MCP_LOG_LEVEL"] = "ERROR"
        cls.env = env
        cls.proc = subprocess.Popen(
            [sys.executable, "-m", "devsnips_mcp"],
            stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            env=env, cwd=str(SRC), text=True, encoding="utf-8")

    @classmethod
    def tearDownClass(cls):
        try:
            cls.proc.stdin.close()
            cls.proc.wait(timeout=10)
        except Exception:  # noqa: BLE001 — test teardown must always kill the child
            cls.proc.kill()
        shutil.rmtree(cls.checkout, ignore_errors=True)
        shutil.rmtree(cls.cache, ignore_errors=True)

    def _send(self, payload):
        self.proc.stdin.write(json.dumps(payload) + "\n")
        self.proc.stdin.flush()

    def _recv(self):
        line = self.proc.stdout.readline()
        self.assertTrue(line, "server closed stdout before replying")
        return json.loads(line)

    def test_stdio_handshake_and_tool_call(self):
        self._send({"jsonrpc": "2.0", "id": 1, "method": "initialize",
                    "params": {"protocolVersion": "2025-06-18", "capabilities": {},
                               "clientInfo": {"name": "devsnips-mcp-test", "version": "0"}}})
        reply = self._recv()
        self.assertEqual(reply["id"], 1)
        self.assertIn("result", reply)

        self._send({"jsonrpc": "2.0", "method": "notifications/initialized"})
        self._send({"jsonrpc": "2.0", "id": 2, "method": "tools/list", "params": {}})
        listing = self._recv()
        names = {tool["name"] for tool in listing["result"]["tools"]}
        self.assertEqual(names, {"search_resources", "get_resource",
                                 "get_resource_file", "list_facets"})

        self._send({"jsonrpc": "2.0", "id": 3, "method": "tools/call",
                    "params": {"name": "search_resources",
                               "arguments": {"query": "dark sidebar"}}})
        result = self._recv()
        content = result["result"]["content"]
        self.assertEqual(content[0]["type"], "text")
        payload = json.loads(content[0]["text"])
        self.assertEqual(payload["items"][0]["id"], "React/Components/Sidebar/dark-sidebar")
        self.assertEqual(payload["registry"]["source"], "local")

        self._send({"jsonrpc": "2.0", "id": 4, "method": "tools/call",
                    "params": {"name": "get_resource_file",
                               "arguments": {"id": "Tailwind/Components/Buttons/dark-button",
                                             "file": "code.html"}}})
        result = self._recv()
        payload = json.loads(result["result"]["content"][0]["text"])
        self.assertIn("code.html", payload["content"])

    def test_stdout_carries_no_logging_noise(self):
        # stderr is where logs go; stdout must be parseable protocol frames only.
        # (implicitly verified by the JSON parsing in the other test; here we
        # assert the server is still alive and answering after traffic.)
        self._send({"jsonrpc": "2.0", "id": 9, "method": "tools/list", "params": {}})
        reply = self._recv()
        self.assertEqual(reply["id"], 9)


if __name__ == "__main__":
    unittest.main()
