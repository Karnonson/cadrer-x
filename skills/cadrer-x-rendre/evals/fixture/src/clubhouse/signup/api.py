"""Sign-ups: a member's seat in a workshop. Other modules use this file only."""
from datetime import datetime, timezone

from clubhouse.members import api as members
from clubhouse.workshops import api as workshops


class Complet(Exception):
    """The workshop has no seat left."""


def _now():
    return datetime.now(timezone.utc).isoformat()


def _taken(conn, workshop_id):
    return conn.execute("SELECT COUNT(*) FROM sign_ups WHERE workshop_id = ? AND cancelled_at IS NULL",
                        (workshop_id,)).fetchone()[0]


def seats_left(conn, workshop_id):
    w = workshops.get_workshop(conn, workshop_id)
    if w is None:
        raise ValueError("unknown workshop")
    return w["seats"] - _taken(conn, workshop_id)


def sign_up(conn, workshop_id, member_id):
    """Give the member a seat in the workshop; the same seat again if they already have one."""
    w = workshops.get_workshop(conn, workshop_id)
    if w is None:
        raise ValueError("unknown workshop")
    if members.get_member(conn, member_id) is None:
        raise ValueError("unknown member")
    conn.execute("BEGIN IMMEDIATE")
    try:
        row = conn.execute("SELECT id, cancelled_at FROM sign_ups WHERE workshop_id = ? AND member_id = ?",
                           (workshop_id, member_id)).fetchone()
        if row and row["cancelled_at"] is None:
            conn.rollback()
            return row["id"]
        if _taken(conn, workshop_id) >= w["seats"]:
            raise Complet(w["title"])
        if row:
            conn.execute("UPDATE sign_ups SET cancelled_at = NULL, signed_up_at = ? WHERE id = ?", (_now(), row["id"]))
            sid = row["id"]
        else:
            sid = conn.execute("INSERT INTO sign_ups (workshop_id, member_id, signed_up_at) VALUES (?, ?, ?)",
                               (workshop_id, member_id, _now())).lastrowid
        conn.commit()
        return sid
    except Exception:
        conn.rollback()
        raise
