"""Members: name, email and role. Other modules use this file only."""
import re

EMAIL = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


def add_member(conn, name, email, role="member"):
    name, email = (name or "").strip(), (email or "").strip().lower()
    if not name:
        raise ValueError("a member needs a name")
    if not EMAIL.match(email):
        raise ValueError("not an email address")
    if role not in ("member", "organizer"):
        raise ValueError("unknown role")
    cur = conn.execute("INSERT INTO members (name, email, role) VALUES (?, ?, ?)", (name, email, role))
    conn.commit()
    return cur.lastrowid


def get_member(conn, member_id):
    row = conn.execute("SELECT id, name, email, role FROM members WHERE id = ?", (member_id,)).fetchone()
    return dict(row) if row else None


def is_organizer(conn, member_id):
    m = get_member(conn, member_id)
    return bool(m) and m["role"] == "organizer"
