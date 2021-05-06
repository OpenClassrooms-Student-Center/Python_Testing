import json

from flask.testing import FlaskClient
from flask.wrappers import Response

import pytest

from ..server import app, loadClubs, loadCompetitions


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

    def test_index__(self):
        with app.test_client() as client:
            with app.app_context() as context:
                client: FlaskClient[Response]
                response: Response = client.get("/")
                assert response.status_code == 200
                assert b"<title>GUDLFT Registration</title>" in response.data

    @pytest.mark.parametrize("email, result, page_title, errors", [
    ("admin@irontemple.com", 200, "<title>Summary | GUDLFT Registration</title>", []),
    ("something@mail.com", 200, "<title>GUDLFT Registration</title>", ["Email not found."])
    ])
    def test_showSummary(self, email, result, page_title, errors):
        with app.test_client() as client:
            client: FlaskClient[Response]
            response: Response = client.post("/showSummary", data={
                "email": email
            })
            assert response.status_code == result
            assert str.encode(page_title) in response.data
            assert [str.encode(club["email"]) for club in self.clubs if club["email"] == email][0] in response.data
            for error in errors:
                print(error)
                assert str.encode(error) in response.data

    @pytest.mark.parametrize("competition, club, result, page_title", [
        ("Spring Festival", "Iron Temple", 200, "<title>Booking for"),
        ("Fall Classic", "She Lifts", 200, "<title>Booking for"),
        ("Spring Festival", "none", 400, "<title>Summary | GUDLFT Registration</title>"),
        ("none", "She Lifts", 400, "<title>Summary | GUDLFT Registration</title>"),
        ("none", "none", 400, "<title>Summary | GUDLFT Registration</title>")
    ])
    def test_book(self, competition, club, result, page_title):
        with app.test_client() as client:
            client: FlaskClient[Response]
            response: Response = client.get("/book/"+ competition + "/" + club)
            assert response.status_code == result
            assert str.encode(page_title) in response.data

    @pytest.mark.parametrize("competition, club, places, result, page_title", [
        ("Spring Festival", "Iron Temple", 1, 200, "<title>Summary | GUDLFT Registration</title>"),
        ("Fall Classic", "She Lifts", 1, 200, "<title>Summary | GUDLFT Registration</title>"),
    ])
    def test_purchasePlaces(self, competition, club, places, result, page_title):
        with app.test_client() as client:
            client: FlaskClient[Response]
            response: Response = client.post("/purchasePlaces", data={
                "competition": competition,
                "club": club,
                "places": places
            })
            assert response.status_code == result
            assert str.encode(page_title) in response.data

    def test_logout(self):
        with app.test_client() as client:
            client: FlaskClient[Response]
            response: Response = client.get("/logout")
            assert response.status_code == 302


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
