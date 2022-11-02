import pytest
from Python_Testing.tests.conftest import client
from Python_Testing import server


def test_login(client):
    app, templates = client
    clubs = server.loadClubs()
    competitions = server.loadCompetitions()
    response = app.get("/")
    assert response.status_code == 200
    rv = app.post(
        "/showSummary", data=dict(email=clubs[0]["email"]), follow_redirects=True
    )
    template, context = templates[1]
    assert rv.status_code == 200
    assert context["club"] == clubs[0]
    assert template.name == 'welcome.html'
    data = rv.data.decode()
    assert clubs[0]["email"] in data
    assert competitions[0]["name"] in data
    assert competitions[1]["name"] in data





