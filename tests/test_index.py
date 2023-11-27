def test_index_route(client):
    """
    Test the behavior of the index route.

    This test checks the response of the index route ("/"). It verifies that
    the response status code is 200 (OK), and it looks for specific content
    in the HTML response to ensure that the expected welcome message is present.

    Args:
    - client: The Flask test client.
    """
    response = client.get("/")
    assert response.status_code == 200
    assert b"<!DOCTYPE html>" in response.data
    assert b"Welcome to the GUDLFT Registration Portal!" in response.data
