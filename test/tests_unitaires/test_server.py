import pytest
from server import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_purchase_places_exceeds_competition_places(client, monkeypatch):
    # Simuler un club avec assez de points
    test_club = {"name": "Test Club", "email": "test@club.com", "points": "20"}
    # Simuler une compétition avec peu de places restantes
    test_competition = {"name": "Test Competition", "numberOfPlaces": "3", "date": "2025-12-12 10:00:00"}

    # Injecter les données dans server.py
    monkeypatch.setattr("server.clubs", [test_club])
    monkeypatch.setattr("server.competitions", [test_competition])

    # Envoyer un POST pour demander trop de places
    response = client.post("/purchasePlaces", data={
        "competition": "Test Competition",
        "club": "Test Club",
        "places": "50"
    }, follow_redirects=True)

    # Vérifier que le message d'erreur s'affiche bien
    assert b"enough places" in response.data


