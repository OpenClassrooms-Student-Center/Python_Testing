import json

from flask.testing import FlaskClient
from flask.wrappers import Response

from ..server import loadClubs, loadCompetitions, app


class Test_PythonTesting():

    def setup_class(self):
        self.clubs = json.loads(clubs)
        self.competitions = json.loads(competitions)

    def teardown_class(self):
        pass

    def test_loadClubs(self):
        clubs = loadClubs()
        assert clubs == self.clubs
    
    def test_loadCompetitions(self):
        competitions = loadCompetitions()
        assert competitions == self.competitions

    def test_index(self):
        with app.test_client() as client:
            with app.app_context() as context:
                client: FlaskClient[Response]
                response: Response = client.get("/")
                assert response.status_code == 200


clubs = """[
    {
        "name":"Simply Lift",
        "email":"john@simplylift.co",
        "points":"13"
    },
    {
        "name":"Iron Temple",
        "email": "admin@irontemple.com",
        "points":"4"
    },
    {   "name":"She Lifts",
        "email": "kate@shelifts.co.uk",
        "points":"12"
    }
]"""

competitions = """[
    {
        "name": "Spring Festival",
        "date": "2020-03-27 10:00:00",
        "numberOfPlaces": "25"
    },
    {
        "name": "Fall Classic",
        "date": "2020-10-22 13:30:00",
        "numberOfPlaces": "13"
    }
]"""
