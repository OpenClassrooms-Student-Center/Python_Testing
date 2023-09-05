import pytest
from server import app



# Test pour acheter des places avec un club et une compétition valides
def test_purchase_places_valid():
    client = app.test_client()
    response = client.post('/purchasePlaces',
                           data={'club': 'Simply Lift', 'competition': 'Spring Festival', 'places': '5'},
                           follow_redirects=True)
    assert response.status_code == 200
    assert b'Welcome' in response.data

# Test pour acheter des places avec un club ou une compétition non trouvés
def test_purchase_places_invalid_club_or_competition():
    client = app.test_client()
    response = client.post('/purchasePlaces', data={'club': 'NonExistentClub', 'competition': 'Spring Festival', 'places': '5'})
    assert response.status_code == 200


# Test pour acheter plus de places que disponibles
def test_purchase_places_not_enough_places():
    client = app.test_client()
    response = client.post('/purchasePlaces', data={'club': 'Simply Lift', 'competition': 'Spring Festival', 'places': '50'})
    assert response.status_code == 302


# Test pour acheter des places sans assez de points dans le club
def test_purchase_places_not_enough_points():
    client = app.test_client()
    response = client.post('/purchasePlaces', data={'club': 'Simply Lift', 'competition': 'Spring Festival', 'places': '20'})
    assert response.status_code == 302

