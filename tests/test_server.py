from source import load_clubs, load_competitions


"""Importation tests"""


def test_importing_list_of_clubs():
    clubs = load_clubs()
    assert clubs[0]["email"] == "john@simplylift.co"


def test_importing_list_of_competitions():
    competitions = load_competitions()
    assert competitions[0]["name"] == "Spring Festival"


"""Email tests"""


def test_entering_valid_email(client):
    response = client.post("/showSummary", data={"email": "john@simplylift.co"})
    data = response.data.decode()
    assert "Logout" in data


def test_entering_invalid_email(client):
    response = client.post("/showSummary", data={"email": "wrong@simplylift.co"})
    data = response.data.decode()
    assert "Welcome to the GUDLFT Registration Portal!" in data


"""Purchasing tests"""


def test_club_has_enought_points_to_purchase(client):
    response = client.post(
        "/purchasePlaces",
        data={"competition": "Spring Festival", "club": "Iron Temple", "places": "5"},
    )
    data = response.data.decode()
    assert (
        "You don&#39;t have enough points to purchase this amount of places !" in data
    )


def test_there_is_enought_places_for_a_competition(client):
    response = client.post(
        "/purchasePlaces",
        data={
            "competition": "Fall Classic",
            "club": "Simply Lift",
            "places": "7",
        },
    )
    data = response.data.decode()
    assert "There isn&#39;t enough places left for this competitions !" in data


def test_buying_more_than_12_places_is_forbidden(client):
    response = client.post(
        "/purchasePlaces",
        data={
            "competition": "Spring Festival",
            "club": "Simply Lift",
            "places": "13",
        },
    )
    data = response.data.decode()
    assert "You can&#39;t purchase more than 12 places !" in data


def test_buying_successfully_buying_places(client):
    response = client.post(
        "/purchasePlaces",
        data={
            "competition": "Spring Festival",
            "club": "Simply Lift",
            "places": "5",
        },
    )
    data = response.data.decode()
    assert "Great-booking complete !" in data


"""Date of competition tests"""


def test_competition_didnt_happen_yet(client):
    response = client.get("/book/Spring Festival/Simply Lift")
    data = response.data.decode()
    assert "How many places?" in data


def test_competition_already_happened(client):
    response = client.get("/book/Fall Classic/Simply Lift")
    data = response.data.decode()
    assert "You can&#39;t book places if the competition already started" in data


"""Changing the amount of points test"""


def test_amount_of_points_is_changing_after_purchase(client):
    response = client.post(
        "/purchasePlaces",
        data={
            "competition": "Spring Festival",
            "club": "She Lifts",
            "places": "2",
        },
    )
    data = response.data.decode()
    assert "Points available: 6" in data


"""Displaying the list of clubs' points test"""


def test_displaying_list_of_clubs_points(client):
    response = client.get("/points")
    data = response.data.decode()
    assert "Number of points" in data
