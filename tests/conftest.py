import pytest
import logging
import json
import os

from ..server import create_app

@pytest.fixture
def client():
    app = create_app({"TESTING": True})
    
    with app.test_client() as client:
        yield client

@pytest.fixture
def purchaseBase():
    purchase = {
		'club': 'club test base',
		'competition': 'Competition Test base',
		'places': '4'
		}
    print( "REQUETE AVANT ENVOI : ", purchase)
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

@pytest.fixture
def dateIsOver():
    purchase = {
		'club': 'club test base',
		'competition': 'out dated',
		'places': '4'
		}
    
    yield purchase