from tests.tests_utils import decode_response

TEST_CLUB = {"name": "Test club", "email": "admin@admin.com", "points": "5"}

TEST_COMPETITION_OVER = {
    "name": "Test competition",
    "date": "2020-03-27 10:00:00",
    "numberOfPlaces": "10",
}

TEST_COMPETITION_GOING = {
    "name": "Test competition going",
    "date": "2026-03-27 10:00:00",
    "numberOfPlaces": "10",
}


def test_book_competition_over(app):
    client = app.test_client()
    response = client.get(
        f"/book/{TEST_COMPETITION_OVER['name']}/{TEST_CLUB['name']}",
        follow_redirects=True,
    )

    decoded_response = decode_response(response.data)

    assert (
        "Sorry, this competition is over, places are not available anymore."
        in decoded_response
    )


def test_book_competition_going(app):
    client = app.test_client()
    response = client.get(
        f"/book/{TEST_COMPETITION_GOING['name']}/{TEST_CLUB['name']}",
        follow_redirects=True,
    )

    decoded_response = decode_response(response.data)

    assert (
        f"This competition is open until {TEST_COMPETITION_GOING['date']}."
        in decoded_response
    )
