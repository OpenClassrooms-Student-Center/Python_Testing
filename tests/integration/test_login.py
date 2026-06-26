def test_login_with_valid_email_shows_summary(client):
    """Happy path : un email connu doit afficher la page de résumé."""
    response = client.post(
        "/showSummary",
        data={"email": "john@simplylift.co"},
    )
    assert response.status_code == 200
    assert b"john@simplylift.co" in response.data


def test_login_with_unknown_email_does_not_crash(client):
    """Sad path (bug #1) : un email inconnu ne doit pas faire planter l'appli."""
    response = client.post(
        "/showSummary",
        data={"email": "inconnu@test.com"},
        follow_redirects=True,
    )
    assert response.status_code == 200
    assert b"Sorry, that email was not found." in response.data