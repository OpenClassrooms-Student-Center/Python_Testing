import pytest
from server import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

# test access and no access routes defined

def test_index(client):
    response = client.get('/')
    assert b'Welcome to the GUDLFT Registration Portal!' in response.data

def test_show_summary_valid_email(client):
    response = client.post('/showSummary', data={'email': 'john@simplylift.co'})
    assert b'Welcome, john@simplylift.co' in response.data

def test_show_summary_invalid_email(client):
    response = client.post('/showSummary', data={'email': 'invalid@example.com'})
    assert b'GUDLFT Registration' in response.data

def test_book_valid_competition(client):
    response = client.get('/book/Spring-Festival/Simply-Lift')
    assert b'Booking for Spring-Festival' in response.data

def test_book_invalid_competition(client):
    response = client.get('/book/Invalid-Competition/Simply-Lift')
    assert b'Something went wrong-please try again' in response.data

def test_purchase_places_valid(client):
    response = client.post('/purchasePlaces', data={'club': 'Simply-Lift', 'competition': 'Spring-Festival', 'places': '1'})
    assert b'Great-booking complete!' in response.data

def test_purchase_places_invalid(client):
    response = client.post('/purchasePlaces', data={'club': 'Simply-Lift', 'competition': 'Spring-Festival', 'places': '20'})
    assert b'You can not buy more than 12 places' in response.data



