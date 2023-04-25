import pytest
import server


server.app.config["TESTING"] = True
client = server.app.test_client()


def test_if_url_redirect_after_logout():
    response = client.get("/logout/")
    assert response.status_code == 302
    assert response.headers.get('Location') == "/"
