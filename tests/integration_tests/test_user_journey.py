from tests.config import client, existent_club, existent_competition


def test_user_journey(client, existent_club, existent_competition):

    """
    User journey :
    1. Check clubs points board
    2. Login as "Test Club 01"
    3. Select and check book "Competition test 01"
    4. Buy 3 places for "Competition test 01"
    5. logout
    6. Recheck clubs points board and note difference in points for club "Test Club 01" due to the last purchase
    """

    """
    1. Check clubs points board
    """
    rv = client.get("/clubsPointsBoard")
    assert rv.status_code == 200
    data = rv.data.decode()
    for i in range(len(existent_club)):
        assert existent_club[i]["name"], existent_club[i]["points"] in data

    """
    2. Login as "Test Club 01"
    """
    rv = client.post("/showSummary",
                     data={"email": existent_club[0]["email"]},
                     follow_redirects=True)
    assert rv.status_code == 200
    data = rv.data.decode()
    assert f"You are connected as {existent_club[0]['email']}" in data

    """
    3. Select and check book "Competition test 01"
    """
    rv = client.get(
        f"/book/{existent_competition[0]['name']}"
        f"/{existent_club[0]['name']}")
    assert rv.status_code == 200
    data = rv.data.decode()
    assert existent_competition[0]['name'] in data
    assert existent_club[0]['name'] in data

    """
    4. Buy 3 places for "Competition test 01" as "Test Club 01"
    """
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

    """
    5. logout
    """
    rv = client.get("/logout")
    assert rv.status_code == 302

    """
    6. Recheck clubs points board and note difference in points for club "Test Club 01" due to the last purchase
    """
    rv = client.get("/clubsPointsBoard")
    assert rv.status_code == 200
    data = rv.data.decode()
    for i in range(len(existent_club)):
        assert existent_club[i]["name"], existent_club[i]["points"] in data
    data_rep_blank = data.replace(" ", "")
    data_rep_line_break = data_rep_blank.replace("\n", "")
    assert f"{existent_club[0]['name'].replace(' ', '')}</td><td>{compared_var_deduct}" in data_rep_line_break
