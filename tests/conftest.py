import pytest

import server

# Fictitious list of competitions with their details
fake_competitions = [
    {
        "name": "Spring Festival",
        "date": "2024-03-27 10:00:00",
        "numberOfPlaces": "25",
    },
    {
        "name": "Fall Classic",
        "date": "2023-10-22 13:30:00",
        "numberOfPlaces": "13",
    },
]

# Fictitious list of clubs with their details
fake_clubs = [
    {"name": "Simply Lift", "email": "john@simplylift.co", "points": "13"},
    {"name": "Iron Temple", "email": "admin@irontemple.com", "points": "4"},
    {"name": "She Lifts", "email": "kate@shelifts.co.uk", "points": "12"},
]


@pytest.fixture
def app():
    """
    Fixture that provides a Flask application instance configured for testing.

    This fixture returns a Flask application instance with the 'TESTING'
    configuration set to True. This is useful for creating a test environment
    that can be used to simulate requests and test various aspects of the
    application.

    Returns:
        Flask: An instance of the Flask application configured for testing.
    """
    app = server.app
    app.config["TESTING"] = True
    return app


@pytest.fixture
def clubs(monkeypatch):
    """
    Fixture that patches the 'server.clubs' attribute with fake club data.

    This fixture uses the 'monkeypatch' object from Pytest to replace the
    actual 'server.clubs' with a predefined set of fake club data. This helps
    isolate the tests from the actual data and ensures consistency in test
    conditions.

    Parameters:
        - monkeypatch (pytest.MonkeyPatch): Pytest fixture for modifying
        attributes at runtime.

    Returns:
        dict: A dictionary containing the fake club data with the key 'clubs'.
    """
    monkeypatch.setattr("server.clubs", fake_clubs)
    return {"clubs": fake_clubs}


@pytest.fixture
def competitions(monkeypatch):
    """
    Fixture that patches the 'server.competitions' attribute with fake
    competition data.

    This fixture uses the 'monkeypatch' object from Pytest to replace the
    actual 'server.competitions' with a predefined set of fake competition
    data.
    This helps isolate the tests from the actual data and ensures consistency
    in test conditions.

    Parameters:
        - monkeypatch (pytest.MonkeyPatch): Pytest fixture for modifying
        attributes at runtime.

    Returns:
        dict: A dictionary containing the fake competition data with the key
        'competitions'.
    """
    monkeypatch.setattr("server.competitions", fake_competitions)
    return {"competitions": fake_competitions}
