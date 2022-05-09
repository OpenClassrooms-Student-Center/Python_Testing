def test_index(client):
    response = client.get("/")
    data = response.data.decode()
    assert response.status_code == 200
    assert "Welcome to the GUDLFT Registration Portal!" in data
