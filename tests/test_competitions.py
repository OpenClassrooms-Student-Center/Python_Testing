import pytest
import server

client = server.app.test_client()


@pytest.fixture
def clubs():
    yield server.clubs


@pytest.fixture
def competitions():
    yield server.competitions


def test_club_can_afford_place(clubs, competitions):
    response = client.post(
        "/purchasePlaces",
        data={
            "places": "3",
            "club": clubs[1]["name"],
            "competition": competitions[0]["name"],
        },
    )
    assert response.status_code == 200
    assert b"Great-booking complete!" in response.data


def test_club_cannot_afford_place(clubs, competitions):
    response = client.post(
        "/purchasePlaces",
        data={
            "places": "5",
            "club": clubs[1]["name"],
            "competition": competitions[0]["name"],
        },
    )
    assert response.status_code == 200
    assert b"your club does not have enough points to affords this." in response.data


def test_club_cannot_book_more_than_12_places(clubs, competitions):
    response = client.post(
        "/purchasePlaces",
        data={
            "places": "13",
            "club": clubs[1]["name"],
            "competition": competitions[0]["name"],
        },
    )
    assert response.status_code == 200
    assert b"You cannot reserve more than 12 places" in response.data
