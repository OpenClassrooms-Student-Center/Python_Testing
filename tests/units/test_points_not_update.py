from conftest import get


def test_points_update_correctly(client, fixture):
    """
        GIVEN a connected secretary's club has 15 points,
        he/she purchased 5 places,
        for a competition who has 20 places available,
        WHEN this secretary click on book button,
        THEN club's points are updated and been displayed on response page.
    """
    data = get(fixture, "club_competition_places", 5)
    response = client.post('/purchasePlaces', data=data)

    assert response.status_code == 200
    assert f"Points available: {fixture[1][0]['points']}" in response.data.decode()
