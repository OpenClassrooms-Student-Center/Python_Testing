import pytest
from server import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


def test_showSummary(client):
    response = client.post('/showSummary', data=dict(email='john@simplylift.co'))
    assert b'<title>Summary | GUDLFT Registration</title>' in response.data


def test_showSummary_unknown_email(client):
    response = client.post('/showSummary', data=dict(email='test@example.com'))
    assert b'<title>GUDLFT Registration</title>' in response.data

