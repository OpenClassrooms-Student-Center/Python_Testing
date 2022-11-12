from conftest import get


def test_purchase_with_enough_points(client, fixture):
    """
        GIVEN a connected secretary's club has 15 points.
        WHEN this secretary types: 10 places to book for
            a competition who has 20 places available,
        THEN the places are successfully purchased with success message.
    """
    data = get(fixture, "club_competition_places", 10)
    response = client.post('/purchasePlaces', data=data)

    assert response.status_code == 200
    assert f"Great you have booked {data['places']} places!" in response.data.decode()


def test_purchase_not_enough_points(client, fixture):
    """
        GIVEN a connected secretary's club has 6 points.
        WHEN this secretary types: 10 places to book for
            a competition who has 20 places available,
        THEN an error message displays, with status code:400 BAD REQUEST.
    """
    data = get(fixture, "small_club_places", 10)
    response = client.post('/purchasePlaces', data=data)

    assert response.status_code == 400
    assert b"Sorry, your club doesn&#39;t have enough points !" in response.data
