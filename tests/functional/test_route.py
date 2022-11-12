from conftest import get

"""
functionnal test of all routes of the app
    *'/'
    *'/showSummary'
    *'/book/<competition>/<club>'
    *'/purchasePlaces'
    */board'
    */logout'
"""


def test_uknown_route(client):
    assert client.get('/fakeRoute').status_code == 404


# ================================================== TEST FOR '/'


def test_route_index(client):
    assert client.get('/').status_code == 200


def test_render_template_index(client):
    response = client.get('/')
    assert b'Welcome to the GUDLFT Registration' in response.data

# ================================================== TEST FOR '/showSummary'


def test_route_showSummary(client, fixture):

    email = get(fixture, "email")
    response = client.post('/showSummary', data=email)

    assert response.status_code == 200


# ================================================== TEST FOR '/book/<competition>/<club>'


def test_route_book(client, fixture):

    data = get(fixture, "valid_club_competition")
    response = client.get(f"/book/{data['competition']}/{data['club']}")

    assert response.status_code == 200


# ================================================== TEST FOR '/purchasePlaces'


def test_route_purchasePlaces(client, fixture):

    data = get(fixture, "club_competition_places", 5)
    response = client.post('/purchasePlaces', data=data)

    assert response.status_code == 200

# ================================================== TEST FOR  /board'


def test_route_board(client):
    response = client.get('/board')
    assert response.status_code == 200


def test_render_template_board(client, fixture):

    clubs = get(fixture, "board")
    response = client.get('/board')
    for club in clubs:
        assert club['name'] in response.data.decode()
        assert str(club["points"]) in response.data.decode()

# ================================================== TEST FOR */logout'


def test_route_logout(client):

    response = client.get('/logout')
    assert response.status_code == 302
    assert response.headers["Location"] == "/"
