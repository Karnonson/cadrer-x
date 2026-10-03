"""Sign-ups: a member's seat in a workshop. Other modules use this file only."""
from datetime import datetime, timezone

from clubhouse.workshops import api as workshops


class Complet(Exception):
    """The workshop has no seat left."""


def _now():
    return datetime.now(timezone.utc).isoformat()


def _member_exists(conn, member_id):
    return conn.execute("SELECT 1 FROM members WHERE id = ?", (member_id,)).fetchone() is not None


def seats_left(conn, workshop_id):
    w = workshops.get_workshop(conn, workshop_id)
    taken = conn.execute("SELECT COUNT(*) FROM sign_ups WHERE workshop_id = ? AND cancelled_at IS NULL",
                         (workshop_id,)).fetchone()[0]
    return w["seats"] - taken


def sign_up(conn, workshop_id, member_id):
    """Give the member a seat in the workshop; the same seat again if they already have one."""
    w = workshops.get_workshop(conn, workshop_id)
    if w is None:
        raise ValueError("unknown workshop")
    if not _member_exists(conn, member_id):
        raise ValueError("unknown member")
    mine = conn.execute("SELECT id FROM sign_ups WHERE workshop_id = ? AND member_id = ? AND cancelled_at IS NULL",
                        (workshop_id, member_id)).fetchone()
    if mine:
        return mine["id"]
    taken = conn.execute("SELECT COUNT(*) FROM sign_ups WHERE workshop_id = ? AND cancelled_at IS NULL",
                         (workshop_id,)).fetchone()[0]
    if taken > w["seats"]:
        raise Complet(w["title"])
    cur = conn.execute("INSERT INTO sign_ups (workshop_id, member_id, signed_up_at) VALUES (?, ?, ?)",
                       (workshop_id, member_id, _now()))
    conn.commit()
    return cur.lastrowid


def my_sign_ups(conn, member_id):
    """The workshops a member has a seat in, the soonest first."""
    return [dict(r) for r in conn.execute(
        "SELECT w.id, w.title, w.starts_at FROM sign_ups s JOIN workshops w ON w.id = s.workshop_id "
        "WHERE s.member_id = ? AND s.cancelled_at IS NULL ORDER BY w.starts_at", (member_id,))]
