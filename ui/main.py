#!/usr/bin/env python3
"""UI server entrypoint for chat + approval dashboard."""

from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
import os
from pathlib import Path


def run() -> None:
    port = int(os.environ.get("UI_PORT", "3000"))
    web_root = Path(__file__).resolve().parent
    os.chdir(web_root)
    server = ThreadingHTTPServer(("0.0.0.0", port), SimpleHTTPRequestHandler)
    print(f"[ui] serving {web_root} at http://127.0.0.1:{port}")
    server.serve_forever()


if __name__ == "__main__":
    run()
