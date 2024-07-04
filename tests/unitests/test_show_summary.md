import pytest
import server
import json
from server import app
from flask import url_for
from http import HTTPStatus


def test_show_summary_ok(client, monkeypatch, competitions):
    """
    GIVEN a email that exists
    WHEN the '/showSummary' page is requested (POST)
    THEN check the summary page is displayed correctly
    """

    # avec monkeypatch
    def patch_get_club(dummy):
        """Mock get_club() function"""

        return {"name": "Simply Lift", "email": "john@simplylift.co", "points": "13"}

    monkeypatch.setattr(server, "getClub", patch_get_club)

    monkeypatch.setattr(server, "competitions", competitions)

    response = client.post("/showSummary", data={"email": "john@simplylift.co"})
    data = response.data.decode()

    # print(data)
    # assert response.status_code == 200
    # assert data.find("<h2>Welcome, john@simplylift.co </h2>") != -1
    assert response.status_code == HTTPStatus.OK
    assert "<h2>Welcome, john@simplylift.co </h2>" in data # Vérifie le contenu spécifique de la page


def test_show_summary_unknown_email(client, monkeypatch):
    """
    GIVEN an email that does not exist
    WHEN the '/showSummary' page is requested (POST)
    THEN check the error message is displayed correctly
    """

    # Fonction mock pour getClub
    def patch_get_club(dummy):
        """Mock get_club() function"""
        return None

    # Utiliser monkeypatch pour remplacer getClub par patch_get_club
    monkeypatch.setattr(server, "getClub", patch_get_club)

    # Simuler l'envoi d'un email qui n'existe pas
    response = client.post("/showSummary", data={"email": "nonexistent@email.com"})

    # Vérifier que la réponse est une redirection
    assert response.status_code == 302

    # Suivre la redirection et obtenir la réponse
    follow_response = client.get(response.headers["Location"])
    print(follow_response.get_data(as_text=True))

    # Vérifier que le message d'erreur est affiché
    assert "Error: email nonexistent@email.com not found" in follow_response.get_data(as_text=True)
    





    



