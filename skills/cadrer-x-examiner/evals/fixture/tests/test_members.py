import unittest

from clubhouse import db
from clubhouse.members import api


class MembersTest(unittest.TestCase):
    def setUp(self):
        self.conn = db.connect()

    def test_an_email_is_kept_in_lower_case(self):
        m = api.add_member(self.conn, "Ana", "Ana@Example.org")
        self.assertEqual(api.get_member(self.conn, m)["email"], "ana@example.org")

    def test_a_bad_email_is_refused(self):
        with self.assertRaises(ValueError):
            api.add_member(self.conn, "Ana", "not-an-email")

    def test_only_an_organizer_is_an_organizer(self):
        m = api.add_member(self.conn, "Ana", "ana@example.org")
        o = api.add_member(self.conn, "Lise", "lise@example.org", role="organizer")
        self.assertFalse(api.is_organizer(self.conn, m))
        self.assertTrue(api.is_organizer(self.conn, o))


if __name__ == "__main__":
    unittest.main()
