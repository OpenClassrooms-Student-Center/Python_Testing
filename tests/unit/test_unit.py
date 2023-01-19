from unittest import TestCase
from server import app
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
        self.club = loadClubs()
        self.competition = loadCompetitions()

    def test(self):
        self.assertTrue(True)

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
