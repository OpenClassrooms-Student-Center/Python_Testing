from tests.tests_utils import decode_response
from http import HTTPStatus

def test_invalid_email(client):
    response = client.post(
        "/showSummary", data={"email": "invalid@example.com"}, follow_redirects=True
    )

    decoded_response = decode_response(response.data)

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert "Sorry, that email wasn't found." in decoded_response


def test_no_email(client):
    response = client.post("/showSummary", data={}, follow_redirects=True)

    decoded_response = decode_response(response.data)

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert "Sorry, that email wasn't found." in decoded_response


def test_email_valid(client):
    response = client.post(
        "/showSummary", data={"email": "book@test.srv"}, follow_redirects=True
    )

    decoded_response = decode_response(response.data)
    assert response.status_code == HTTPStatus.OK
    assert "Welcome, book@test.srv" in decoded_response


def test_logout(client):
    response = client.get("/logout")
    assert response.status_code == HTTPStatus.FOUND
