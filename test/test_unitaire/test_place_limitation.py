import pytest
import server


@pytest.fixture
def client():
    server.app.config['TESTING'] = True
    clients = server.app.test_client()
    return clients

def test_purchase_more_than_12_place(client):
    club = server.clubs[0]['name']
    competition = server.competitions[0]
    response = client.post('/purchasePlaces',
                           data={
                               'club': club,
                               'competition': competition['name'],
                               'numberOfPlaces': competition['numberOfPlaces'],
                               'places': 14,
                           })
    assert response.status_code == 200

def test_purchase_correct_amount_of_point(client):
    club = server.clubs[0]['name']
    competition = server.competitions[0]
    response = client.post('/purchasePlaces',
                           data={
                               'club': club,
                               'competition': competition['name'],
                               'numberOfPlaces': competition['numberOfPlaces'],
                               'places': 12,
                           })
    assert response.status_code == 200