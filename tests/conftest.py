import pytest


import server


@pytest.fixture
def client():
    app = server.create_app({"TESTING": True})
    with app.test_client() as client:
        yield client


@pytest.fixture
def past_competition():
    competition = {
        "name": "Spring Festival",
        "date": "2020-03-27 10:00:00",
        "numberOfPlaces": "25"
    }
    return competition


@pytest.fixture
def to_come_competition():
    competition = {
        "name": "Spring Festival",
        "date": "2025-03-27 10:00:00",
        "numberOfPlaces": "25"
    }
    return competition