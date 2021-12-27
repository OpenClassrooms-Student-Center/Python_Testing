import pytest

from flask import session


def test_index_get(client):
    response = client.get('/')
    assert response.status_code == 200


def test_showSummary_get(client):
    response = client.get('/showSummary')
    assert response.status_code == 405


def test_login_valid_input(client, auth):
    response = auth.login()
    assert b'john@simplylift.co' in response.data

    with client:
        client.get("/book")
        assert session["user_id"] == "john@simplylift.co"


@pytest.mark.parametrize(('email',), (
    ('does_not_exist@gmail.com',),
    ))
def test_login_invalid_input(auth, email):
    response = auth.login(email)
    assert "http://localhost/" == response.headers["Location"]


def test_logout(client, auth):
    auth.login()

    with client:
        response = auth.logout()
        assert 'user_id' not in session
        assert "http://localhost/" == response.headers["Location"]
