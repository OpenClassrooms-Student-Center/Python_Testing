import os
import pytest
import shutil
import sys

from dotenv import load_dotenv
from os import environ

current = os.path.dirname(os.path.realpath(__file__))
test_dir = os.path.dirname(current)
sys.path.append(test_dir)

import server
from server import app, DB_CLUBS, DB_COMP, load_config

@pytest.fixture
def test_app():
    load_dotenv()
    test_app = app
    test_app.secret_key = os.getenv('SECRET_KEY')

    yield test_app

@pytest.fixture
def client(test_app):
    shutil.copyfile('clubs.json', 'test_clubs.json')
    shutil.copyfile('competitions.json', 'test_competitions.json')
    load_config(mode='TESTING')

    yield test_app.test_client()

    os.remove('test_clubs.json')
    os.remove('test_competitions.json')

class AuthActions(object):
    def __init__(self, client):
        self._client = client

    def login(self, email='john@simplylift.co'):
        return self._client.post(
            '/showSummary',
            data={'email': email}
        )

    def logout(self):
        return self._client.get('/logout')


class PurchaseActions(object):
    def __init__(self, client):
        self._client = client

    def purchase(self, places='2', club='Simply Lift', competition='Frozen Drops'):
        return self._client.post(
            '/purchasePlaces',
            data={'places': places, 'club': club, 'competition': competition}
        )

    def only_purchase(self, places='2', club='Simply Lift', competition='Frozen Drops'):
        return self._client.post(
            '/purchasePlaces',
            data={'places': places, 'club': club, 'competition': competition}
        )

@pytest.fixture
def auth(client):
    return AuthActions(client)

@pytest.fixture
def purchase(client):
    return PurchaseActions(client)

@pytest.fixture
def only_purchase(client):
    return PurchaseActions(client)
