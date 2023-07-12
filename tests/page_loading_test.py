import pytest

from server import *


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_showSummary(client):
    response = client.post("/showSummary", data=dict(email="john@simplylift.co"))
    assert b"<title>Summary | GUDLFT Registration</title>" in response.data


def test_showSummary_unknown_email(client):
    response = client.post("/showSummary", data=dict(email="test@example.com"))
    assert b"<title>GUDLFT Registration</title>" in response.data

def test_index(client):
    response = client.get("/")
    assert b"<title>GUDLFT Registration</title>" in response.data

def test_logout(client):
    response = client.get("/logout", follow_redirects=True)
    assert b"Welcome " in response.data

def test_book(client):
    response = client.get("/book/Spring%20Festival/Simply%20Lift")
    assert b"Book</button>" in response.data

def test_book_unknown_competition(client):
    response = client.get("/book/Unknown%20Competition/Simply%20Lift")
    # the page is not changing, so the title is still "Summary"
    assert b"Something went wrong-please try again" in response.data

def test_book_unknown_club(client):
    response = client.get("/book/Spring%20Festival/Unknown%20Club")
    # the page is not changing, so the title is still "Summary"
    assert b"Something went wrong-please try again" in response.data
