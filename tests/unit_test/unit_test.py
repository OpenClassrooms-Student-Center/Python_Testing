# unit_test.py
# created 19/01/2021 at 12:50 by Antoine 'AatroXiss' BEAUDESSON
# last modified 19/01/2021 at 12:50 by Antoine 'AatroXiss' BEAUDESSON

""" unit_test.py

To do:
    - implement all unit tests
    - *
"""

__author__ = "Antoine 'AatroXiss' BEAUDESSON"
__copyright__ = "Copyright 2021, Antoine 'AatroXiss' BEAUDESSON"
__credits__ = ["Antoine 'AatroXiss' BEAUDESSON"]
__license__ = ""
__version__ = "0.0.1"
__maintainer__ = "Antoine 'AatroXiss' BEAUDESSON"
__email__ = "antoine.beaudesson@gmail.com"
__status__ = "Development"

# standard library imports

# third party imports

# local application imports
import server

# other imports

# constants
NUMBER_OF_CLUBS = 3
NUMBER_OF_COMPETITIONS = 2
WRONG_EMAIL = "wrong@gmail.com"
EMPTY_EMAIL = ""


class TestDatabases():

    def test_load_clubs(self):
        """
        Test that the clubs.json file is loaded correctly
        we know that the file is loaded correctly because
        listOfClubs has the same number of clubs as the
        clubs.json file"""

        listOfClubs = server.loadClubs()
        assert len(listOfClubs) == NUMBER_OF_CLUBS

    def test_load_competitions(self):
        """
        Test that the competitions.json file is loaded correctly
        we know that the file is loaded correctly because
        listOfCompetitions has the same number of competitions as the
        competitions.json file"""

        listOfCompetitions = server.loadCompetitions()
        assert len(listOfCompetitions) == NUMBER_OF_COMPETITIONS


class TestIndex():

    # Happy paths => hp / Sad paths => sp

    def test_status_code_200_template(self, client):
        """
        Test that the page is loaded correctly.
        we know that because the page has the status code 200.
        We also know that the page has the right template because
        the title of the page is GUDLFT Registration"""

        response = client.get('/')
        assert response.status_code == 200
        assert ("GUDLFT Registration") in response.data.decode()

    def test_hp_registered_user_login(self, client):
        """
        Test where a user logs in with a registered email.
        We know the user has successfully logged in because
        the status code is 200 and the page has the right template
        We know that the template is correct because the welcome message
        is displayed with the user's email"""

        email = server.loadClubs()[0]['email']
        response = client.post('/showSummary', data={'email': email})
        assert response.status_code == 200
        assert ("Welcome, " + email) in response.data.decode()

    def test_sp_unregistered_user_login(self, client):
        """
        Test where a user logs in with an unregistered email.
        We know the user has successfully not logged in because
        the status code is 200 and the page has the right template
        We know that the template is correct because the error message
        is displayed
        """
        email = WRONG_EMAIL
        response = client.post('/showSummary', data={'email': email})
        assert response.status_code == 200
        assert ("Error: email is not registered") in response.data.decode()

    def test_sp_no_email_user_login(self, client):
        """
        Test where a user logs in with no email.
        We know the user has successfully not logged in because
        the status code is 200 and the page has the right template
        We know that the template is correct because the error message
        is displayed
        """
        email = EMPTY_EMAIL
        response = client.post('/showSummary', data={'email': email})
        assert response.status_code == 200
        assert ("Error: field is empty") in response.data.decode()
