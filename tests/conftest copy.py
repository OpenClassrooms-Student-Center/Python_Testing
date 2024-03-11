import os
import json
import pytest
from flask import Flask, url_for

@pytest.fixture
def app():
    app = Flask(__name__)

    @app.route('/')
    def index():
        return "Welcome to the GUDLFT Registration Portal!"

    return app

@pytest.fixture
def test_client(app):
    with app.test_client() as client:
        yield client

@pytest.fixture
def competitions_and_clubs():
    competitions = []
    clubs = []

    # Obtenir le chemin absolu du répertoire contenant le script Python
    current_dir = os.path.dirname(os.path.abspath(__file__))
    competitions_path = os.path.join(current_dir, '../competitions.json')
    clubs_path = os.path.join(current_dir, '../clubs.json')

    with open(competitions_path) as comps_file:
        competitions_data = json.load(comps_file)
        competitions = competitions_data['competitions']

    with open(clubs_path) as clubs_file:
        clubs_data = json.load(clubs_file)
        clubs = clubs_data['clubs']

    return competitions, clubs

def test_book(test_client, competitions_and_clubs):
    competitions, clubs = competitions_and_clubs

    # Connectez-vous d'abord à la page /showSummary
    login_response = test_client.post("/showSummary", data={"email": "john@simplylift.co"})
    assert login_response.status_code == 200
    assert b"Welcome, john@simplylift.co" in login_response.data

    # Effectuez une requête GET vers l'URL du bouton "Book Places" pour chaque compétition et chaque club
    for comp in competitions:
        for club in clubs:
            book_places_url = url_for('book', competition=comp['name'], club=club['name'])
            book_response = test_client.get(book_places_url)
            assert book_response.status_code == 200
            assert bytes(comp['name'], 'utf-8') in book_response.data
            assert bytes(f"Places available: {comp['numberOfPlaces']}", 'utf-8') in book_response.data
