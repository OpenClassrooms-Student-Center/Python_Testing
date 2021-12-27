def test_full_display(client, auth):
    auth.login()
    response = client.get('/fullDisplay')

    assert response.status_code == 200
    assert b"Current Point Count" in response.data
    assert b"Simply Lift" in response.data
    assert b"Points: 13" in response.data
    assert b"Iron Temple" in response.data
    assert b"She Lifts" in response.data


def test_full_display_unlogged(client, auth):
    """
    GIVEN an unlogged user
    WHEN they attempt to access /fullDisplay
    THEN redirect them to the index
    """
    response = client.get('/fullDisplay')
    assert response.status_code == 302
    assert "http://localhost/" == response.headers["Location"]
