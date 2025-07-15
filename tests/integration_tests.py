from urllib.parse import quote
from .conftest import client


def test_full_booking_flow(client, clubs, competitions):
    # 1. Log in with a valid club email
    response = client.post('/showSummary', data={'email': 'test@club.com'})
    assert response.status_code == 200
    assert clubs[0]["email"] in response.get_data(as_text=True)

    # 2. Go to the booking page for a future competition
    competition_name = quote(competitions[0]["name"])
    club_name = quote(clubs[0]["name"])
    response = client.get(f'/book/{competition_name}/{club_name}')
    assert response.status_code == 200
    assert "How many places?" in response.get_data(as_text=True)

    # 3. Book some places
    initial_points = int(clubs[0]["points"])
    initial_places = int(competitions[0]["numberOfPlaces"])
    places_to_book = 2

    response = client.post(
        '/purchasePlaces',
        data={
            'club': clubs[0]["name"],
            'competition': competitions[0]["name"],
            'places': places_to_book
        }
    )
    assert response.status_code == 200
    assert "Great - booking complete!" in response.get_data(as_text=True)

    # 4. Check that points and competition places have been updated
    updated_points = int(clubs[0]["points"])
    updated_places = int(competitions[0]["numberOfPlaces"])
    assert updated_points == initial_points - places_to_book
    assert updated_places == initial_places - places_to_book
