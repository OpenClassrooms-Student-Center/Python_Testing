import html
import os
import sys

import pytest

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, PROJECT_ROOT)

import server

TEST_CLUB = {"name": "Test club", "email": "admin@admin.com", "points": "5"}

TEST_COMPETITION_OVER = {
    "name": "Test competition",
    "date": "2020-03-27 10:00:00",
    "numberOfPlaces": "10",
}

TEST_COMPETITION_GOING = {
    "name": "Test competition going",
    "date": "2026-03-27 10:00:00",
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


def test_book_competition_over(app):
    client = app.test_client()
    response = client.get(
        f"/book/{TEST_COMPETITION_OVER['name']}/{TEST_CLUB['name']}",
        follow_redirects=True,
    )

    decoded_response = decode_response(response.data)

    assert (
        "Sorry, this competition is over, places are not available anymore."
        in decoded_response
    )


def test_book_competition_going(app):
    client = app.test_client()
    response = client.get(
        f"/book/{TEST_COMPETITION_GOING['name']}/{TEST_CLUB['name']}",
        follow_redirects=True,
    )

    decoded_response = decode_response(response.data)

    assert (
        f"This competition is open until {TEST_COMPETITION_GOING['date']}."
        in decoded_response
    )
