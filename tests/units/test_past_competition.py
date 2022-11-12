from conftest import get


def test_purchase_futur_competition(client, fixture):
    """
        GIVEN a connected secretary's club wants to book places in a futur competition.
        date of this competition = "2023-02-05 10:00:00".
        WHEN this secretary types: 5 places
        THEN places are pruchased with status code:200.
    """
    data = get(fixture, "club_competition_places", 5)
    response = client.post('/purchasePlaces', data=data)

    assert response.status_code == 200
    assert f"Great you have booked {data['places']} places!" in response.data.decode()


def test_purchase_past_competition(client, fixture):
    """
        GIVEN a connected secretary's club wants to book places in a past competition.
        date of this competition = "2021-05-12 09:00:00".
        WHEN this secretary types: 5 places
        THEN an error message displays, with status code:400 BAD REQUEST.
    """
    data = get(fixture, "past_competition_places", 5)
    response = client.post('/purchasePlaces', data=data)

    assert response.status_code == 400
    assert b'Sorry, this competition is over !' in response.data
