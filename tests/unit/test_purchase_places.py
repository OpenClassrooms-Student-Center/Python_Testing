from server import load_clubs, load_competitions


def test_purchase_first_time(auth, client, purchase):
    """
    GIVEN an existing user
    WHEN they attempt to purchase places for a competition for the first time
    THEN points and places are deduced and the competition is added to their profile
    """
    auth.login()
    response = purchase.purchase()
    db = load_clubs()

    assert response.status_code == 200
    assert b"Summary | GUDLFT Registration" in response.data
    assert b"Points available: 7" in response.data
    assert b"Number of Places: 3" in response.data
    assert db[0]['competitions'][2]['name'] == 'Frozen Drops'


def test_purchase_places_exists(auth, client, purchase):
    """
    GIVEN an existing user
    WHEN they attempt to purchase places for a competition they've already booked for
    THEN points and places are deduced
    """
    auth.login()
    response = purchase.purchase(places='1', club='Simply Lift', competition='Spring Festival')
    db_clubs = load_clubs()
    db_comp = load_competitions()

    assert response.status_code == 200
    assert b"Summary | GUDLFT Registration" in response.data
    assert b"Points available: 10" in response.data
    assert db_clubs[0]['competitions'][0]['places'] == '12'
    assert db_comp[0]['numberOfPlaces'] == '24'


def test_purchase_not_logged(client, purchase):
    """
    GIVEN a user not logged in
    WHEN they attempt to purchase places for a competition
    THEN they are redirected to the index page
    """
    response = purchase.purchase()
    assert response.status_code == 302
    assert "http://localhost/" == response.headers["Location"]


def test_purchase_too_much(auth, client, purchase):
    """
    GIVEN an existing user
    WHEN they attempt to purchase more places for a competition than possible
    THEN the attempt fails
    """
    auth.login()
    response = purchase.purchase('20')
    assert response.status_code == 200
    assert b"Summary | GUDLFT Registration" in response.data
    assert b"Not enough available places anymore" in response.data

def test_purchase_negative_number(auth, client, purchase):
    """
    GIVEN an existing user
    WHEN they attempt to purchase a negative amount of places
    THEN the attempt fails
    """
    auth.login()
    response = purchase.purchase('-6')
    assert response.status_code == 200
    assert b"Summary | GUDLFT Registration" in response.data
    assert b"Please purchase more than one place." in response.data
