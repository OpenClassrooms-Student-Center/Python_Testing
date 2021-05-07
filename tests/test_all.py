import json

from flask.testing import FlaskClient
from flask.wrappers import Response

import pytest

from ..server import FlaskWrapper


class Test_PythonTesting():

    def setup_class(self):
        self.clubs = Test_PythonTesting.loadClubs()
        self.competitions = Test_PythonTesting.loadCompetitions()
        self.flask_wrapper = FlaskWrapper("tests/competitions.json", "tests/clubs.json")
        self.app = self.flask_wrapper.app

    def teardown_class(self):
        pass

    def test_loadClubs(self):
        assert self.flask_wrapper.clubs == self.clubs

    def test_loadCompetitions(self):
        assert self.flask_wrapper.competitions == self.loadCompetitions()

    def test_index__(self):
        with self.app.test_client() as client:
            client: FlaskClient[Response]
            response: Response = client.get("/")
            assert response.status_code == 200
            assert b"<title>GUDLFT Registration</title>" in response.data

    @pytest.mark.parametrize("email, result, page_title, errors", [
    ("admin@irontemple.com", 200, "<title>Summary | GUDLFT Registration</title>", []),
    ("something@mail.com", 200, "<title>GUDLFT Registration</title>", ["Email not found."])
    ])
    def test_showSummary(self, email, result, page_title, errors):
        with self.app.test_client() as client:
            client: FlaskClient[Response]
            response: Response = client.post("/showSummary", data={
                "email": email
            })
            assert response.status_code == result
            assert str.encode(page_title) in response.data
            assert all([str.encode(error) in response.data for error in errors])

    @pytest.mark.parametrize("competition, club, result, page_title, errors", [
        ("Spring Festival", "Iron Temple", 200, "<title>Booking for", []),
        ("Fall Classic", "She Lifts", 200, "<title>Booking for", []),
        ("Spring Festival", "none", 200, "<title>Summary | GUDLFT Registration</title>", ["Club or competition not found."]),
        ("none", "She Lifts", 200, "<title>Summary | GUDLFT Registration</title>", ["Club or competition not found."]),
        ("none", "none", 200, "<title>Summary | GUDLFT Registration</title>", ["Club or competition not found."])
    ])
    def test_book(self, competition, club, result, page_title, errors):
        with self.app.test_client() as client:
            client: FlaskClient[Response]
            response: Response = client.get("/book/"+ competition + "/" + club)
            assert response.status_code == result
            assert str.encode(page_title) in response.data
            assert all([str.encode(error) in response.data for error in errors])

    @pytest.mark.parametrize("competition, club, places_required, result, page_title, errors, points", [
        ("Spring Festival", "Iron Temple", 4, 200, "<title>Summary | GUDLFT Registration</title>", [], "Points available: 0"),
        ("Fall Classic", "Simply Lift", 5, 200, "<title>Booking for", ["Club has not enough points."], ""),
        ("New Horizons", "She Lifts", 4, 200, "<title>Booking for", ["Competition has not enough places."], ""),
    ])
    def test_purchasePlaces(self, competition, club, places_required, result, page_title, errors, points):
        with self.app.test_client() as client:
            client: FlaskClient[Response]
            response: Response = client.post("/purchasePlaces", data={
                "competition": competition,
                "club": club,
                "places": places_required
            })
            assert response.status_code == result
            assert str.encode(page_title) in response.data
            assert all([str.encode(error) in response.data for error in errors])
            if len(errors) == 0:
                assert str.encode(points) in response.data

    def test_logout(self):
        with self.app.test_client() as client:
            client: FlaskClient[Response]
            response: Response = client.get("/logout")
            assert response.status_code == 302
    
    @staticmethod
    def loadClubs():
        with open("tests/clubs.json") as c:
            listOfClubs = json.load(c)['clubs']
            return listOfClubs

    @staticmethod
    def loadCompetitions():
        with open("tests/competitions.json") as comps:
            listOfCompetitions = json.load(comps)['competitions']
            return listOfCompetitions
