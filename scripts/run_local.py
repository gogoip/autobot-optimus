#!/usr/bin/env python3
"""Run local development stack in startup order with one command."""

from __future__ import annotations

import os
from pathlib import Path
import signal
import subprocess
import sys
import time
from typing import Sequence

ROOT = Path(__file__).resolve().parents[1]


def _start(name: str, cmd: Sequence[str]) -> subprocess.Popen[bytes]:
    process = subprocess.Popen(
        cmd,
        cwd=ROOT,
        env=os.environ.copy(),
    )
    print(f"[runner] started {name} (pid={process.pid})")
    return process


def main() -> int:
    python_exec = sys.executable
    print("[runner] seeding deterministic data")
    subprocess.run([python_exec, "data/seed.py"], cwd=ROOT, check=True)

    processes = [
        ("backend", _start("backend", [python_exec, "backend/main.py"])),
        ("agent", _start("agent", [python_exec, "agent/main.py"])),
        ("ui", _start("ui", [python_exec, "ui/main.py"])),
    ]

    def shutdown() -> None:
        print("\n[runner] shutting down all components")
        for _, process in reversed(processes):
            if process.poll() is None:
                process.terminate()
        for _, process in reversed(processes):
            if process.poll() is None:
                process.wait(timeout=5)

    def handle_signal(signum, frame):  # type: ignore[no-untyped-def]
        print(f"\n[runner] received signal {signum}")
        shutdown()
        raise SystemExit(0)

    signal.signal(signal.SIGINT, handle_signal)
    signal.signal(signal.SIGTERM, handle_signal)

    print("[runner] stack is up")
    print("[runner] backend: http://127.0.0.1:8000")
    print("[runner] ui:      http://127.0.0.1:3000")
    print("[runner] press Ctrl+C to stop")

    try:
        while True:
            for name, process in processes:
                exit_code = process.poll()
                if exit_code is not None:
                    print(f"[runner] {name} exited unexpectedly with code {exit_code}")
                    shutdown()
                    return exit_code
            time.sleep(1)
    except KeyboardInterrupt:
        shutdown()
        return 0


if __name__ == "__main__":
    raise SystemExit(main())
