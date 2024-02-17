import pytest
import server

# from server import app, clubs, competitions
from flask import url_for
from datetime import datetime, timedelta


# Utilisez les fixtures définies dans conftest.py
@pytest.mark.usefixtures("client", "clubs", "competitions")
def test_purchase_places_success(client, monkeypatch, clubs, competitions):
    """
    GIVEN a club with sufficient points and available places in the competition
    WHEN the '/purchasePlaces' endpoint is called with valid input
    THEN check that the booking is successful and club points and competition places are updated
    """

    # GIVEN: Mock the get_club function
    def patch_get_club(dummy):
        """Mock get_club() function"""
        return {"name": "Simply Lift", "points": 13}

    monkeypatch.setattr(server, "get_club", patch_get_club)
    monkeypatch.setattr(server, "competitions", competitions)
    monkeypatch.setattr(server, "clubs", clubs)

    # WHEN: Make the request to the '/purchasePlaces' endpoint with valid input
    response = client.post(
        "/purchasePlaces",
        data={"competition": "Spring Festival", "club": "Simply Lift", "places": "5"},
        follow_redirects=True,
    )

    # THEN: Check response
    assert b"Great-booking complete!" in response.data
    assert clubs[0]["points"] == 8  # Club points updated
    assert competitions[0]["numberOfPlaces"] == 20  # Competition places updated


def test_purchase_places_insufficient_points(client, monkeypatch, clubs, competitions):
    """
    GIVEN a club with insufficient points
    WHEN the '/purchasePlaces' endpoint is called
    THEN check that an error message is displayed and club points and competition places remain unchanged
    """

    # Mock the get_club function
    def patch_get_club(dummy):
        """Mock get_club() function"""
        return {"name": "Simply Lift", "points": 13}

    monkeypatch.setattr(server, "get_club", patch_get_club)
    monkeypatch.setattr(server, "competitions", competitions)
    monkeypatch.setattr(server, "clubs", clubs)

    # Make the request to the '/purchasePlaces' endpoint
    response = client.post(
        "/purchasePlaces",
        data={"competition": "Spring Festival", "club": "Simply Lift", "places": "10"},
        follow_redirects=True,
    )

    # THEN: Check response
    assert b"<li>You don't have enough points.</li>"


def test_purchase_places_insufficient_places(client, monkeypatch, clubs, competitions):
    """
    GIVEN a competition with insufficient places
    WHEN the '/purchasePlaces' endpoint is called
    THEN check that an error message is displayed and club points and competition places remain unchanged
    """

    # Mock the get_club function
    def patch_get_club(dummy):
        """Mock get_club() function"""
        return {"name": "Simply Lift", "points": 13}

    monkeypatch.setattr(server, "get_club", patch_get_club)
    monkeypatch.setattr(server, "competitions", competitions)
    monkeypatch.setattr(server, "clubs", clubs)

    # Make the request to the '/purchasePlaces' endpoint
    response = client.post(
        "/purchasePlaces",
        data={"competition": "Spring Festival", "club": "Simply Lift", "places": "30"},
        follow_redirects=True,
    )

    # THEN: Check response
    assert b"<li>Not enough places available, you are trying to book more than the remaining places.</li>"


def test_purchase_places_invalid_input(client, monkeypatch, clubs, competitions):
    """
    GIVEN invalid input
    WHEN the '/purchasePlaces' endpoint is called
    THEN check that an error message is displayed and club points and competition places remain unchanged
    """

    # Mock the get_club function
    def patch_get_club(dummy):
        """Mock get_club() function"""
        return {"name": "Simply Lift", "points": 13}

    monkeypatch.setattr(server, "get_club", patch_get_club)
    monkeypatch.setattr(server, "competitions", competitions)
    monkeypatch.setattr(server, "clubs", clubs)

    # Make the request to the '/purchasePlaces' endpoint
    response = client.post(
        "/purchasePlaces",
        data={
            "competition": "Spring Festival",
            "club": "Simply Lift",
            "places": "invalid",
        },
        follow_redirects=True,
    )

    # THEN: Check response
    assert b"<li>Please enter a number between 0 and 12.</li>"
