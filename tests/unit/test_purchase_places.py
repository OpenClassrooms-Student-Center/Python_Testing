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

def test_purchase_first_time(auth, client, purchase):
    """
    GIVEN an existing user
    WHEN they attempt to purchase places for a competition for the first time
    THEN points and places are deduced and the competition is added to their profile
    """
    auth.login()
    response = purchase.purchase()
    db = load_clubs()

    assert response.status_code == 200
    assert b"Summary | GUDLFT Registration" in response.data
    assert b"Points available: 7" in response.data
    assert b"Number of Places: 3" in response.data
    assert db[0]['competitions'][2]['name'] == 'Frozen Drops'

def test_purchase_places_exists(auth, client, purchase):
    """
    GIVEN an existing user
    WHEN they attempt to purchase places for a competition they've already booked for
    THEN points and places are deduced
    """
    auth.login()
    response = purchase.purchase(places='1', club='Simply Lift', competition='Spring Festival')
    db = load_clubs()

    assert response.status_code == 200
    assert b"Summary | GUDLFT Registration" in response.data
    assert b"Points available: 10" in response.data
    assert db[0]['competitions'][0]['places'] == '12'

def test_purchase_not_logged(client, purchase):
    """
    GIVEN a user not logged in
    WHEN they attempt to purchase places for a competition
    IF they have enough points and there are enough places
    THEN points and places are deduced
    """
    response = purchase.purchase()
    assert response.status_code == 302

def test_purchase_too_much(auth, client, purchase):
    """
    GIVEN an existing user
    WHEN they attempt to purchase more places for a competition than possible
    THEN the attempts fails
    """
    auth.login()
    response = purchase.purchase('20')
    assert response.status_code == 200
    assert b"Summary | GUDLFT Registration" in response.data
    assert b"Not enough available places anymore" in response.data

def test_purchase_negative_number(auth, client, purchase):
    """
    GIVEN an existing user
    WHEN they attempt to purchase places for a competition
    IF they have enough points and there are enough places
    THEN points and places are deduced
    """
    auth.login()
    response = purchase.purchase('-6')
    assert response.status_code == 200
    assert b"Summary | GUDLFT Registration" in response.data
    assert b"Please purchase more than one place." in response.data
