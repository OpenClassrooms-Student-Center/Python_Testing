from urllib.parse import quote

from server import load_clubs, load_competitions


def test_show_summary_function(client, valid_club):
    response = client.post('/showSummary', data=valid_club)
    assert response.status_code == 200


def test_book_function(client, valid_club, past_competition):
    competition_name = quote(past_competition["name"])
    club_name = quote(valid_club["name"])
    response = client.get(f'/book/{competition_name}/{club_name}')
    assert response.status_code == 200


def test_load_clubs_function():
    clubs = load_clubs()
    assert clubs is not None
    assert isinstance(clubs, list)
    assert len(clubs) > 0


def test_load_competitions_function():
    competitions = load_competitions()
    assert competitions is not None
    assert isinstance(competitions, list)
    assert len(competitions) > 0


def test_no_places_during_book(client, next_competition, valid_club):
    no_places = ""
    data = {
        "club": valid_club["name"],
        "competition": next_competition["name"],
        "places": no_places
    }
    response = client.post('/purchasePlaces', data=data)
    message = response.data.decode()
    assert response.status_code == 200
    assert "You did not send a number of places" in message


def test_positif_points(client, next_competition, valid_club):
    places_deducted = -5
    data = {
        "club": valid_club["name"],
        "competition": next_competition["name"],
        "places": places_deducted
    }
    response = client.post('/purchasePlaces', data=data)
    message = response.data.decode()
    assert response.status_code == 200
    assert "Please choice a positif number of places" in message


def test_points_greater_than_places(client, next_competition, valid_club):
    places_required = 5
    data = {
        "club": valid_club["name"],
        "competition": next_competition["name"],
        "places": places_required
    }
    response = client.post('/purchasePlaces', data=data)
    message = response.data.decode()
    assert response.status_code == 200
    assert "You do not have enough points" in message


def test_points_correctly_deducted(client, next_competition, valid_club):
    places_deducted = 2
    data = {
        "club": valid_club["name"],
        "competition": next_competition["name"],
        "places": places_deducted
    }
    points_available = int(valid_club["points"]) - places_deducted
    response = client.post('/purchasePlaces', data=data)
    message = response.data.decode()
    assert response.status_code == 200
    assert "Great-booking complete" in message
    assert f"Points available: {points_available}" in message


def test_booking_max_places(client, next_competition, valid_club):
    places_required = 13
    data = {
        "club": valid_club["name"],
        "competition": next_competition["name"],
        "places": places_required
    }
    response = client.post('/purchasePlaces', data=data)
    message = response.data.decode()
    assert response.status_code == 200
    assert "You cannot book more than 12 places" in message


def test_no_booking_past_competitions(client, past_competition, valid_club):
    places_required = 2
    data = {
        "club": valid_club["name"],
        "competition": past_competition["name"],
        "places": places_required
    }
    response = client.post('/purchasePlaces', data=data)
    message = response.data.decode()
    assert response.status_code == 200
    assert "Competition is already finished. Please book another competition" in message


# def test_booking_next_competitions(client, next_competition, valid_club):
#     places_required = 2
#     data = {
#         "club": valid_club["name"],
#         "competition": next_competition["name"],
#         "places": places_required
#     }
#     response = client.post('/purchasePlaces', data=data)
#     message = response.data.decode()
#     assert response.status_code == 200
#     assert "Great-booking complete" in message
