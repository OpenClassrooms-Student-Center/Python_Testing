from flask import url_for


def test_showSummary_email_found(client, clubs):
    """
    Test if the show_summary route displays the correct information for a
    found email.

    This test checks if the show_summary route responds with a status code of
    200 and contains the expected information when a valid email is provided.

    Args:
    - client: A Flask test client for making HTTP requests.
    - clubs: A fixture providing mock data for clubs.
    """
    response = client.post(
        url_for("show_summary"), data={"email": "admin@irontemple.com"}
    )
    assert b"Welcome, Iron Temple" in response.data
    assert response.status_code == 200


def test_showSummary_wrong_or_email_not_found(client, clubs):
    """
    Test if the show_summary route redirects for a wrong or not found email.

    This test checks if the show_summary route responds with a status code of
    302 and contains the "Redirecting" message when an invalid or not found
    email is provided.

    Args:
    - client: A Flask test client for making HTTP requests.
    - clubs: A fixture providing mock data for clubs.
    """
    response = client.post(
        url_for("show_summary"), data={"email": "NoExist@email.com"}
    )
    assert b"Redirecting" in response.data
    assert response.status_code == 302


def test_showSummary_missing_email_field(client, clubs):
    """
    Test if the show_summary route redirects when the email field is missing.

    This test checks if the show_summary route responds with a status code
    of 302 when the email field is not provided in the POST request data.

    Args:
    - client: A Flask test client for making HTTP requests.
    - clubs: A fixture providing mock data for clubs.
    """
    response = client.post(url_for("show_summary"), data={})
    assert response.status_code == 302
