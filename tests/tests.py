from urllib.parse import quote

from .conftest import client
from bs4 import BeautifulSoup


def test_show_summary_with_mock_data(client, clubs, competitions):
    response = client.post('/showSummary', data={'email': 'test@club.com'})
    assert response.status_code == 200
    soup = BeautifulSoup(response.data, 'html.parser')

    assert "test@club.com" in soup.text


def test_book_more_than_12_tickets(client, clubs, competitions):
    response = client.post(
        '/purchasePlaces',
        data={
            'club': clubs[0].get("name"),
            'competition': competitions[0].get("name"),
            'places': 13})

    assert response.status_code == 200
    soup = BeautifulSoup(response.data, 'html.parser')

    assert 'You cannot book more than 12 tickets!' in soup.text


def test_book_less_than_12_tickets(client, clubs, competitions):
    initial_points = int(clubs[0].get("points"))
    places_to_book = 5

    response = client.post(
        '/purchasePlaces',
        data={
            'club': clubs[0].get("name"),
            'competition': competitions[0].get("name"),
            'places': places_to_book
        }
    )

    assert response.status_code == 200
    soup = BeautifulSoup(response.data, 'html.parser')
    assert "Great - booking complete!" in soup.text

    updated_points = int(clubs[0].get("points"))
    assert updated_points == initial_points - places_to_book

def test_book_competition_in_the_past(client, clubs, competitions):
    competition_name = quote(competitions[1]["name"])
    club_name = quote(clubs[0]["name"])
    response = client.get(f'/book/{competition_name}/{club_name}')

    assert response.status_code == 200
    soup = BeautifulSoup(response.data, 'html.parser')
    assert "Sorry, the competition is already over. Please try another competition." in soup.text


def test_book_competition_in_the_future(client, clubs, competitions):
    competition_name = quote(competitions[0]["name"])
    club_name = quote(clubs[0]["name"])
    response = client.get(f'/book/{competition_name}/{club_name}')

    assert response.status_code == 200
    soup = BeautifulSoup(response.data, 'html.parser')
    assert "How many places?" in soup.text

def test_booking_more_than_available_points(client, clubs, competitions):
    clubs[0]["points"] = 3
    competitions[0]["numberOfPlaces"] = 10

    response = client.post(
        '/purchasePlaces',
        data={
            'club': clubs[0].get("name"),
            'competition': competitions[0].get("name"),
            'places': 4
        }
    )

    assert response.status_code == 200
    soup = BeautifulSoup(response.data, 'html.parser')

    assert "Not enough points to book these places." in soup.text


def test_booking_more_than_competition_available_places(client, clubs, competitions):
    clubs[0]["points"] = 15
    competitions[0]["numberOfPlaces"] = 3

    response = client.post(
        '/purchasePlaces',
        data={
            'club': clubs[0].get("name"),
            'competition': competitions[0].get("name"),
            'places': 4
        }
    )

    assert response.status_code == 200
    soup = BeautifulSoup(response.data, 'html.parser')

    assert "Not enough places left in this competition." in soup.text