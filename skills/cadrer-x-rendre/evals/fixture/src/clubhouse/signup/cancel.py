"""Cancelling a sign-up, up to 24 hours before the workshop starts."""
from datetime import datetime, timedelta, timezone

from clubhouse.workshops import api as workshops


class TropTard(Exception):
    """Less than 24 hours before the start: the member calls Lise."""


class NonAutorise(Exception):
    """Not the member's own sign-up."""


def cancel(conn, sign_up_id, member_id, now=None):
    now = now or datetime.now(timezone.utc)
    row = conn.execute("SELECT id, workshop_id, member_id, cancelled_at FROM sign_ups WHERE id = ?",
                       (sign_up_id,)).fetchone()
    if row is None or row["member_id"] != member_id:
        raise NonAutorise()
    if row["cancelled_at"] is not None:
        return
    starts = datetime.fromisoformat(workshops.get_workshop(conn, row["workshop_id"])["starts_at"])
    if starts - now < timedelta(hours=24):
        raise TropTard()
    conn.execute("UPDATE sign_ups SET cancelled_at = ? WHERE id = ?", (now.isoformat(), sign_up_id))
    conn.commit()
