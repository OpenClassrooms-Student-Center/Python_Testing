import pytest
import server


client = server.app.test_client()


@pytest.fixture
def clubs():
    yield server.clubs


def test_authenticate_club(clubs):
    response = client.post("/showSummary", data={"email": "admin@irontemple.com"})
    assert response.status_code == 200
    assert b"admin@irontemple.com" in response.data


def test_no_authenticate_club_for_invalid_email(clubs):
    response = client.post("/showSummary", data={"email": "test@test.com"})
    assert response.data not in clubs
