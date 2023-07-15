from tests.config import client, existent_club, non_existent_club


def test_get_login_page_200(client):

    rv = client.get('/')
    assert rv.status_code == 200


def test_login_post_email_200(client, existent_club):

    rv = client.post("/showSummary",
                     data={"email": existent_club[2]["email"]},
                     follow_redirects=True)
    assert rv.status_code == 200
    data = rv.data.decode()
    assert f"You are connected as {existent_club[2]['email']}" in data


def test_login_post_email_401(client, non_existent_club):

    rv = client.post("/showSummary",
                     data={"email": non_existent_club[0]["email"]},
                     follow_redirects=True)
    assert rv.status_code == 401
    data = rv.data.decode()
    assert "Please enter a recognized email" in data


def test_logout_user(client):
    rv = client.get("/logout")
    assert rv.status_code == 302
