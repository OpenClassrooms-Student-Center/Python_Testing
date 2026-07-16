"""
Fixtures partagées pour toute la suite de tests.

L'application charge clubs.json et competitions.json au moment de l'import et
modifie ces listes en mémoire (déduction de points/places). Pour garantir des
tests déterministes et isolés, on remplace ces données globales par des jeux
de test contrôlés avant chaque test, et on réinitialise le compteur de
réservations cumulées.
"""
import pytest

import server as server_module
from server import app


@pytest.fixture
def clubs_data():
    """Deux clubs de test : l'un avec beaucoup de points, l'autre avec peu."""
    return [
        {"name": "Test Club A", "email": "a@test.com", "points": "15"},
        {"name": "Test Club B", "email": "b@test.com", "points": "4"},
    ]


@pytest.fixture
def competitions_data():
    """
    Jeux de compétitions contrôlés :
    - une clairement à venir (2050)
    - une clairement passée (2000)
    - une à venir mais complète (0 place)
    """
    return [
        {"name": "Future Comp", "date": "2050-01-01 10:00:00", "numberOfPlaces": "25"},
        {"name": "Past Comp", "date": "2000-01-01 10:00:00", "numberOfPlaces": "25"},
        {"name": "Full Comp", "date": "2050-02-01 10:00:00", "numberOfPlaces": "0"},
    ]


@pytest.fixture(autouse=True)
def setup_data(clubs_data, competitions_data, monkeypatch):
    """Remplace les données globales du serveur et réinitialise les compteurs."""
    monkeypatch.setattr(server_module, "clubs", clubs_data)
    monkeypatch.setattr(server_module, "competitions", competitions_data)
    server_module.club_competition_bookings.clear()
    yield
    server_module.club_competition_bookings.clear()


@pytest.fixture
def client():
    """Client de test Flask (mode TESTING pour des messages d'erreur propres)."""
    app.config["TESTING"] = True
    return app.test_client()


@pytest.fixture
def logged_in_client(client):
    """Client déjà authentifié en tant que Test Club A."""
    client.post("/showSummary", data={"email": "a@test.com"})
    return client
