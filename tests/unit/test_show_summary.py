import sys
import os

import pytest

from flask import g, session, url_for
#from flaskr.db import get_db


current = os.path.dirname(os.path.realpath(__file__))
test_dir = os.path.dirname(current)
root_dir = os.path.dirname(test_dir)
sys.path.append(test_dir)
sys.path.append(root_dir)

from conftest import *
from server import app


def test_index_get(client):
    response = client.get('/')
    assert response.status_code == 200

def test_showSummary_get(client):
    response = client.get('/showSummary')
    assert response.status_code == 405

def test_login_valid_input(client, auth):
    """
    GIVEN an existing user
    WHEN a user attempts to connect with the right credentials
    THEN log them in and redirect to the show_summary page
    """
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
