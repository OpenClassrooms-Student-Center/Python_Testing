import html
import os
import sys

import pytest

# Obtenir le chemin du répertoire parent du répertoire actuel (dossier unit)
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, PROJECT_ROOT)

import server

# PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
# sys.path.insert(0, PROJECT_ROOT)

TEST_CLUB = {"name": "Test club", "email": "admin@admin.com", "points": "5"}

TEST_COMPETITION = {
    "name": "Test competition",
    "date": "2020-03-27 10:00:00",
    "numberOfPlaces": "10",
}


def decode_response(response_bytes):
    decoded_text = response_bytes.decode("utf-8")
    decoded_text = html.unescape(decoded_text)
    return decoded_text


@pytest.fixture
def app():
    app = server.app
    app.config["TESTING"] = True
    app.secret_key = "testing_secret_key"

    return app


def test_not_enough_points(app):
    client = app.test_client()
    response = client.post(
        "/purchasePlaces",
        data={"competition": "Test competition", "club": "Test club", "places": "10"},
        follow_redirects=True,
    )

    decoded_response = decode_response(response.data)
    assert "Sorry you can't book more than 5 places." in decoded_response


def test_points_are_deducted_after_booking(app):
    client = app.test_client()
    response = client.post(
        "/purchasePlaces",
        data={"competition": "Test competition", "club": "Test club", "places": "3"},
        follow_redirects=True,
    )

    decoded_response = decode_response(response.data)
    assert "Points available: 2" in decoded_response
