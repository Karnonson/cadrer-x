import os
import sqlite3
import tempfile
import threading
import unittest

from clubhouse import db
from clubhouse.members import api as members
from clubhouse.signup import api
from clubhouse.workshops import api as workshops


class SignUpTest(unittest.TestCase):
    def setUp(self):
        self.conn = db.connect()
        self.ana = members.add_member(self.conn, "Ana", "ana@example.org")
        self.bruno = members.add_member(self.conn, "Bruno", "bruno@example.org")

    def count(self, w):
        return self.conn.execute("SELECT COUNT(*) FROM sign_ups WHERE workshop_id = ?", (w,)).fetchone()[0]

    def test_a_member_gets_a_seat_and_one_seat_less_is_free(self):
        w = workshops.add_workshop(self.conn, "Raku", "2026-10-18T09:00:00+00:00", 8)
        api.sign_up(self.conn, w, self.ana)
        self.assertEqual(api.seats_left(self.conn, w), 7)

    def test_a_full_workshop_refuses_the_sign_up(self):
        w = workshops.add_workshop(self.conn, "Raku", "2026-10-18T09:00:00+00:00", 1)
        api.sign_up(self.conn, w, self.ana)
        with self.assertRaises(api.Complet):
            api.sign_up(self.conn, w, self.bruno)
        self.assertEqual(api.seats_left(self.conn, w), 0)
        self.assertEqual(self.count(w), 1)

    def test_signing_up_twice_keeps_one_seat(self):
        w = workshops.add_workshop(self.conn, "Raku", "2026-10-18T09:00:00+00:00", 8)
        first = api.sign_up(self.conn, w, self.ana)
        self.assertEqual(api.sign_up(self.conn, w, self.ana), first)
        self.assertEqual(self.count(w), 1)

    def test_risk_two_sign_ups_at_once_for_the_last_seat(self):
        path = os.path.join(tempfile.mkdtemp(), "club.db")
        conn = db.connect(path)
        w = workshops.add_workshop(conn, "Raku", "2026-10-18T09:00:00+00:00", 1)
        a = members.add_member(conn, "Ana", "ana@example.org")
        b = members.add_member(conn, "Bruno", "bruno@example.org")
        results, barrier = [], threading.Barrier(2)

        def go(member):
            c = sqlite3.connect(path, timeout=5, isolation_level=None)
            c.row_factory = sqlite3.Row
            barrier.wait()
            try:
                api.sign_up(c, w, member)
                results.append("ok")
            except api.Complet:
                results.append("complet")

        ts = [threading.Thread(target=go, args=(m,)) for m in (a, b)]
        [t.start() for t in ts]
        [t.join() for t in ts]
        self.assertEqual(sorted(results), ["complet", "ok"])
        self.assertEqual(api.seats_left(conn, w), 0)

    def test_risk_an_unknown_workshop_or_member_is_refused(self):
        w = workshops.add_workshop(self.conn, "Raku", "2026-10-18T09:00:00+00:00", 8)
        with self.assertRaises(ValueError):
            api.sign_up(self.conn, 999, self.ana)
        with self.assertRaises(ValueError):
            api.sign_up(self.conn, w, 999)
        self.assertEqual(self.count(w), 0)


if __name__ == "__main__":
    unittest.main()
