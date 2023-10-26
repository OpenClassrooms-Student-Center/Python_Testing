import pytest
from server import app


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        with client.session_transaction() as session:
            # Configuration des messages flash
            session["message"] = []
        yield client


def test_showSummary_email_found(client):
    response = client.post(
        "/showSummary", data={"email": "admin@irontemple.com"}
    )
    assert b"Welcome" in response.data
    assert response.status_code == 200


def test_showSummary_email_not_found(client):
    response = client.post("/showSummary", data={"email": "NoExist@email.com"})
    assert b"Redirecting..." in response.data
    assert response.status_code == 302


def test_showSummary_expected_template(client):
    response = client.post(
        "/showSummary", data={"email": "admin@irontemple.com"}
    )
    assert b"Welcome, admin@irontemple.com" in response.data
    assert response.status_code == 200


def test_showSummary_flash_message(client):
    response = client.post("/showSummary", data={"email": "NoExist@email.com"})
    assert b"Redirecting..." in response.data
    assert response.status_code == 302


def test_showSummary_missing_email_field(client):
    response = client.post("/showSummary", data={})
    assert b"400 Bad Request" in response.data
    assert response.status_code == 400
