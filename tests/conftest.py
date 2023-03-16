import pytest
import logging
import json
import os

from unittest.mock import patch
from ..server import create_app, loadClubs


def pytest_configure(config):
    logging.basicConfig(level=logging.INFO)

def clubs_dataset():
    with open('data/clubs_test.json') as c:
         listOfClubs = json.load(c)['clubs']
    return listOfClubs

def competitions_dataset():
    with open('data/competitions_test.json') as c:
         listOfCompetitions = json.load(c)['competitions']
    return listOfCompetitions

@pytest.fixture
def client():
    app = create_app({"TESTING": True})

    clubs = clubs_dataset()
    competitions = competitions_dataset()

    os.environ['server.clubs'] = json.dumps(clubs)
    os.environ['server.competitions'] = json.dumps(competitions)

    with app.test_client() as client:
        yield client
    
    del os.environ['server.clubs']
    del os.environ['server.competitions']

@pytest.fixture
def purchaseBase():
    purchase = {
		'club': 'club test base',
		'competition': 'Competition Test base',
		'places': '4'
		}
    
    yield purchase

@pytest.fixture
def purchase12points():
    purchase = {
		'club': 'club test more than 12 points',
		'competition': 'Competition Test 12 points',
		'places': '13'
		}
    
    yield purchase

@pytest.fixture
def purchaseEmpty():
    purchase = {
		'club': 'club test base',
		'competition': 'Competition Test base',
		'places': ''
		}
    
    yield purchase

@pytest.fixture
def purchaseNotEnoughPointsCompetition():
    purchase = {
		'club': 'club test base',
		'competition': 'Competition Test not enough points',
		'places': '4'
		}
    
    yield purchase

@pytest.fixture
def purchaseNotEnoughPointsClub():
    purchase = {
		'club': 'club test not enough points',
		'competition': 'Competition Test base',
		'places': '4'
		}
    
    yield purchase