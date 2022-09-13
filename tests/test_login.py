def test_index(client):
    response = client.get('/')
    assert response.status_code == 200


def test_login_with_valid_mail(client, valid_club):
    data = {
        "email": valid_club["email"]
    }
    response = client.post('/showSummary', data=data)
    assert response.status_code == 200


def test_login_with_invalid_mail(client, invalid_club):
    data = {
        "email": invalid_club["email"]
    }
    response = client.post('/showSummary', data=data)
    assert response.status_code == 404
