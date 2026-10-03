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
        self.chloe = members.add_member(self.conn, "Chloé", "chloe@example.org")

    def count(self, workshop_id):
        return self.conn.execute("SELECT COUNT(*) FROM sign_ups WHERE workshop_id = ?", (workshop_id,)).fetchone()[0]

    def test_a_member_gets_a_seat_and_one_seat_less_is_free(self):
        w = workshops.add_workshop(self.conn, "Raku", "2026-10-18T09:00:00+00:00", 8)
        api.sign_up(self.conn, w, self.ana)
        self.assertEqual(api.seats_left(self.conn, w), 7)

    def test_a_full_workshop_refuses_the_sign_up(self):
        w = workshops.add_workshop(self.conn, "Raku", "2026-10-18T09:00:00+00:00", 1)
        self.conn.execute("INSERT INTO sign_ups (workshop_id, member_id, signed_up_at) VALUES (?, ?, 'x')", (w, self.ana))
        self.conn.execute("INSERT INTO sign_ups (workshop_id, member_id, signed_up_at) VALUES (?, ?, 'x')", (w, self.bruno))
        with self.assertRaises(api.Complet):
            api.sign_up(self.conn, w, self.chloe)
        self.assertEqual(self.count(w), 2)

    def test_signing_up_twice_keeps_one_seat(self):
        w = workshops.add_workshop(self.conn, "Raku", "2026-10-18T09:00:00+00:00", 8)
        first = api.sign_up(self.conn, w, self.ana)
        self.assertEqual(api.sign_up(self.conn, w, self.ana), first)
        self.assertEqual(self.count(w), 1)

    def test_two_sign_ups_for_the_last_seat(self):
        w = workshops.add_workshop(self.conn, "Raku", "2026-10-18T09:00:00+00:00", 2)
        api.sign_up(self.conn, w, self.ana)
        api.sign_up(self.conn, w, self.bruno)
        self.assertEqual(api.seats_left(self.conn, w), 0)

    def test_an_unknown_workshop_or_member_is_refused(self):
        w = workshops.add_workshop(self.conn, "Raku", "2026-10-18T09:00:00+00:00", 8)
        with self.assertRaises(ValueError):
            api.sign_up(self.conn, 999, self.ana)
        with self.assertRaises(ValueError):
            api.sign_up(self.conn, w, 999)
        self.assertEqual(self.count(w), 0)

    def test_my_sign_ups_soonest_first(self):
        late = workshops.add_workshop(self.conn, "Émaillage", "2026-10-25T09:00:00+00:00", 6)
        soon = workshops.add_workshop(self.conn, "Raku", "2026-10-18T09:00:00+00:00", 8)
        api.sign_up(self.conn, late, self.ana)
        api.sign_up(self.conn, soon, self.ana)
        self.assertEqual([w["title"] for w in api.my_sign_ups(self.conn, self.ana)], ["Raku", "Émaillage"])


if __name__ == "__main__":
    unittest.main()
