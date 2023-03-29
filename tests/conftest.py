import logging
import pytest
import shutil
import json
import os

from ..server import create_app

CLUBS_TEST_PATH = 'data_tests/clubs.json'
COMPETITIONS_TEST_PATH = 'data_tests/competitions.json'


@pytest.fixture
def client():
    app = create_app({"TESTING": True})

    # Initialisation de la base de données
    with app.app_context():
        with open(CLUBS_TEST_PATH, 'r') as cl:
            clubs_temp = json.load(cl)
        with open(COMPETITIONS_TEST_PATH, 'r') as co:
            comps_temp = json.load(co)

    yield app.test_client()

    # Nettoyage de la base de données
    with app.app_context():

        with open(CLUBS_TEST_PATH, 'w') as clw:
            json.dump(clubs_temp, clw)

        with open(COMPETITIONS_TEST_PATH, 'w') as cow:
            json.dump(comps_temp, cow)


@pytest.fixture
def purchaseBase():
    purchase = {
        'club': 'Simply Lift',
                'competition': 'Spring Festival',
                'places': '4'
    }

    yield purchase


@pytest.fixture
def purchase12points():
    purchase = {
        'club': 'Simply Lift',
                'competition': 'Spring Festival',
                'places': '13'
    }

    yield purchase


@pytest.fixture
def purchaseEmpty():
    purchase = {
        'club': 'Simply Lift',
                'competition': 'Spring Festival',
                'places': ''
    }

    yield purchase


@pytest.fixture
def purchaseNotEnoughPointsCompetition():
    purchase = {
        'club': 'Simply Lift',
                'competition': 'Fall Classic',
                'places': '4'
    }

    yield purchase


@pytest.fixture
def purchaseNotEnoughPointsClub():
    purchase = {
        'club': 'Iron Temple',
                'competition': 'Spring Festival',
                'places': '4'
    }

    yield purchase


@pytest.fixture
def dateIsOver():
    purchase = {
        'club': 'Simply Lift',
                'competition': 'Out Dated',
                'places': '4'
    }

    yield purchase
