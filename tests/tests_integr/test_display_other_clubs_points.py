import pytest
from Python_Testing.tests.conftest import client
from Python_Testing import server


def test_login(client):
    app, templates = client
    clubs = server.loadClubs()
    rv = app.post(
        "/showSummary", data=dict(email=clubs[0]["email"]), follow_redirects=True
    )
    template, context = templates[0]

    assert context["club"] == clubs[0]
    assert template.name == 'welcome.html'
    data = rv.data.decode()
    assert clubs[1]["name"] in data
    assert clubs[2]["name"] in data
    assert clubs[2]["points"] in data
