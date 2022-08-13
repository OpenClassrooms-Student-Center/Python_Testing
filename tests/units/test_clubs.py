def test_should_purchase_place(client):
    """Test buying basic reservations"""
    response = client.post('/purchasePlaces', data = {
      "club": "Simply Lift",
      "competition": "Spring Festival",
      "places": 10
    })
    assert response.status_code == 200
    assert 'Great-booking complete!' in response.text


def test_should_not_enought_club_points(client):
    """Test buy more places than available club points"""
    response = client.post('/purchasePlaces', data = {
      "club": "Simply Lift",
      "competition": "Spring Festival",
      "places": 20
    })
    assert response.status_code == 200
    assert 'You cannot use more points then you have !' in response.text


def test_should_not_enought_competition_points(client):
    """Test buy more places than available"""
    response = client.post('/purchasePlaces', data = {
      "club": "Simply Lift",
      "competition": "Test Competition",
      "places": 12
    })
    assert response.status_code == 200
    assert 'This competition does not have enough places' in response.text


def test_should_deduct_competition_points(client):
    """Test for deduct 2 points of Test Competition"""
    data = {
      "club": "Simply Lift",
      "competition": "Test Competition",
      "places": 2
    }

    response = client.post('/purchasePlaces', data=data)
    assert response.status_code == 200
    assert ('Number of Places: 6' + '\n            \n                '
    + '<a href="/book/Test%20Competition/Simply%20Lift">') in response.text


def test_should_deduct_club_points(client):
    """Test for deduct 2 points of Simply Lift club """
    data = {
      "club": "Simply Lift",
      "competition": "Test Competition",
      "places": 2
    }

    response = client.post('/purchasePlaces', data=data)
    assert response.status_code == 200
    assert 'Points available: 11' in response.text


def test_should_not_take_more_than_12_places(client):
    
    response = client.post('/purchasePlaces', data = {
        "competition": "Spring Festival",
        "club": "Simply Lift",
        "places": 13
        })
    
    assert response.status_code == 200
    assert 'You cannot take more than 12 places' in response.text


def test_should_not_accept_negative_numbers(client):

    response = client.post('/purchasePlaces', data = {
        "competition": "Spring Festival",
        "club": "Simply Lift",
        "places": -2
        })
    
    assert response.status_code == 200
    assert 'You cannot enter negative number' in response.text


def test_should_raise_error(client):

    response = client.get('book/Futur Competition/Simply Bug')
    assert 'Something went wrong-please try again' in response.text


def test_should_return_200_on_booking(client):

    response = client.get('book/Test Competition/Simply Lift')
    assert response.status_code == 200
    assert 'Test Competition' in response.text
