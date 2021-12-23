import sys
import os

import pytest

from flask import g, json, request, Response, session, url_for
#from flaskr.db import get_db

current = os.path.dirname(os.path.realpath(__file__))
test_dir = os.path.dirname(current)
root_dir = os.path.dirname(test_dir)
sys.path.append(test_dir)
sys.path.append(root_dir)

from conftest import *
from server import app, clubs, load_clubs

MAX_CLUB_POINTS = 12

def test_purchase_twice(auth, client, purchase):
    """
    GIVEN an existing user
    WHEN they attempt to purchase places twice
    THEN points and places are deduced and the competition is added to their profile
    """
    auth.login()
    response = purchase.purchase()
    db = load_clubs()

    assert response.status_code == 200
    assert b"Points available: 7" in response.data
    assert b"Number of Places: 3" in response.data
    assert db[0]['competitions'][2]['name'] == 'Frozen Drops'

    response = purchase.purchase()
    db = load_clubs()
    assert response.status_code == 200
    assert b"Points available: 1" in response.data
    assert b"Number of Places: 1" in response.data
    assert db[0]['competitions'][2]['places'] == '4'
