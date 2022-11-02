from Python_Testing import server


def mockloadClubs():
    """
    Mocks data loading from database, discounted after test_booking
    """
    list_of_clubs = [
        {
            "name": "Simply Lift",
            "email": "john@simplylift.co",
            "points": "13"
        },
        {
            "name": "Iron Temple",
            "email": "admin@irontemple.com",
            "points": 1
        },
        {"name": "She Lifts",
         "email": "kate@shelifts.co.uk",
         "points": "12"
         }]

    return list_of_clubs


def test_return_object_clubs():
    server.loadClubs = mockloadClubs()
    result = server.clubs
    assert result == mockloadClubs()
