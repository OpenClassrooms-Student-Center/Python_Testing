from server import SUCCESS_MESSAGE, INSUFFICIENT_POINTS, BOOKING_LIMIT_12_PLACES_MESSAGE, NEGATIVE_POINTS, \
    BOOKING_MORE_THAN_AVAILABLE, clubs, competitions


def test_integration_flow(test_client):
    club_name = clubs[0]["name"]
    club_email = clubs[0]["email"]
    competition_name = competitions[0]["name"]

    # Test email validation
    response = test_client.post("/showSummary", data={"email": club_email})
    data = response.data.decode()
    assert "Welcome" in data

    # Test invalid email
    response = test_client.post("/showSummary", data={"email": "invalid@email.com"})
    data = response.data.decode()
    assert "Invalid email !" in data

    # Test successful booking
    response = test_client.get(f"/book/{competition_name}/{club_name}")
    assert "How many places?" in response.data.decode()

    # Test insufficient points for booking
    response = test_client.post(
        "/purchasePlaces",
        data={
            "competition": competition_name,
            "club": club_name,
            "places": 100,  # Assuming this is more than available points
        },
    )
    data = response.data.decode()
    assert INSUFFICIENT_POINTS in data

    # Test successful booking with enough points
    response = test_client.post(
        "/purchasePlaces",
        data={
            "competition": competition_name,
            "club": club_name,
            "places": 1,
        },
    )
    data = response.data.decode()
    assert SUCCESS_MESSAGE in data

    # Test booking over 12 places
    response = test_client.post(
        "/purchasePlaces",
        data={
            "competition": competition_name,
            "club": club_name,
            "places": 13,
        },
    )
    data = response.data.decode()
    assert BOOKING_LIMIT_12_PLACES_MESSAGE in data

    # Test negative booking places
    response = test_client.post(
        "/purchasePlaces",
        data={
            "competition": competition_name,
            "club": club_name,
            "places": -2,
        },
    )
    data = response.data.decode()
    assert NEGATIVE_POINTS in data

    # Test booking more than available
    response = test_client.post(
        "/purchasePlaces",
        data={
            "competition": competition_name,
            "club": club_name,
            "places": int(competitions[0]["numberOfPlaces"]) + 1,
        },
    )
    data = response.data.decode()
    assert BOOKING_MORE_THAN_AVAILABLE in data
