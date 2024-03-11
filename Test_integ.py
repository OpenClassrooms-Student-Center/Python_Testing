import pytest
from server import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

# Tests concerning issues

# Issue#1 email adress empty or unknown PR#213 
def test_showSummary_empty(client):
    response = client.post('/showSummary', data={'email': ''})
    assert response.status_code == 200
    assert b"Welcome to the GUDLFT Registration Portal!" in response.data

#  Issue#2 not negative account for clubs PR#215  
def test_purchasePlaces_points(client):
    response = client.post('/purchasePlaces', data={'club': 'Iron-Temple', 'competition': 'Spring-Festival', 'places': '10'})
    assert response.status_code == 200
    assert b"You do not have enougth points" in response.data

# Issue#4 12 places max PR#216   
def test_purchasePlaces_max(client):
    response = client.post('/purchasePlaces', data={'club': 'Simply-Lift', 'competition': 'Spring-Festival', 'places': '13'})
    assert response.status_code == 200
    assert b"You can not buy more than 12 places" in response.data

# Issue#5 not possible to book competition in the past PR#218 
def test_book_past(client):
    response = client.get('/book/Fall-Classic/Simply-Lift')
    assert response.status_code == 200
    assert b"Competition is over. You can not buy places" in response.data

# Issue#6 update points PR#215   
def test_purchasePlaces_update(client):
    response = client.post('/purchasePlaces', data={'club': 'Simply-Lift', 'competition': 'Spring-Festival', 'places': '6'})
    assert response.status_code == 200
    assert b"7" in response.data #13-6points

# Issue#7 display clubs points
def test_display_points(client):
    response = client.get('/displaypoints')
    assert response.status_code == 200
    assert b'Simply-Lift' in response.data
    assert b'Iron-Temple' in response.data
    assert b'She-Lifts' in response.data

# empty field purchase places PR#214   
def test_purchasePlaces_empty(client):
    response = client.post('/purchasePlaces', data={'club': 'Simply-Lift', 'competition': 'Spring-Festival', 'places': ''})
    assert response.status_code == 200
    assert b"Something went wrong-please try again" in response.data

