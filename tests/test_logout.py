import server


server.app.config["TESTING"] = True
client = server.app.test_client()


def test_if_url_redirect_after_logout():
    response = client.get("/logout/")
    assert response.status_code == 302
    assert response.headers.get("Location") == "/"


def test_if_redirected_template_is_index():
    response = client.get("/logout/", follow_redirects=True)
    assert response.status_code == 200
    assert b"Welcome to the GUDLFT Registration Portal!" in response.data
