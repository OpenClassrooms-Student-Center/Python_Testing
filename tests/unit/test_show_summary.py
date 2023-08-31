from tests.tests_utils import decode_response


def test_invalid_email(app):
    client = app.test_client()
    response = client.post(
        "/showSummary", data={"email": "invalid@example.com"}, follow_redirects=True
    )

    decoded_response = decode_response(response.data)

    assert "Sorry, that email wasn't found." in decoded_response
