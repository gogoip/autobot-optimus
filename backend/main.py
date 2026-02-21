#!/usr/bin/env python3
"""Backend API and orchestration entrypoint."""

from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import json
import os


class BackendHandler(BaseHTTPRequestHandler):
    def _send_json(self, payload: dict, status: int = 200) -> None:
        body = json.dumps(payload).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self) -> None:  # noqa: N802 - BaseHTTPRequestHandler interface
        if self.path in {"/", "/health"}:
            self._send_json({"service": "backend", "status": "ok"})
            return
        if self.path == "/orchestrate":
            self._send_json(
                {
                    "service": "backend",
                    "message": "Orchestration endpoint placeholder.",
                }
            )
            return
        self._send_json({"error": "Not found"}, status=404)


def run() -> None:
    port = int(os.environ.get("BACKEND_PORT", "8000"))
    server = ThreadingHTTPServer(("0.0.0.0", port), BackendHandler)
    print(f"[backend] listening on http://127.0.0.1:{port}")
    server.serve_forever()


if __name__ == "__main__":
    run()
