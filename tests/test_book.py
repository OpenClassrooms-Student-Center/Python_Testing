from server import Flask


def test_book_route(client, clubs, competitions):
    """
    Test the book route functionality.

    This function simulates a GET request to the book route for a given
    competition and club, checking that the response contains the expected
    HTML elements and information.

    Parameters:
    - client (FlaskClient): The Flask test client.
    - clubs (dict): Dictionary containing club data.
    - competitions (dict): Dictionary containing competition data.

    Returns:
    None: This function asserts conditions about the response.

    Raises:
    AssertionError: If any of the expected conditions are not met.
    """
    Flask(__name__)

    club = clubs["clubs"][0]
    competition = competitions["competitions"][0]

    response = client.get(
        f"/book/{competition['name']}/{club['name']}",
        data=dict(clubs=clubs, competitions=competitions),
    )

    assert response.status_code == 200
    assert (
        f'<input type="hidden" name="club" value="{club["name"]}">'
        in response.get_data(as_text=True)
    )
    assert club["name"] in response.get_data(as_text=True)

    assert (
        f'<input type="hidden" name="competition" value="{competition["name"]}">'
        in response.get_data(as_text=True)
    )
    assert competition["name"] in response.get_data(as_text=True)

    response_invalid_club = client.get(
        f"/book/{competition['name']}/InvalidClub",
        data=dict(clubs=clubs, competitions=competitions),
    )
    assert response_invalid_club.status_code == 200
    assert (
        "Something went wrong - please try again"
        in response_invalid_club.get_data(as_text=True)
    )
