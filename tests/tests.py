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

    assert "You cannot book more than 12 tickets !" in soup.text


def test_book_less_than_12_tickets(client, clubs, competitions):
    response = client.post(
        '/purchasePlaces',
        data={
            'club': clubs[0].get("name"),
            'competition': competitions[0].get("name"),
            'places': 5})
    assert response.status_code == 200
    soup = BeautifulSoup(response.data, 'html.parser')

    assert "Great-booking complete!" in soup.text
