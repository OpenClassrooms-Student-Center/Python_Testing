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

    def test_load_clubs(self):
        """Test that the clubs are loaded from the JSON file."""
        club = loadClubs()
        self.assertEqual(club,
                         [{'name': 'Simply Lift', 'email':
                           'john@simplylift.co', 'points': '13'},
                          {'name': 'Iron Temple', 'email':
                           'admin@irontemple.com', 'points': '4'},
                          {'name': 'She Lifts', 'email': 'kate@shelifts.co.uk',
                           'points': '12'}])

    def test_load_competitions(self):
        """Test that the competitions are loaded from the JSON file."""
        competition = loadCompetitions()
        self.assertEqual(competition,
                         [{'name': 'Spring Festival', 'date':
                           '2020-03-27 10:00:00', 'numberOfPlaces': '25'},
                          {'name': 'Fall Classic', 'date':
                           '2020-10-22 13:30:00', 'numberOfPlaces': '13'}])

    def test_server_is_running(self):
        """Test that the server is running."""
        with app.test_client() as client:
            response = client.get('/')
            self.assertEqual(response.status_code, 200)

    def test_show_summary_bad_email(self):
        """Test that the user is redirected to the index page if the email
        is not found."""
        payload = {
                'email': 'hello@example.com',
                }
        with app.test_client() as client:
            res = client.post('/showSummary', data=payload)

            self.assertEqual(res.status_code, 200)
            self.assertIn("Sorry, that email wasn't found.",
                          html.unescape(res.data.decode(encoding='utf-8')))

    def test_show_summary_good_email(self):
        """Test that the user is redirected to the summary page if the email
        is found."""
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
            self.assertIn("You don't have enough points to book 13 places",
                          html.unescape(res.data.decode(encoding='utf-8')))

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
            club = return_club_from_server('She Lifts')
            self.assertEqual(club['points'], '8')

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
            club = return_club_from_server('She Lifts')
            self.assertEqual(club['points'], '8')

    def test_not_able_to_take_more_than_12_places_per_competition(self):
        """Test that the user cannot book more
        than 12 places per competition."""
        payload = {
                'places': "13",
                'competition': "Spring Festival",
                'club': "Simply Lift",
                }
        with app.test_client() as client:
            res = client.post('/purchasePlaces', data=payload)

            self.assertEqual(res.status_code, 200)
            self.assertIn("You can only book 12 places per competition",
                          html.unescape(res.data.decode(encoding='utf-8')))
            club = return_club_from_server('Simply Lift')
            self.assertEqual(club['points'], '13')

    def test_competition_in_the_past_cant_be_reserved_anymore(self):
        """Test that the user cannot book a competition that is in the past."""
        with app.test_client() as client:
            res = client.get('/book/Fall Classic/Simply Lift')

            self.assertEqual(res.status_code, 200)
            self.assertIn(("Sorry, you can't book for this competition as the"
                           " date has passed."),
                          html.unescape(res.data.decode(encoding='utf-8')))
            club = return_club_from_server('Simply Lift')
            self.assertEqual(club['points'], '13')

    def test_competition_in_the_past_cant_be_reserved(self):
        """Test gui doesn't show links anymore."""
        payload = {
                'email': "kate@shelifts.co.uk",
                }
        with app.test_client() as client:
            res = client.post('/showSummary', data=payload)

            self.assertEqual(res.status_code, 200)
            self.assertEqual(res.data.decode(encoding='utf-8').count("<a"), 1)

    def test_display_points_board(self):
        """Test that the points board is displayed."""
        payload = {
                'email': "kate@shelifts.co.uk",
                }
        with app.test_client() as client:
            res = client.post('/showSummary', data=payload)

            self.assertEqual(res.status_code, 200)
            self.assertIn("Points Board",
                          html.unescape(res.data.decode(encoding='utf-8')))
