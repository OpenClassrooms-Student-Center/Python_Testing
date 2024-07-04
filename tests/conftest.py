import pytest
from server import app

@pytest.fixture
def client():
    """
    Fixture to create a test client for the Flask application.
    """
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client



@pytest.fixture
def clubs():
    return [
        {
            "name": "Simply Lift",
            "email": "john@simplylift.co",
            "points": "13"
        },
        {
            "name": "Iron Temple",
            "email": "admin@irontemple.com",
            "points": "4"
        },
        {
            "name": "She Lifts",
            "email": "kate@shelifts.co.uk",
            "points": "12"
        }
    ]

@pytest.fixture
def competitions():
    return [
        {
            "name": "Spring Festival",
            "date": "2020-03-27 10:00:00",
            "numberOfPlaces": "25"
        },
        {
            "name": "Fall Classic",
            "date": "2020-10-22 13:30:00",
            "numberOfPlaces": "13"
        },
        {
            "name": "Winter Showdown",
            "date": "2024-12-05 09:00:00",
            "numberOfPlaces": "30"
        }

    ]

@pytest.fixture
def club():
    return {
        "name": "Simply Lift",
        "email": "john@simplylift.co",
        "points": "13"
    }

@pytest.fixture
def competition():
    return {
        "name": "Spring Festival",
        "date": "2020-03-27 10:00:00",
        "numberOfPlaces": "25"
    }
