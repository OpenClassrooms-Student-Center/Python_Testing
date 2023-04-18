import pytest
import server


server.app.config["TESTING"] = True
client = server.app.test_client()


@pytest.fixture
def clubs():
    yield server.clubs


def test_check_if_a_club_email_exists(clubs):
    response = client.post("/showSummary", data={
        'email': "admin@irontemple.com"
    })
    assert response.status_code == 200
    assert b"admin@irontemple.com" in response.data


def test_check_if_a_club_email_does_not_exists(clubs):
    response = client.post("/showSummary", data={
        'email': "admin@irontemple.com"
    })
    assert response.data not in clubs
