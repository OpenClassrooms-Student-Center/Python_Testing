from unittest import TestCase
from server import app
import server
import json


def loadClubs():
    with open('clubs.json') as c:
        listOfClubs = json.load(c)['clubs']
        return listOfClubs


def loadCompetitions():
    with open('competitions.json') as comps:
        listOfCompetitions = json.load(comps)['competitions']
        return listOfCompetitions


class Test(TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
        server.clubs = loadClubs()
        server.competitions = loadCompetitions()

    def test_load_clubs(self):
        club = loadClubs()
        self.assertEqual(club,
                         [{'name': 'Simply Lift', 'email':
                           'john@simplylift.co', 'points': '13'},
                          {'name': 'Iron Temple', 'email':
                           'admin@irontemple.com', 'points': '4'},
                          {'name': 'She Lifts', 'email': 'kate@shelifts.co.uk',
                           'points': '12'}])

    def test_load_competitions(self):
        competition = loadCompetitions()
        self.assertEqual(competition,
                         [{'name': 'Spring Festival', 'date':
                           '2020-03-27 10:00:00', 'numberOfPlaces': '25'},
                          {'name': 'Fall Classic', 'date':
                           '2020-10-22 13:30:00', 'numberOfPlaces': '13'}])

    def test_server_is_running(self):
        with app.test_client() as client:
            response = client.get('/')
            self.assertEqual(response.status_code, 200)

    def test_show_summary_bad_email(self):
        payload = {
                'email': 'hello@example.com',
                }
        with app.test_client() as client:
            res = client.post('/showSummary', data=payload)

            self.assertEqual(res.status_code, 200)
            self.assertIn("Sorry, that email wasn&#39;t found.",
                          res.data.decode(encoding='utf-8'))

    def test_show_summary_good_email(self):
        payload = {
                'email': "kate@shelifts.co.uk",
                }
        with app.test_client() as client:
            res = client.post('/showSummary', data=payload)

            self.assertEqual(res.status_code, 200)
            self.assertIn("kate@shelifts.co.uk",
                          res.data.decode(encoding='utf-8'))

    def test_cannot_book_more_places_than_user_have(self):
        """Test that the user cannot spend more points than they have."""
        payload = {
                'places': "13",
                'competition': "Spring Festival",
                'club': "She Lifts",
                }
        with app.test_client() as client:
            res = client.post('/purchasePlaces', data=payload)

            self.assertEqual(res.status_code, 200)
            self.assertIn("You don&#39;t have enough points to book 13 places",
                          res.data.decode(encoding='utf-8'))

    def test_can_book_places(self):
        """Test that the user can spend points."""
        payload = {
                'places': "4",
                'competition': "Spring Festival",
                'club': "She Lifts",
                }
        with app.test_client() as client:
            res = client.post('/purchasePlaces', data=payload)

            self.assertEqual(res.status_code, 200)
            self.assertIn("Great-booking complete!",
                          res.data.decode(encoding='utf-8'))

    def test_point_are_correctly_deducted(self):
        """Test that the user can spend points."""
        payload = {
                'places': "4",
                'competition': "Spring Festival",
                'club': "She Lifts",
                }
        with app.test_client() as client:
            res = client.post('/purchasePlaces', data=payload)

            self.assertEqual(res.status_code, 200)
            self.assertIn("Points available: 8",
                          res.data.decode(encoding='utf-8'))
