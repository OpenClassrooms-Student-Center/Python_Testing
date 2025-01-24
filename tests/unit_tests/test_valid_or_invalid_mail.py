import pytest

def test_connection_with_valid_email(client):
    result = client.post("/showSummary", data={"email": "john@simplylift.co"})
    assert result.status_code == 200
    assert f"john@simplylift.co" in result.data.decode()

def test_connection_with_invalid_email_no_at(client):
    result = client.post("/showSummary", data={"email": "johnsimplylift.co"})
    assert result.status_code == 302

def test_connection_with_invalid_email_no_dot(client):
    result = client.post("/showSummary", data={"email": "john@simplyliftco"})
    assert result.status_code == 302

def test_connection_with_empty_email(client):
    result = client.post("/showSummary", data={"email": ""})
    assert result.status_code == 302

def test_logout(client):
    result = client.get("/logout")
    assert result.status_code == 302