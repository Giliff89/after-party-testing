import unittest

from party import app
from model import db, example_data, connect_to_db


class PartyTests(unittest.TestCase):
    """Tests for my party site."""

    def setUp(self):
        self.client = app.test_client()
        app.config['TESTING'] = True

    def test_homepage(self):
        result = self.client.get("/")
        self.assertIn("board games, rainbows, and ice cream sundaes", result.data)

    def test_no_rsvp_yet(self):
        result = self.client.get("/")
        self.assertNotIn("123 Magic Unicorn Way", result.data)

    def test_rsvp(self):
        result = self.client.post("/rsvp",
                                  data={"name": "Jane",
                                        "email": "jane@jane.com"},
                                  follow_redirects=True)
        self.assertIn("123 Magic Unicorn Way", result.data)
        self.assertNotIn("Please RSVP", result.data)


class PartyTestsDatabase(unittest.TestCase):
    """Flask tests that use the database."""

    def setUp(self):
        """Stuff to do before every test."""

        self.client = app.test_client()
        app.config['TESTING'] = True

        connect_to_db(app, "postgresql:///testdb")

        db.create_all()
        example_data()

        with self.client as c:
            with c.session_transaction() as sess:
                sess['RSVP'] = True

    def tearDown(self):
        """Do at end of every test."""

        db.session.close()
        db.drop_all()

    def test_games(self):
        result = self.client.get("/games")
        self.assertIn("A game of cats", result.data)


if __name__ == "__main__":
    unittest.main()
