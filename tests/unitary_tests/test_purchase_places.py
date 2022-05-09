"""
Testing the '/purchasePlaces' endpoint.
"""
from tests.conftest import mock_clubs_and_competitions


def test_clubs_purchase_places_working(client, mock_clubs_and_competitions):
    """
    Purchase 4 places as the Iron Temple club for the Fall Classic tournament.
    13 places in total are remaining and Iron Temple have 4 points so the purchase works.
    """
    response = client.post(
        "/purchasePlaces",
        data={"club": "Iron Temple", "competition": "Spring Boxing", "places": "4"},
    )
    data = response.data.decode()
    assert response.status_code == 200
    assert "Great-booking complete!" in data


def test_clubs_purchase_places_without_enough_points(
    client, mock_clubs_and_competitions
):
    """
    Purchase 6 places as the Iron Temple club for the Fall Classic tournament.
    13 places in total are remaining and Iron Temple have only 4 points so the purchase fails.
    """
    response = client.post(
        "/purchasePlaces",
        data={"club": "Iron Temple", "competition": "Fall Classic", "places": "6"},
    )
    data = response.data.decode()
    assert response.status_code == 200
    assert "Your club does not have enough points to participate." in data


def test_clubs_purchase_more_than_twelve_places(client, mock_clubs_and_competitions):
    response = client.post(
        "/purchasePlaces",
        data={"club": "Simply Lift", "competition": "Fall Classic", "places": "13"},
    )
    data = response.data.decode()
    assert response.status_code == 200
    assert "You cannot book more than 12 places." in data


def tests_clubs_purchase_outdated_competition(client, mock_clubs_and_competitions):
    response = client.post(
        "/purchasePlaces",
        data={"club": "Wing chun", "competition": "Fall Classic", "places": "1"},
    )
    data = response.data.decode()
    assert response.status_code == 200
    assert "Purchase not allowed - Outdated competition." in data
