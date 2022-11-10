from server import (COMPETITION_PLACES_SUCCESFULLY_BOOKED_MESSAGE,
                    NOT_ENOUGH_POINTS_MESSAGE, clubs, competitions)

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
            "places": club_points,
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
