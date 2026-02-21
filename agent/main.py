#!/usr/bin/env python3
"""Agent state machine and tool-calling loop entrypoint."""

import os
import signal
import sys
import time


def run_loop() -> None:
    interval = float(os.environ.get("AGENT_TICK_SECONDS", "2.0"))
    print(f"[agent] started with tick interval={interval}s")
    print("[agent] state machine/tool loop placeholder is running")

    running = True

    def stop_handler(signum, frame):  # type: ignore[no-untyped-def]
        nonlocal running
        running = False
        print(f"[agent] received signal {signum}; shutting down")

    signal.signal(signal.SIGINT, stop_handler)
    signal.signal(signal.SIGTERM, stop_handler)

    tick = 0
    while running:
        tick += 1
        print(f"[agent] tick={tick}")
        time.sleep(interval)

    print("[agent] stopped cleanly")


if __name__ == "__main__":
    try:
        run_loop()
    except KeyboardInterrupt:
        sys.exit(0)
