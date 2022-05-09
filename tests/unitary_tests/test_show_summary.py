"""
Testing the '/showSummary' endpoint.
First issue:
- Entering an unknown email crashes the app
"""
from tests.conftest import mock_clubs_and_competitions


def test_show_summary_with_existing_email(client, mock_clubs_and_competitions):
    email = "yipman@grandmaster.cn"
    response = client.post("/showSummary", data={"email": email}, follow_redirects=True)
    data = response.data.decode()
    assert response.status_code == 200
    assert "yipman@grandmaster.cn" in data


def test_show_summary_with_non_existing_email(client):
    email = "non_existing@mail.com"
    response = client.post("/showSummary", data={"email": email}, follow_redirects=True)
    data = response.data.decode()
    assert "This email does not exist." in data
    assert response.status_code == 200
