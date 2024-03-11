import pytest
from server import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

# tests principal functions
def test_index(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b"Welcome to the GUDLFT Registration Portal!" in response.data

def test_showSummary(client):
    response = client.post('/showSummary', data={'email': 'john@simplylift.co'})
    assert response.status_code == 200
    assert b"Summary" in response.data
    assert b"john@simplylift.co" in response.data
    assert b"13" in response.data

def test_book(client):
    response = client.get('/book/Spring-Festival/Simply-Lift')
    assert response.status_code == 200
    assert b"Booking for Spring-Festival" in response.data

def test_purchase_places(client):
    response = client.post('/purchasePlaces', data={'club': 'Simply-Lift', 'competition': 'Spring-Festival', 'places': '3'})
    assert response.status_code == 200
    assert b"Great-booking complete!" in response.data