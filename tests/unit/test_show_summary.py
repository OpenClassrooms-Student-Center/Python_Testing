import html
import os
import sys

import pytest

# Obtenir le chemin du répertoire parent du répertoire actuel (dossier unit)
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.insert(0, PROJECT_ROOT)

import server

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, PROJECT_ROOT)


def decode_response(response_bytes):
    decoded_text = response_bytes.decode('utf-8')
    decoded_text = html.unescape(decoded_text)
    return decoded_text


@pytest.fixture
def app():
    app = server.app
    app.config['TESTING'] = True
    app.secret_key = 'testing_secret_key'
    return app


def test_invalid_email(app):
    client = app.test_client()
    response = client.post('/showSummary', data={'email': 'invalid@example.com'}, follow_redirects=True)

    decoded_response = decode_response(response.data)

    assert "Sorry, that email wasn't found." in decoded_response
