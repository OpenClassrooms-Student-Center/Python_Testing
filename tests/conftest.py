"""
Shared fixtures for GüdLft test suite.

File is discovered by pytest.ini and makes its fixtures available to all test modules without
needing to explictly export.

Strategy for fixtures includes :
- Use in-memory mock data (not real JSON files) so tests are isolated, fast and never modify
the actual data
- Patch the module-level 'clubs' and 'competitions' list in server.py via monkeypatch so every
route handler uses our controlled test data (dummy data).
"""

import copy
import pytest
import server
from server import app

# ---------------------------------------------------------------------------
# Mock data — mirrors the shape of clubs.json / competitions.json
# ---------------------------------------------------------------------------

MOCK_CLUBS = [
    {"name": "PowerUP Lifting", "email": "powerup@lifting.com", "points": "24"},
    {"name": "StrongWoMen", "email": "strong_women@testemail.com", "points": "8"},
    {"name": "LiftAndBurn", "email": "liftandburn@gmail.com", "points": "19"},
]

MOCK_COMPETITIONS = [
    { "name": "Spring Festival", "date": "2026-04-28 10:00:00", "numberOfPlaces": "20"},
    { "name": "Fall / Autumn Challenges", "date": "2026-09-05 14:00:00", "numberOfPlaces": "14"},
    { "name": "SummerTime Fun", "date": "2026-08-14 16:00:00", "numberOfPlaces": "6"}
]

# ---------------------------------------------------------------------------
# Fixtures - client and server patch
# ---------------------------------------------------------------------------

@pytest.fixture
def client():
    """Return a Flask test client with TESTING mode on."""
    app.config["TESTING"] = True
    with app.test_client() as test_client:
        yield test_client

@pytest.fixture
def mock_clubs():
    """Return a mock clubs fixture."""
    return copy.deepcopy(MOCK_CLUBS)

@pytest.fixture
def mock_competitions():
    """Return a mock competitions fixture."""
    return copy.deepcopy(MOCK_COMPETITIONS)

@pytest.fixture(autouse=False)
def patch_server_data(monkeypatch, mock_clubs, mock_competitions):
    """
    Patch the module-level `clubs` and `competitions` lists that Flask routes
    read from.  Use this fixture in any test that calls a route handler.

    Usage:
        def test_something(client, patch_server_data):
            ...
    """
    monkeypatch.setattr(server, "clubs", mock_clubs)
    monkeypatch.setattr(server, "competitions", mock_competitions)
