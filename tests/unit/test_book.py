def test_book_get(client, auth):
    auth.login()
    response = client.get('/book/Frozen Drops/Simply Lift')
    assert response.status_code == 200
    assert b"Booking for Frozen Drops" in response.data


def test_book_not_logged(client, auth):
    response = client.get('/book/Frozen Drops/Simply Lift')
    assert "http://localhost/" == response.headers["Location"]


def test_book_wrong_club(client, auth):
    """
    GIVEN an existing user
    WHEN they attempt to access /book and the club in the URL's not their own
    THEN redirect them to the index
    """
    auth.login()
    response = client.get('/book/Frozen Drops/Iron Temple')
    assert "http://localhost/" == response.headers["Location"]


def test_book_past_competition(client, auth):
    auth.login()
    response = client.get('/book/Fall Classic/Simply Lift', follow_redirects=True)
    assert response.status_code == 200
    assert b"You cannot book places for a past event." in response.data
    assert b"Summary | GUDLFT Registration" in response.data


def test_book_already_bought_all_places(client, auth):
    auth.login()
    response = client.get('/book/Sweaty Summer/Simply Lift', follow_redirects=True)
    assert response.status_code == 200
    assert b"Clubs - Full Display" in response.data
    assert b"You have already booked 12 places!" in response.data


def test_check_max_selector(auth, client):
    """
    GIVEN an existing user
    WHEN they attempt to purchase places for a competition
    THEN the max number of places they can purchase is the lower one between
    MAX_CLUB_POINTS, their points and the number of available places
    """
    auth.login()
    # If the club points are the lowest factor (5 places available, only 12 clubs points)
    response = client.get('/book/Frozen Drops/Simply Lift', follow_redirects=True)
    assert b'min="1" max=4' in response.data
    # If MAX_BOOKED_PLACES is the lowest factor (the club already booked 11 places)
    response = client.get('/book/Spring Festival/Simply Lift', follow_redirects=True)
    assert b'min="1" max=1' in response.data
