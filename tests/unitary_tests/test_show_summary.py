"""
Testing the '/showSummary' endpoint.
First issue:
- Entering an unknown email crashes the app
"""


def test_show_summary_with_existing_email(client):
    email = "john@simplylift.co"
    response = client.post("/showSummary", data={"email": email}, follow_redirects=True)
    data = response.data.decode()
    assert response.status_code == 200


def test_show_summary_with_non_existing_email(client):
    email = "test@gmail.com"
    response = client.post("/showSummary", data={"email": email}, follow_redirects=True)
    data = response.data.decode()
    assert "This email does not exist." in data
    assert response.status_code == 200
