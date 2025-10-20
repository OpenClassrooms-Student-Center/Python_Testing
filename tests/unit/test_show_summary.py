import pytest
import server
from server import app


@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


def test_show_summary_with_valid_email(client, monkeypatch):
    club = {'name': 'John', 'email': 'john@simplylift.co', 'points': '15'}
    monkeypatch.setattr(server, 'clubs', [club])
    monkeypatch.setattr(server, 'competitions', [])
    response = client.post('/showSummary', data={'email': 'john@simplylift.co'})
    assert response.status_code == 200
    assert b'Welcome' in response.data
    assert b'john@simplylift.co' in response.data


def test_show_summary_with_unknown_email(client, monkeypatch):
    club = {'name': 'Other Club', 'email': 'other@example.com', 'points': '10'}
    monkeypatch.setattr(server, 'clubs', [club])
    monkeypatch.setattr(server, 'competitions', [])
    response = client.post('/showSummary', data={'email': 'unknown@example.com'})
    assert response.status_code == 200
    assert b'please try again' in response.data


def test_show_summary_with_invalid_email(client, monkeypatch):
    club = {'name': 'John', 'email': 'john@simplylift.co', 'points': '15'}
    monkeypatch.setattr(server, 'clubs', [club])
    monkeypatch.setattr(server, 'competitions', [])
    response = client.post('/showSummary', data={'email': '   '})
    assert response.status_code == 200
    assert b'please try again' in response.data