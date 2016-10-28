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
        """Tests that people not logged in cannot see party details"""
        
        result = self.client.get("/")
        self.assertNotIn("Party Details", result.data)
        self.assertIn("RSVP", result.data)

    def test_rsvp(self):
        """Test to check the correct site renders after the user rsvps"""

        result = self.client.post("/rsvp",
                                  data={"name": "Jane",
                                        "email": "jane@jane.com"},
                                        follow_redirects=True)
        self.assertIn("Party Details", result.data)
        self.assertNotIn("RSVP", result.data)



class PartyTestsDatabase(unittest.TestCase):
    """Flask tests that use the database."""

    def setUp(self):
        """Stuff to do before every test."""

        self.client = app.test_client()
        app.config['TESTING'] = True

        # Connect to test database (uncomment when testing database)
        connect_to_db(app, "postgresql:///testdb")

        # Create tables and add sample data (uncomment when testing database)
        db.create_all()
        example_data()

    def tearDown(self):
        """Do at end of every test."""

        # (uncomment when testing database)
        db.session.close()
        db.drop_all()

    def test_games(self):
        """Uses test data to check if /games shows database information"""
        result = self.client.get("/games")

        self.assertIn('balloonicorn', result.data)
        self.assertNotIn('Agricola', result.data)


if __name__ == "__main__":
    unittest.main()
