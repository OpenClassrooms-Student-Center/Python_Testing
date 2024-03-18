def test_index(test_client):
    """Test the index route."""
    response = test_client.get("/")
    assert response.status_code == 200
    assert b"Welcome to the GUDLFT Registration Portal!" in response.data
