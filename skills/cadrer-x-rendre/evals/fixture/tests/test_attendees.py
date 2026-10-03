import unittest

from clubhouse import db
from clubhouse.members import api as members
from clubhouse.signup import api, attendees, cancel
from clubhouse.workshops import api as workshops


class AttendeesTest(unittest.TestCase):
    def setUp(self):
        self.conn = db.connect()
        self.lise = members.add_member(self.conn, "Lise", "lise@example.org", role="organizer")
        self.ana = members.add_member(self.conn, "Ana", "ana@example.org")
        self.bruno = members.add_member(self.conn, "Bruno", "bruno@example.org")
        self.w = workshops.add_workshop(self.conn, "Raku", "2099-10-18T09:00:00+00:00", 8)

    def test_an_organizer_sees_each_name_and_email_first_come_first_without_the_cancelled(self):
        api.sign_up(self.conn, self.w, self.bruno)
        s = api.sign_up(self.conn, self.w, self.ana)
        api.sign_up(self.conn, self.w, self.lise)
        cancel.cancel(self.conn, s, self.ana)
        self.assertEqual(attendees.attendees(self.conn, self.w, self.lise),
                         [{"name": "Bruno", "email": "bruno@example.org"}, {"name": "Lise", "email": "lise@example.org"}])

    def test_risk_a_member_who_is_not_an_organizer_is_refused(self):
        api.sign_up(self.conn, self.w, self.ana)
        with self.assertRaises(cancel.NonAutorise):
            attendees.attendees(self.conn, self.w, self.ana)


if __name__ == "__main__":
    unittest.main()
