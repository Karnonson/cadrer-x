"""Workshops: one dated session with a fixed number of seats. Other modules use this file only."""


def add_workshop(conn, title, starts_at, seats):
    title = (title or "").strip()
    if not title:
        raise ValueError("a workshop needs a title")
    if not isinstance(seats, int) or seats < 1:
        raise ValueError("a workshop needs at least one seat")
    cur = conn.execute("INSERT INTO workshops (title, starts_at, seats) VALUES (?, ?, ?)",
                       (title, starts_at, seats))
    conn.commit()
    return cur.lastrowid


def get_workshop(conn, workshop_id):
    row = conn.execute("SELECT id, title, starts_at, seats FROM workshops WHERE id = ?",
                       (workshop_id,)).fetchone()
    return dict(row) if row else None


def list_workshops(conn):
    """Every workshop, the soonest first."""
    return [dict(r) for r in conn.execute("SELECT id, title, starts_at, seats FROM workshops ORDER BY starts_at")]
