from tests.unit_test.conftest import client, club, competition
from server import loadClubs, loadCompetitions


def test_loadClubs():
    assert loadClubs("./tests/unit_test/fixture_files/fixture_load.json") == club()

def test_loadCompetitions():
    assert loadCompetitions("./tests/unit_test/fixture_files/fixture_load.json") == competition()

def test_sould_login_in_out(client):
    response = client.get("/logout")
    assert response.status_code == 302

def test_sould_connect_with_email_exists(client):
    clubs = loadClubs()
    for club in clubs:
        response = client.post("/showSummary", data={'email': club.get('email')})
        assert response.status_code == 200

def test_sould_no_connect_with_email_does_not_exists(client):
    response = client.post("/showSummary", data={'email': "not_exists_email@test.com"})
    assert response.status_code == 401