from ..conftest import club_fixture, competition_fixture, client
from server import showSummary
import server


def test_showsummary_valid_credential(client, monkeypatch, club_fixture):
    monkeypatch.setattr(server, "clubs", club_fixture)
    user = {"email": "admin@irontemple.com"}
    response = client.post("/showSummary", data=user)
    assert response.status_code == 200


def test_showsummary_invalid_credential(client, monkeypatch, club_fixture):
    monkeypatch.setattr(server, "clubs", club_fixture)
    user = {"email": "nicolas@vendrisse.com"}
    response = client.post("/showSummary", data=user)
    assert response.status_code == 302
