from server import (COMPETITION_PLACES_SUCCESFULLY_BOOKED_MESSAGE,
                    NOT_ENOUGH_POINTS_MESSAGE, UNABLE_TO_BOOK_MORE_THAN_12_PLACES_MESSAGE,
                    PAST_COMPETITION_ERROR_MESSAGE,
                    clubs,
                    competitions)

club_name = clubs[0]["name"]
club_email = clubs[0]["email"]
club_points = int(clubs[0]["points"])
competition_name = competitions[0]["name"]


# Login tests
def test_login_with_valid_email(client):
    response = client.post("/showSummary", data={"email": club_email})
    data = response.data.decode()
    assert "Welcome" in data


def test_login_with_wrong_email(client):
    response = client.post("/showSummary", data={"email": "wrong.email@test.com"})
    data = response.data.decode()
    assert "Email not found" in data


# Booking tests
def test_book_competition_places_with_enough_amount_of_points(client):
    response = client.post(
        "/purchasePlaces",
        data={
            "competition": competition_name,
            "club": club_name,
            "places": 1,
        },
    )

    data = response.data.decode()
    assert COMPETITION_PLACES_SUCCESFULLY_BOOKED_MESSAGE in data


def test_book_competition_places_with_not_enough_points(client):
    wrong_amount_of_points = club_points + 1

    response = client.post(
        "/purchasePlaces",
        data={
            "competition": competitions[0]["name"],
            "club": clubs[0]["name"],
            "places": wrong_amount_of_points,
        },
    )

    data = response.data.decode()
    assert NOT_ENOUGH_POINTS_MESSAGE in data


def test_book_12_places_or_less(client):
    response = client.post(
        "/purchasePlaces",
        data={
            "competition": competition_name,
            "club": club_name,
            "places": 12,
        },
    )

    data = response.data.decode()
    assert COMPETITION_PLACES_SUCCESFULLY_BOOKED_MESSAGE in data


def test_book_more_than_12_places(client):
    response = client.post(
        "/purchasePlaces",
        data={
            "competition": competition_name,
            "club": club_name,
            "places": 13,
        },
    )

    data = response.data.decode()
    assert UNABLE_TO_BOOK_MORE_THAN_12_PLACES_MESSAGE in data


def test_able_to_book_upcoming_competition(client):
    response = client.get(f"/book/{competition_name}/{club_name}")
    data = response.data.decode()
    assert "How many places?" in data


def test_unable_to_book_past_competition(client):
    response = client.get(f"/book/{competitions[1]['name']}/{clubs[1]['name']}")
    data = response.data.decode()
    assert PAST_COMPETITION_ERROR_MESSAGE in data
