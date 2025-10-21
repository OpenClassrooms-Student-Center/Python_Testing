import pytest
from server import app
import server

"""
Fichier de tests unitaires pour la fonctionnalité de réservation de places.
Le but est de vérifier que la réservation de places n'est possible qu'avec suffisamment de points.

1er test : on a 4 points on veut réserver 4 places, réservation acceptée.
2ème test : on a 4 points on veut réserver 5 places, réservation refusée.
"""

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


def test_purchase_places_with_enough_points(client):
    server.clubs = [{"name": "Club A", "points": "4"}]
    server.competitions = [{"name": "Comp 1", "numberOfPlaces": "5"}]

    response = client.post('/purchasePlaces', data={
        'competition': 'Comp 1',
        'club': 'Club A',
        'places': '4'
    })

    assert response.status_code == 200
    assert b"Great-booking complete!" in response.data
    assert int(server.competitions[0]['numberOfPlaces']) == 1


def test_purchase_places_without_enough_points(client):
    server.clubs = [{"name": "Club B", "points": "4"}]
    server.competitions = [{"name": "Comp 2", "numberOfPlaces": "5"}]

    response = client.post('/purchasePlaces', data={
        'competition': 'Comp 2',
        'club': 'Club B',
        'places': '5'
    })

    assert response.status_code == 200
    assert b"Cannot book more places than club points." in response.data
    assert int(server.competitions[0]['numberOfPlaces']) == 5

