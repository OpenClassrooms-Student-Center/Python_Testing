def test_valid_email(client):
    response = client.post("/showSummary", data={"email": "john@simplylift.co"})
    data = response.data.decode()
    assert "Welcome" in data


def test_wrong_email(client):
    response = client.post("/showSummary", data={"email": "jane@simplylift.co"})
    data = response.data.decode()
    assert "Email not found" in data
