"""The database connection and the migrations (db/migrations/*.sql, applied once each, in order)."""
import sqlite3
from pathlib import Path

MIGRATIONS = Path(__file__).resolve().parents[2] / "db" / "migrations"


def connect(path=":memory:"):
    conn = sqlite3.connect(path)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    migrate(conn)
    return conn


def migrate(conn):
    conn.execute("CREATE TABLE IF NOT EXISTS _migrations (name TEXT PRIMARY KEY)")
    done = {r[0] for r in conn.execute("SELECT name FROM _migrations")}
    for f in sorted(MIGRATIONS.glob("*.sql")):
        if f.name not in done:
            conn.executescript(f.read_text())
            conn.execute("INSERT INTO _migrations (name) VALUES (?)", (f.name,))
    conn.commit()
