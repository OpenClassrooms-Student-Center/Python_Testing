from tests.tests_utils import decode_response


def test_purchase_no_club(app):
    client = app.test_client()

    response = client.post(
        "/purchasePlaces",
        data={"competition": "empty", "places": "11"},
        follow_redirects=True,
    )
    decoded_response = decode_response(response.data)

    assert "Something went wrong-please try again" in decoded_response


def test_purchase_non_existing_club(app):
    client = app.test_client()

    response = client.post(
        "/purchasePlaces",
        data={"competition": "empty", "club": "DoesntExist", "places": "11"},
        follow_redirects=True,
    )
    decoded_response = decode_response(response.data)

    assert "Something went wrong-please try again" in decoded_response


def test_purchase_no_competition(app):
    client = app.test_client()

    response = client.post(
        "/purchasePlaces",
        data={"club": "purchase_place", "places": "11"},
        follow_redirects=True,
    )
    decoded_response = decode_response(response.data)

    assert "Something went wrong-please try again" in decoded_response


def test_purchase_non_existing_competition(app):
    client = app.test_client()

    response = client.post(
        "/purchasePlaces",
        data={"competition": "DoesntExist", "club": "purchase_places", "places": "11"},
        follow_redirects=True,
    )
    decoded_response = decode_response(response.data)

    assert "Something went wrong-please try again" in decoded_response


def test_purchase_competition_over(app):
    client = app.test_client()

    response = client.post(
        "/purchasePlaces",
        data={"competition": "over", "club": "purchase_places", "places": "1"},
        follow_redirects=True,
    )
    decoded_response = decode_response(response.data)
    print(decoded_response)
    assert "Something went wrong-please try again" in decoded_response

def test_purchase_no_places(app):
    client = app.test_client()

    response = client.post(
        "/purchasePlaces",
        data={"competition": "empty", "club": "purchase_places"},
        follow_redirects=True,
    )
    decoded_response = decode_response(response.data)
    assert "Please provide a valid rounded number" in decoded_response


def test_purchase_non_numerical_number_of_places(app):
    client = app.test_client()

    response = client.post(
        "/purchasePlaces",
        data={"competition": "empty", "club": "purchase_places", "places": "€"},
        follow_redirects=True,
    )
    decoded_response = decode_response(response.data)

    assert "Please provide a valid rounded number" in decoded_response


def test_purchase_non_int_number_of_places(app):
    client = app.test_client()

    response = client.post(
        "/purchasePlaces",
        data={"competition": "empty", "club": "purchase_places", "places": "1.1"},
        follow_redirects=True,
    )
    decoded_response = decode_response(response.data)
    assert "Please provide a valid rounded number" in decoded_response


def test_not_enough_places_for_purchase(app):
    client = app.test_client()
    response = client.post(
        "/purchasePlaces",
        data={"competition": "full", "club": "purchase_places", "places": "1"},
        follow_redirects=True,
    )

    decoded_response = decode_response(response.data)
    assert "Sorry this competition is already full." in decoded_response


def test_purchase_more_than_allowed_places(app):
    client = app.test_client()
    response = client.post(
        "/purchasePlaces",
        data={"competition": "full", "club": "purchase_places", "places": "15"},
        follow_redirects=True,
    )

    decoded_response = decode_response(response.data)
    assert "Sorry you can't book more than 12 places" in decoded_response


def test_not_enough_points_for_purchase(app):
    client = app.test_client()
    response = client.post(
        "/purchasePlaces",
        data={"competition": "empty", "club": "purchase_places", "places": "11"},
        follow_redirects=True,
    )

    decoded_response = decode_response(response.data)
    assert "Sorry you can't book more than 10 places" in decoded_response


def test_points_are_deducted_after_booking(app):
    client = app.test_client()
    response = client.post(
        "/purchasePlaces",
        data={"competition": "empty", "club": "purchase_places", "places": "1"},
        follow_redirects=True,
    )

    decoded_response = decode_response(response.data)
    assert "Points available: 9" in decoded_response
