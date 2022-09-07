

def test_should_return_200_on_login_page(client):

    response = client.get('/')
    assert response.status_code == 200
    assert "Welcome to the GUDLFT Registration Portal!" in response.text


def test_should_return_401_with_unknown_mail(client):

    data = {"email": "unknownemail@email.fr"}
    response = client.post("/showSummary", data=data, follow_redirects=True)
    assert response.status_code == 401


def test_should_return_200_with_known_email(client):

    data = {"email": "john@simplylift.co"}
    response = client.post("/showSummary", data=data, follow_redirects=True)
    assert response.status_code == 200
    assert "Welcome, john@simplylift.co" in response.text


def test_should_return_302_on_logout(client):

    data = {"email": "john@simplylift.co"}
    client.post("/showSummary", data=data, follow_redirects=True)
    response = client.get("/logout", follow_redirects=False)
    assert response.status_code == 302