import pytest

# from server import app
from server import *


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_showSummary(client):
    response = client.post("/showSummary", data=dict(email="john@simplylift.co"))
    assert b"<title>Summary | GUDLFT Registration</title>" in response.data


def test_showSummary_unknown_email(client):
    response = client.post("/showSummary", data=dict(email="test@example.com"))
    assert b"<title>GUDLFT Registration</title>" in response.data


def test_purchase_places_exceeding_points(client):
    # load the clubs and competitions data
    clubs = loadClubs()
    competitions = loadCompetitions()

    # find a club and a competition for testing
    club = next(c for c in clubs if c["name"] == "Simply Lift")
    competition = next(c for c in competitions if c["name"] == "Spring Festival")

    # count the initial number of points
    initial_points = int(club["points"])

    # try to purchase more places than the club has points
    places_required = initial_points + 1
    response = client.post(
        "/purchasePlaces",
        data=dict(
            competition=competition["name"],
            club=club["name"],
            places=places_required,
        ),
        follow_redirects=True,
    )

    # response should indicate that the purchase was not possible
    assert b"Cannot redeem more points than available" in response.data
    # TODO club's points should not have changed


def test_purchase_places_max_points(client):
    # load the clubs and competitions data
    clubs = loadClubs()
    competitions = loadCompetitions()

    # find a club and a competition for testing
    club = next(c for c in clubs if c["name"] == "Simply Lift")
    competition = next(c for c in competitions if c["name"] == "Spring Festival")

    # count the initial number of points
    initial_points = int(club["points"])
    if initial_points >= 13:
        # try to purchase more places than 12
        places_required = 13
        response = client.post(
            "/purchasePlaces",
            data=dict(
                competition=competition["name"],
                club=club["name"],
                places=places_required,
            ),
            follow_redirects=True,
        )

        # response should indicate that the purchase was not possible

        assert b"Cannot redeem more than 12 places!" in response.data


def test_purchase_places_deducts_points(client):
    # Load the clubs and competitions data
    clubs = loadClubs()
    competitions = loadCompetitions()

    # Find a club and a competition for testing
    club = next(c for c in clubs if c["name"] == "Simply Lift")
    competition = next(c for c in competitions if c["name"] == "Spring Festival")

    # Save the initial number of points and available places
    initial_points = int(club["points"])
    initial_places = int(competition["numberOfPlaces"])

    # Define the number of places to be purchased
    places_required = 5

    # Make a POST request to purchase places
    response = client.post(
        "/purchasePlaces",
        data=dict(
            competition=competition["name"],
            club=club["name"],
            places=places_required,
        ),
        follow_redirects=True,
    )

    # Assert that the response indicates a successful purchase
    if initial_points >= places_required:
        assert b"Great-booking complete!" in response.data
        clubs = loadClubs()
        competitions = loadCompetitions()

        # Retrieve the updated club and competition data
        updated_club = next(c for c in clubs if c["name"] == "Simply Lift")
        updated_competition = next(
            c for c in competitions if c["name"] == "Spring Festival"
        )

        # Assert that the club's points have been deducted
        assert int(updated_club["points"]) == initial_points - places_required

        # Assert that the competition's available places have been updated
        assert (
            int(updated_competition["numberOfPlaces"])
            == initial_places - places_required
        )


def test_display_points(client):
    # Load the clubs and competitions data
    clubs = loadClubs()
    club = next(c for c in clubs if c["name"] == "Simply Lift")
    club_points = int(club["points"])
    print(club_points)

    response = client.post(
        "/clubPoints",
        data=dict(email=clubs[1]["email"]),
        follow_redirects=True,
    )
    print(response.data)

    assert f"Simply Lift</td>\n\t\t\t\t<td>{club_points}".encode() in response.data
