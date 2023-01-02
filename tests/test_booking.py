from server import MAX_BOOKING
# They should not be able to redeem more points than available; this should be done within the UI. 
# The redeemed points should be correctly deducted from the club's total.


# book with sufficient points balance
def test_sufficient_points_balance_should_return_status_200(client):
    """
    Test club book a competition with sufficient points balance.
    """
    response= client.post('/purchasePlaces', data={
      "club": "She Lifts",
      "competition": "Spring Festival",
      "places": 12
    })
    assert response.status_code == 200


# book with insufficient points balance
def test_insufficient_points_balance_should_return_error(client):
    """
    Test club book a competition with insufficient points balance.
    """
    response= client.post('/purchasePlaces', data={
      "club": "She Lifts",
      "competition": "Spring Festival",
      "places": 16
    })
    assert response.status_code == 405
    # assert "You have " + response.data['points'] + " points which is not enough to book " + response.data['places'] + " places."  in response.data.decode('UTF-8')


# if placesRequired > availablePlaces
def test_required_places_superior_to_available_places_should_return_status_405(client):
    """
    Test club book more places than availables places.
    """
    response= client.post('/purchasePlaces', data={
      "club": "She Lifts",
      "competition": "Fall Classic",
      "places": 11
    })
    assert response.status_code == 405
    # assert "You can't book more places than availables competition places : " in response.data.decode('UTF-8')


def test_book_negative_number_of_places_should_return_error(client):
    """
    Test club book a negative number of places which is impossible.
    """
    response = client.post('/purchasePlaces', data={
      "club": "She Lifts",
      "competition": "Fall Classic",
      "places": -5
    })
    assert response.status_code == 405
    assert "Booking a negative number of places or 0 is forbidden." in response.data.decode('UTF-8')


# substract points from club when club books places
def test_booked_places_should_subtract_club_points(client):
    """
    Test deduction of club points when club books a competition
    with points of club = 15.  
    """
    response= client.post('/purchasePlaces', data={
      "club": "She Lifts",
      "competition": "Spring Festival",
      "places": 3
    })
    assert response.status_code == 200
    assert "Points available: 12" in response.data.decode('UTF-8')


# book more than max determinate places(12)
def test_booking_more_than_max_booking_places_should_return_error(client):
    """
    Test club books more than max_booking places in a competition.
    """
    response= client.post('/purchasePlaces', data={
      "club": "Simply Lift",
      "competition": "Spring Festival",
      "places": 13
    })
    assert response.status_code == 405
    assert "Booking more than " + str(MAX_BOOKING) + " places is forbidden." in response.data.decode('UTF-8')