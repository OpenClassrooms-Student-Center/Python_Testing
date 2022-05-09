def test_logout(client):
    response = client.get("/logout")
    data = response.data.decode()
    assert response.status_code == 302
    assert "Redirecting..." in data
