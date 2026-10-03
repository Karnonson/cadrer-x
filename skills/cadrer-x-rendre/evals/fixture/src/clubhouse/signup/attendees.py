"""The list of who is coming to a workshop, for organizers only."""
from clubhouse.members import api as members

from .cancel import NonAutorise


def attendees(conn, workshop_id, asked_by):
    if not members.is_organizer(conn, asked_by):
        raise NonAutorise()
    rows = conn.execute("SELECT member_id FROM sign_ups WHERE workshop_id = ? AND cancelled_at IS NULL "
                        "ORDER BY signed_up_at, id", (workshop_id,)).fetchall()
    out = []
    for r in rows:
        m = members.get_member(conn, r["member_id"])
        out.append({"name": m["name"], "email": m["email"]})
    return out
