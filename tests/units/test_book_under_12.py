from conftest import get


def test_purchase_more_in_one_step(client, fixture):
    """
        GIVEN a connected secretary's club has 15 points.
        WHEN this secretary types: 13 places to book for
            a competition who has 20 places available,
        THEN an error message displays, with status code:400 BAD REQUEST.
    """
    data = get(fixture, "club_competition_places", 13)
    response = client.post('/purchasePlaces', data=data)

    assert response.status_code == 400
    assert b'Sorry, you can&#39;t book more than 12 places !' in response.data


def test_purchase_more_in_two_step(client, fixture):
    """
        GIVEN a connected secretary's club has 15 points.
        FIRST REQUEST :
            WHEN this secretary types: 10 places to book for
                a competition who has 20 places available,
            THEN places are pruchased.

        SECOND REQUEST :
            WHEN this secretary types: 3 places to book for the same competition,
            THEN an error message displays, with status code:400 BAD REQUEST.
    """
    data = get(fixture, "club_competition_places", 10)
    response = client.post('/purchasePlaces', data=data)

    data = get(fixture, "club_competition_places", 3)
    response = client.post('/purchasePlaces', data=data)

    assert response.status_code == 400
    assert b"Sorry, you have already booked places, for this competition" in response.data
