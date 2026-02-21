#!/usr/bin/env python3
"""Backend API entrypoint for local development."""

from __future__ import annotations

import os

import uvicorn


def run() -> None:
    port = int(os.environ.get("BACKEND_PORT", "8000"))
    uvicorn.run("backend.app.main:app", host="0.0.0.0", port=port, reload=False)


if __name__ == "__main__":
    run()
