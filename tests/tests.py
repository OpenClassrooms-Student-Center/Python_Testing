import pytest

from server import app

# verifier les données envoyées, gérer tous les cas (mauvais set de données par exemple)
# si string reçu au lieu de int > renvoyer une erreur par exemple
# tester le payload envoyé


@pytest.fixture
def client():
    app.config['TESTING'] = True
    return app.test_client()


def test_index(client):
    response = client.get('/')
    assert response.status_code == 200
    data = response.data.decode()
    assert 'GUDLFT Registration' in data


def test_ShowSummary(client):
    response = client.post(
        '/showSummary', data={'email': 'john@simplylift.co'}, follow_redirects=True
    )
    data = response.data.decode()
    assert response.status_code == 200
    assert 'Competitions' in data
    assert 'Club' in data


def test_Invalid_ShowSummary(client):
    response = client.post(
        '/showSummary', data={'email': 'mock@mock.com'}, follow_redirects=True
    )
    data = response.data.decode()
    assert response.status_code == 200
    assert 'Email not found' in data


def test_book(client):
    response = client.get('/book/Spring Festival/Simply Lift')
    assert response.status_code == 200


def test_purchasePlaces(client):
    client = app.test_client()
    response = client.post(
        '/purchasePlaces', data={'places': '1', 'competition': 'Test Competition', 'club': 'Simply Lift'})
    data = response.data.decode()
    assert response.status_code == 200
    assert 'Great, booking complete!' in data


def test_purchase_date(client):
    client = app.test_client()
    response = client.post(
        '/purchasePlaces', data={'places': '1', 'competition': 'Fall Classic', 'club': 'Simply Lift'})
    data = response.data.decode()
    assert response.status_code == 200
    assert 'Sorry, the competition has already started.' in data


def test_purchase_points(client):
    response = client.post(
        '/purchasePlaces', data={'places': '5', 'competition': 'Test Competition', 'club': 'Iron Temple'})
    data = response.data.decode()
    assert response.status_code == 200
    assert 'Sorry, you do not have enough points.' in data


def test_12_points_limit(client):
    response = client.post(
        '/purchasePlaces', data={'places': '13', 'competition': 'Test Competition', 'club': 'Test Club'})
    data = response.data.decode()
    assert response.status_code == 200
    assert 'Sorry, you can only book up to 12 places.' in data


def test_club_page(client):
    response = client.get('/clubs')
    assert response.status_code == 200
    data = response.data.decode()
    assert 'Welcome' in data
