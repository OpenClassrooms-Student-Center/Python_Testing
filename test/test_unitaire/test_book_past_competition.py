import server
import pytest

@pytest.fixture
def client():
    server.app.config['TESTING'] = True
    clients = server.app.test_client()
    return clients

def test_booking_actual_competition(client):
    club = server.clubs[0]["name"]
    response = client.post('/purchasePlaces',
                           data={
                               "club": club,
                               "competition": "Spring Festival",
                               "places": 10
                           })
    assert response.status_code == 200

def test_booking_past_competition(client):
    club = server.clubs[0]['name']
    response = client.post('/purchasePlaces',
                           data={
                               "club": club,
                               "competition": "Fall Classic",
                               "places": 10
                           })
    assert response.status_code == 302