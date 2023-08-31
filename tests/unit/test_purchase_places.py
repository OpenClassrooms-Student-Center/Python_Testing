from tests.tests_utils import decode_response


def test_not_enough_points(app):
    client = app.test_client()
    response = client.post(
        "/purchasePlaces",
        data={"competition": "empty", "club": "purchase_places", "places": "11"},
        follow_redirects=True,
    )

    decoded_response = decode_response(response.data)
    assert "Sorry you can't book more than 10 places." in decoded_response


def test_points_are_deducted_after_booking(app):
    client = app.test_client()
    response = client.post(
        "/purchasePlaces",
        data={"competition": "empty", "club": "purchase_places", "places": "1"},
        follow_redirects=True,
    )

    decoded_response = decode_response(response.data)
    assert "Points available: 9" in decoded_response
