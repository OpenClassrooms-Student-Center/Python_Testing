import pytest
import json

from server import create_app


def loadClubs_fortest():
    with open('tests/clubs_fortest.json') as c:
         listOfClubs = json.load(c)['clubs']
         return listOfClubs


def loadCompetitions_fortest():
    with open('tests/competitions_fortest.json') as comps:
         listOfCompetitions = json.load(comps)['competitions']
         return listOfCompetitions


@pytest.fixture
def client():
    app = create_app({"TESTING": True},
                     loadCompetitions_fortest(),
                     loadClubs_fortest())
    with app.test_client() as client:
        yield client


@pytest.fixture
def non_existent_club():
    return [
        {"name": "The unknowns",
         "email": "mysteries_users@mail.com",
         "points": "15"
         }
    ]


@pytest.fixture
def non_existent_competition():
    return [
        {"name": "The non existent competition",
         "date": "2020-10-22 13:30:00",
         "numberOfPlaces": "8"
         }
    ]


@pytest.fixture
def existent_club():
    return loadClubs_fortest()


@pytest.fixture
def existent_competition():
    return loadCompetitions_fortest()

