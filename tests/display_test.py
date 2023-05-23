import pytest

from server import *


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_display_points_no_mail(client):
    # Load the clubs and competitions data
    clubs = loadClubs()
    club = next(c for c in clubs if c["name"] == "Simply Lift")
    club_points = int(club["points"])
    print(club_points)

    response = client.get(
        "/clubPoints",
        follow_redirects=True,
    )
    print(response.data)

    assert f"Simply Lift</td>\n\t\t\t\t<td>{club_points}".encode() in response.data



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