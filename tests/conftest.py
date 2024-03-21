import pytest
from server import app


@pytest.fixture
def client():
    app.testing = True
    with app.test_client() as client:
        yield client


@pytest.fixture
def club_fixture():
    return [{"name": "nom_club", "email": "john@simplylift.co", "points": "50"}]


@pytest.fixture
def competition_fixture():
    return [
        {
            "name": "nom_competition",
            "date": "2020-10-22 13:30:00",
            "numberOfPlaces": "100",
        }
    ]
