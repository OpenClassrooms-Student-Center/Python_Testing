from unittest import TestCase
from server import app
import server
import json
import html


def loadClubs():
    with open('clubs.json') as c:
        listOfClubs = json.load(c)['clubs']
        return listOfClubs


def loadCompetitions():
    with open('competitions.json') as comps:
        listOfCompetitions = json.load(comps)['competitions']
        return listOfCompetitions


def return_club_from_server(club_name):
    """Return the club from the clubs.json file."""
    for club in server.clubs:
        if club['name'] == club_name:
            return club


def return_competition_from_server(competition_name):
    """Return the competition from the competitions.json file."""
    for competition in server.competitions:
        if competition['name'] == competition_name:
            return competition


class Test(TestCase):

    def setUp(self):
        """Reset the 'database' before each test."""
        self.app = app.test_client()
        self.app.testing = True
        server.clubs = loadClubs()
        server.competitions = loadCompetitions()
        server.history_of_reservation = []

    def test_no_more_than_12_places_in_several_times(self):
        """Test that the user cannot book more
        than 12 places in several times."""
        payload = {
                'places': "7",
                'competition': "Spring Festival",
                'club': "Simply Lift",
                }
        with app.test_client() as client:
            res = client.post('/purchasePlaces', data=payload)

            self.assertEqual(res.status_code, 200)
            self.assertIn("Great-booking complete!",
                          res.data.decode(encoding='utf-8'))
            club = return_club_from_server('Simply Lift')
            self.assertEqual(club['points'], '6')

        payload = {
                'places': "6",
                'competition': "Spring Festival",
                'club': "Simply Lift",
                }
        with app.test_client() as client:
            res = client.post('/purchasePlaces', data=payload)

            self.assertEqual(res.status_code, 200)
            self.assertIn("You can only book 12 places per competition",
                          html.unescape(res.data.decode(encoding='utf-8')))

    def test_competition_with_no_places_cant_be_reserved_anymore(self):
        """Test that the user cannot book a competition that is full."""
        with app.test_client() as client:
            payload = {
                    'places': "12",
                    'competition': "Fall Classic",
                    'club': "Simply Lift",
                    }

            res = client.post('/purchasePlaces', data=payload)

            self.assertEqual(res.status_code, 200)
            club = return_club_from_server('Simply Lift')
            competition = return_competition_from_server('Fall Classic')
            self.assertEqual(club['points'], '1')
            self.assertEqual(competition['numberOfPlaces'], '1')
            payload = {
                    'places': "2",
                    'competition': "Fall Classic",
                    'club': "Iron Temple",
                    }

            res = client.post('/purchasePlaces', data=payload)

            self.assertEqual(res.status_code, 200)
            self.assertIn(("Sorry, you can't book for this competition as"
                           " there are no places left."), html.unescape(
                            res.data.decode(encoding='utf-8')))
