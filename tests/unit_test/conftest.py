import pytest

from server import app

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def club():
    fixture = [
            {
                "name":"TEST_CLUB",
                "email":"TEST_CLUB_EMAIL",
                "points":"13"
            }
        ]
    return fixture

def competition():
    fixture = [
            {
                "name": "TEST_COMPETITION",
                "date": "2020-03-27 10:00:00",
                "numberOfPlaces": "25"
            }
        ]
    return fixture