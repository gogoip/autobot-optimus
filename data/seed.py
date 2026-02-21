#!/usr/bin/env python3
"""Deterministic data seeding script."""

import sqlite3
from pathlib import Path


def main() -> None:
    data_dir = Path(__file__).resolve().parent
    db_path = data_dir / "dev.db"
    schema_path = data_dir / "schema.sql"

    with sqlite3.connect(db_path) as conn:
        conn.executescript(schema_path.read_text(encoding="utf-8"))
        conn.execute("DELETE FROM approvals")
        conn.execute("DELETE FROM conversations")

        conn.execute(
            "INSERT INTO conversations (id, title, created_at) VALUES (?, ?, ?)",
            (1, "Demo conversation", "2026-01-01T00:00:00Z"),
        )
        conn.execute(
            "INSERT INTO approvals (id, conversation_id, action, status, created_at) VALUES (?, ?, ?, ?, ?)",
            (1, 1, "deploy", "pending", "2026-01-01T00:01:00Z"),
        )

    print(f"[data] seeded deterministic data at {db_path}")


if __name__ == "__main__":
    main()
