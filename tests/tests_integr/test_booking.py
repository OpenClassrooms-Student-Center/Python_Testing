import pytest
from Python_Testing.tests.conftest import client
from Python_Testing import server


def test_booking_places(client):
    """tests path:
    /book/{competitions[1]['name']}/{clubs[1]['name']};
    booking of 3 places"""
    app, templates = client
    clubs = server.loadClubs()
    competitions = server.loadCompetitions()
    url = f"/book/{competitions[1]['name']}/{clubs[1]['name']}"
    rv = app.get(url, follow_redirects=True)
    assert rv.status_code == 200
    club_points_before = int(clubs[1]["points"])
    competitions_places_before = int(competitions[1]["numberOfPlaces"])
    rv = app.post(
        "/purchasePlaces",
        data=dict(club=clubs[1]["name"], competition=competitions[1]["name"], places=3),
        follow_redirects=True,
    )
    template, context = templates[1]
    data = rv.data.decode()
    assert rv.status_code == 200
    assert context["club"]["points"] == club_points_before - 3
    assert (
            context["competitions"][1]["numberOfPlaces"] == competitions_places_before - 3
    )
    assert "Great-booking complete!" in data

