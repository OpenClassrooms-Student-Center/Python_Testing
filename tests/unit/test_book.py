from http import HTTPStatus

from tests.tests_utils import decode_response


def test_book_competition_over(client):
    response = client.get(
        f"/book/over/book",
        follow_redirects=True,
    )

    decoded_response = decode_response(response.data)

    assert (
        "Sorry, this competition is over, places are not available anymore."
        in decoded_response
    )
    assert response.status_code == HTTPStatus.BAD_REQUEST


def test_book_competition_going(client):
    response = client.get(
        f"/book/going/book",
        follow_redirects=True,
    )

    decoded_response = decode_response(response.data)
    assert f"This competition is open until" in decoded_response
    assert response.status_code == HTTPStatus.OK


def test_book_non_existing_competition(client):
    response = client.get(
        f"/book/DoesntExist/book",
        follow_redirects=True,
    )

    decoded_response = decode_response(response.data)

    assert "Something went wrong-please try again" in decoded_response
    assert response.status_code == HTTPStatus.BAD_REQUEST


def test_book_non_existing_club(client):
    response = client.get(
        f"/book/empty/DoesntExist",
        follow_redirects=True,
    )

    decoded_response = decode_response(response.data)

    assert "Something went wrong-please try again" in decoded_response
    assert response.status_code == HTTPStatus.BAD_REQUEST
