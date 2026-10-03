import unittest
from datetime import datetime, timezone

from clubhouse import db
from clubhouse.members import api as members
from clubhouse.signup import api, cancel
from clubhouse.workshops import api as workshops

NOW = datetime(2026, 10, 15, 9, 0, tzinfo=timezone.utc)


class CancelTest(unittest.TestCase):
    def setUp(self):
        self.conn = db.connect()
        self.ana = members.add_member(self.conn, "Ana", "ana@example.org")
        self.bruno = members.add_member(self.conn, "Bruno", "bruno@example.org")

    def test_three_days_before_the_seat_is_free_again(self):
        w = workshops.add_workshop(self.conn, "Raku", "2026-10-18T09:00:00+00:00", 1)
        s = api.sign_up(self.conn, w, self.ana)
        cancel.cancel(self.conn, s, self.ana, now=NOW)
        self.assertEqual(api.seats_left(self.conn, w), 1)

    def test_the_day_before_it_is_too_late(self):
        w = workshops.add_workshop(self.conn, "Raku", "2026-10-16T08:00:00+00:00", 1)
        s = api.sign_up(self.conn, w, self.ana)
        with self.assertRaises(cancel.TropTard):
            cancel.cancel(self.conn, s, self.ana, now=NOW)
        self.assertEqual(api.seats_left(self.conn, w), 0)

    def test_exactly_24_hours_before_is_still_allowed(self):
        w = workshops.add_workshop(self.conn, "Raku", "2026-10-16T09:00:00+00:00", 1)
        s = api.sign_up(self.conn, w, self.ana)
        cancel.cancel(self.conn, s, self.ana, now=NOW)
        self.assertEqual(api.seats_left(self.conn, w), 1)

    def test_risk_another_members_sign_up_cannot_be_cancelled(self):
        w = workshops.add_workshop(self.conn, "Raku", "2026-10-18T09:00:00+00:00", 1)
        s = api.sign_up(self.conn, w, self.ana)
        with self.assertRaises(cancel.NonAutorise):
            cancel.cancel(self.conn, s, self.bruno, now=NOW)
        self.assertEqual(api.seats_left(self.conn, w), 0)

    def test_signing_up_again_after_cancelling(self):
        w = workshops.add_workshop(self.conn, "Raku", "2026-10-18T09:00:00+00:00", 1)
        s = api.sign_up(self.conn, w, self.ana)
        cancel.cancel(self.conn, s, self.ana, now=NOW)
        api.sign_up(self.conn, w, self.ana)
        self.assertEqual(api.seats_left(self.conn, w), 0)


if __name__ == "__main__":
    unittest.main()
