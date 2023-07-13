from tests.config import client, existent_club, existent_competition


def test_purchase_places_post_200(client, existent_club, existent_competition):
    # Success purchase place
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


def test_purchase_places_outdated_book_400(client, existent_club, existent_competition):
    # Error if try to purchase outdated places
    rv = client.post("/purchasePlaces",
                     data={"club": existent_club[0]["name"],
                           "competition": existent_competition[2]["name"],
                           "places": 1
                           })
    assert rv.status_code == 400
    data = rv.data.decode()
    assert 'Cannot buy places, this book is obsolete, please select one that has not already passed' in data



def test_purchase_place_deduct_points_club_200(client, existent_club, existent_competition):
    # Test and success if points deduction is taken into club balance account
    compared_var = int(existent_club[0]["points"])
    places_purchased = int(3)
    compared_var_deduct = compared_var - places_purchased
    rv = client.post("/purchasePlaces",
                     data={"club": existent_club[0]["name"],
                           "competition": existent_competition[0]["name"],
                           "places": places_purchased
                           })
    assert rv.status_code == 200
    data = rv.data.decode()
    assert "Great-booking complete!" in data
    assert f"Points available: {compared_var_deduct}" in data


def test_purchase_place_deduct_places_competition_200(client, existent_club, existent_competition):
    # Test and success if places deduction is taken into competition balance account
    compared_var = int(existent_competition[0]["numberOfPlaces"])
    places_purchased = int(3)
    compared_var_deduct = compared_var - places_purchased
    rv = client.post("/purchasePlaces",
                     data={"club": existent_club[0]["name"],
                           "competition": existent_competition[0]["name"],
                           "places": places_purchased
                           })
    assert rv.status_code == 200
    data = rv.data.decode()
    assert "Great-booking complete!" in data
    data_rep_blank = data.replace(" ", "")
    data_rep_line_break = data_rep_blank.replace("\n", "")
    assert f"{existent_competition[0]['name'].replace(' ', '')}<br/>Date:2030-10-2213:30:00</br>NumberofPlaces:{compared_var_deduct}" in data_rep_line_break


