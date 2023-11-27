def test_purchase_places_valid_booking(client, competitions, clubs):
    """
    Test if the purchase_places route books places successfully with valid
    input.

    This test case simulates a POST request to the "/purchasePlaces" route
    with valid input, checks that the response status code is 200,
    and verifies that the flash message indicates a successful booking.

    Args:
    - client: Flask test client.
    """
    with client.session_transaction() as session:
        session["user"] = {"username": "example_user"}

    response = client.post(
        "/purchasePlaces",
        data={
            "competition": "Spring Festival",
            "club": "Simply Lift",
            "places": "5",
        },
    )
    assert response.status_code == 200
    assert b"You have booked 5 places for Spring Festival!" in response.data
    assert b"Welcome" in response.data


def test_purchase_places_invalid_booking(client, competitions, clubs):
    """
    Test if the purchase_places route handles invalid booking conditions.

    This test case simulates a POST request to the "/purchasePlaces" route
    with invalid booking conditions,
    checks that the response status code is 200,
    and verifies that the flash message indicates the reason for the failure.

    Args:
    - client: Flask test client.
    """
    with client.session_transaction() as session:
        session["user"] = {"username": "example_user"}

    response = client.post(
        "/purchasePlaces",
        data={
            "competition": "Fall Classic",
            "club": "Simply Lift",
            "places": "30",
        },
    )
    assert response.status_code == 200

    assert b'<!DOCTYPE html>\n<html lang="en">'
    assert b"Sorry, you booked more places than available!"
    assert b"booking"
