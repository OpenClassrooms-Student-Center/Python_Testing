from tests.tests_utils import decode_response


def test_invalid_email(app):
    client = app.test_client()
    response = client.post(
        "/showSummary", data={"email": "invalid@example.com"}, follow_redirects=True
    )

    decoded_response = decode_response(response.data)

    assert "Sorry, that email wasn't found." in decoded_response


def test_no_email(app):
    client = app.test_client()
    response = client.post("/showSummary", data={}, follow_redirects=True)

    decoded_response = decode_response(response.data)

    assert "Sorry, that email wasn't found." in decoded_response


def test_email_valid(app):
    client = app.test_client()
    response = client.post(
        "/showSummary", data={"email": "book@test.srv"}, follow_redirects=True
    )

    decoded_response = decode_response(response.data)
    assert "Welcome, book@test.srv" in decoded_response


def test_logout(app):
    client = app.test_client()
    response = client.get("/logout", follow_redirects=True)

    decoded_response = decode_response(response.data)
    assert "Welcome to the GUDLFT Registration Portal!" in decoded_response
