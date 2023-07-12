from tests.config import client, existent_club, existent_competition


def test_purchase_places_post_200(client, existent_club, existent_competition):
    rv = client.post("/purchasePlaces",
                     data={"club": existent_club[0]["name"],
                           "competition": existent_competition[0]["name"],
                           "places": 2
                           })
    assert rv.status_code == 200
    data = rv.data.decode()
    assert "Great-booking complete!" in data


def test_purchase_places_post_under_zero_input_400(client, existent_club, existent_competition):
    # If the club does not have enough points
    rv = client.post("/purchasePlaces",
                     data={"club": existent_club[0]["name"],
                           "competition": existent_competition[0]["name"],
                           "places": -5,
                           })
    assert rv.status_code == 400
    data = rv.data.decode()
    assert "Please, enter an integer greater than 0 as value" in data


def test_purchase_places_post_not_enough_point_400(client, existent_club, existent_competition):
    # If the club does not have enough points
    rv = client.post("/purchasePlaces",
                     data={"club": existent_club[2]["name"],
                           "competition": existent_competition[0]["name"],
                           "places": 2,
                           })
    assert rv.status_code == 400
    data = rv.data.decode()
    assert "Not enough points available for this purchase" in data


def test_purchase_places_post_not_enough_places_400(client, existent_club, existent_competition):
    # If the competition does not have enough places
    rv = client.post("/purchasePlaces",
                     data={"club": existent_club[0]["name"],
                           "competition": existent_competition[1]["name"],
                           "places": 2
                           })
    assert rv.status_code == 400
    data = rv.data.decode()
    assert "Not enough places available for this purchase" in data


def test_purchase_places_post_more_than_12_places_400(client, existent_club, existent_competition):
    # If the secretary try to buy more than 12 places from the same competition
    rv = client.post("/purchasePlaces",
                     data={"club": existent_club[0]["name"],
                           "competition": existent_competition[0]["name"],
                           "places": 13
                           })
    assert rv.status_code == 400
    data = rv.data.decode()
    assert "You cannot buy more than 12 tickets from the same competition" in data