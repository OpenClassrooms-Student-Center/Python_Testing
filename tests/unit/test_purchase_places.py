from tests.tests_utils import decode_response

TEST_CLUB = {"name": "Test club", "email": "admin@admin.com", "points": "5"}

TEST_COMPETITION = {
    "name": "Test competition",
    "date": "2020-03-27 10:00:00",
    "numberOfPlaces": "10",
}

def test_not_enough_points(app):
    client = app.test_client()
    response = client.post(
        "/purchasePlaces",
        data={"competition": "Test competition", "club": "Test club", "places": "10"},
        follow_redirects=True,
    )

    decoded_response = decode_response(response.data)
    assert "Sorry you can't book more than 5 places." in decoded_response


def test_points_are_deducted_after_booking(app):
    client = app.test_client()
    response = client.post(
        "/purchasePlaces",
        data={"competition": "Test competition", "club": "Test club", "places": "3"},
        follow_redirects=True,
    )

    decoded_response = decode_response(response.data)
    assert "Points available: 2" in decoded_response
