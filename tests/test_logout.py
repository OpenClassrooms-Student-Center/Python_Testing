from urllib.parse import urlparse


def test_logout_route_redirects_to_index(client):
    """
    Test if the logout route redirects to the index page.

    This test case simulates a GET request to the "/logout" route, checks that
    the response status code is a redirection code (302), and compares only the
    path of the redirection URL to ensure it leads to the index page.

    Args:
    - client: Flask test client.
    """
    response = client.get("/logout")
    assert response.status_code == 302
    assert urlparse(response.location).path == "/"


def test_logout_route_with_authenticated_user_redirects_to_index(client):
    """
    Test if the logout route redirects to the index page for an authenticated
    user.

    This test case simulates a GET request to the "/logout" route with an
    authenticated user, checks that the response status code is a redirection
    code (302), and compares only the path of the redirection URL to ensure
    it leads to the index page.

    Args:
    - client: Flask test client.
    """
    with client.session_transaction() as session:
        session["user"] = {"username": "example_user"}

    response = client.get("/logout")
    assert response.status_code == 302
    assert urlparse(response.location).path == "/"
