import server
import pytest


@pytest.fixture()
def client():
    with server.app.test_client() as client:
        yield client


class TestLogin():
    def test_login_valid_mail(self, client):
        valid_mail = {'email': 'admin@irontemple.com'}
        response = client.post('/showSummary', data=valid_mail)
        assert b'Welcome, admin@irontemple.com' in response.data

    def test_login_invalid_mail(self, client):
        invalid_mail = {'email': 'invalid@invalid.com'}
        response = client.post('/showSummary', data=invalid_mail, follow_redirects=True)
        assert b'This email is incorrect.' in response.data




	