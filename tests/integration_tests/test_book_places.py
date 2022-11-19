from server import COMPETITION_PLACES_SUCCESFULLY_BOOKED_MESSAGE, loadClubs, loadCompetitions


def test_booking_places_full_route(client):
    """
    We first test if we can rendered the template index.html,
    then we test if we can log in and rendered the template welcome.html and booking.html.
    then we test if POST request works to purchase places.

    """
    # testing data loading functions
    competitions = loadCompetitions()
    clubs = loadClubs()

    competition_name = [c for c in competitions if c["name"] == "Spring Festival"]
    club_name = [c for c in clubs if c["name"] == "Simply Lift"]

    #  render template index.html with GET request
    response = client.get("/")
    data = response.data.decode()
    assert "Please enter your secretary email to continue" in data

    #  render template welcome.html with POST request
    response = client.post("/showSummary", data={"email": "john@simplylift.co"})
    data = response.data.decode()
    assert "Welcome" in data

    #  render template booking.html with POST request
    response = client.get(f"/book/{competition_name}/{club_name}")
    data = response.data.decode()
    assert data.find("How many places?")

    response = client.post(
        "/purchasePlaces",
        data={
            "competition": competition_name,
            "club": club_name,
            "places": 12,
        },
    )

    data = response.data.decode()
    assert data.find(COMPETITION_PLACES_SUCCESFULLY_BOOKED_MESSAGE)
