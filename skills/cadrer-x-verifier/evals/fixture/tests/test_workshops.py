import unittest

from clubhouse import db
from clubhouse.workshops import api


class WorkshopsTest(unittest.TestCase):
    def setUp(self):
        self.conn = db.connect()

    def test_a_workshop_keeps_its_title_and_seats(self):
        w = api.add_workshop(self.conn, "  Raku firing ", "2026-10-18T09:00:00+00:00", 8)
        self.assertEqual(api.get_workshop(self.conn, w)["title"], "Raku firing")
        self.assertEqual(api.get_workshop(self.conn, w)["seats"], 8)

    def test_a_workshop_needs_at_least_one_seat(self):
        with self.assertRaises(ValueError):
            api.add_workshop(self.conn, "Glazing", "2026-10-20T09:00:00+00:00", 0)

    def test_the_soonest_workshop_comes_first(self):
        api.add_workshop(self.conn, "Glazing", "2026-10-25T09:00:00+00:00", 6)
        api.add_workshop(self.conn, "Raku firing", "2026-10-18T09:00:00+00:00", 8)
        self.assertEqual([w["title"] for w in api.list_workshops(self.conn)], ["Raku firing", "Glazing"])


if __name__ == "__main__":
    unittest.main()
