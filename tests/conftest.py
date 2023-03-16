import pytest
import logging
import json
import os

from unittest.mock import patch
from ..server import create_app, loadClubs


def pytest_configure(config):
    logging.basicConfig(level=logging.INFO)

@pytest.fixture
def client():
    app = create_app({"TESTING": True})

    with app.test_client() as client:
        yield client

@pytest.fixture
def purchaseRequest():
    purchase = {
		'club': 'Simply Lift',
		'competition': 'Fall Classic',
		'places': '4'
		}
    
    yield purchase

@pytest.fixture
def purchaseMorePointThanCompetition():
    purchase = {
		'club': 'Simply Lift',
		'competition': 'Fall Classic',
		'places': '14'
		}
    
    yield purchase

@pytest.fixture
def purchaseMorePointThanClub():
    purchase = {
		'club': 'Iron Temple',
		'competition': 'Fall Classic',
		'places': '5'
		}
    
    yield purchase

@pytest.fixture
def purchaseNoPointSpecified():
    purchase = {
		'club': 'Iron Temple',
		'competition': 'Fall Classic',
		'places': ''
		}
    
    yield purchase

@pytest.fixture
def patch_clubs(monkeypatch):

    clubs_list = clubs_dataset()
    club_json = json.dumps(clubs_list)

    monkeypatch.setenv('server.clubs', club_json)
    yield club_json
    monkeypatch.delenv('server.clubs')

@pytest.fixture
def patch_competitions(monkeypatch):

    competitions_list = competitions_dataset()
    competitions_json = json.dumps(competitions_list)

    monkeypatch.setenv('server.competitions', competitions_json)
    yield competitions_json
    monkeypatch.delenv('server.competitions')

def clubs_dataset():
    with open('data/clubs_test.json') as c:
         listOfClubs = json.load(c)['clubs']
    return listOfClubs

def competitions_dataset():
    with open('data/competitions_tests.json') as c:
         listOfCompetitions = json.load(c)['clubs']
    return listOfCompetitions
