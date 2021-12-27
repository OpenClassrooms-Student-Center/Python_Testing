import os
import os.path
import pytest
import sys

from flask import g, session, url_for

current = os.path.dirname(os.path.realpath(__file__))
test_dir = os.path.dirname(current)
root_dir = os.path.dirname(test_dir)
sys.path.append(test_dir)
sys.path.append(root_dir)

from conftest import *
from server import app


def test_full_display(client, auth):
    """
    GIVEN an existing user
    WHEN they attempt to access /fullDisplay
    THEN allow full display
    """
    shutil.copyfile('clubs.json', 'test_clubs.json')
    shutil.copyfile('competitions.json', 'test_competitions.json')

    auth.login()
    response = client.get('/fullDisplay')

    assert response.status_code == 200
    assert b"Current Point Count" in response.data
    assert b"Simply Lift" in response.data
    assert b"Points: 13" in response.data
    assert b"Iron Temple" in response.data
    assert b"She Lifts" in response.data

    os.remove('test_clubs.json')
    os.remove('test_competitions.json')
    
def test_full_display_unlogged(client, auth):
    """
    GIVEN an unlogged user
    WHEN they attempt to access /fullDisplay
    THEN redirect them for privacy reasons
    """
    response = client.get('/fullDisplay')
    assert response.status_code == 302
    assert "http://localhost/" == response.headers["Location"]
