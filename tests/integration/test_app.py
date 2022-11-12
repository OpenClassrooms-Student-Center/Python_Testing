from conftest import get


"""
    Testing a complete smooth scenario of a user :
     * Home page
     * Login
     * book for a competition
     * purchase places
     * got to see display board
     * Logout

"""

# ================================================== START TESTING


def test_app(client, fixture):

    assert client.get('/').status_code == 200
    response = client.get('/')
    assert b'Welcome to the GUDLFT Registration' in response.data

    email = get(fixture, "email")
    response = client.post('/showSummary', data=email)
    assert response.status_code == 200

    data = get(fixture, "valid_club_competition")
    response = client.get(f"/book/{data['competition']}/{data['club']}")
    assert response.status_code == 200

    data = get(fixture, "club_competition_places", 5)
    response = client.post('/purchasePlaces', data=data)
    assert response.status_code == 200

    response = client.get('/board')
    clubs = get(fixture, "board")
    assert response.status_code == 200
    for club in clubs:
        assert club['name'] in response.data.decode()
        assert str(club["points"]) in response.data.decode()

    response = client.get('/logout')
    assert response.status_code == 302
    assert response.headers["Location"] == "/"
