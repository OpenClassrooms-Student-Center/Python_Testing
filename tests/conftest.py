import pytest


@pytest.fixture
def competition_name():
    """Return a competition name."""
    return 'Spring Festival'


@pytest.fixture
def competition():
    """Return a competition."""
    return {
            "name": "Spring Festival",
            "date": "2020-03-27 10:00:00",
            "numberOfPlaces": "25"
            }


@pytest.fixture
def club_name():
    """Return a club name."""
    return 'Iron Temple'


@pytest.fixture
def club():
    """Return a club."""
    return {
                "name": "Iron Temple",
                "email": "admin@irontemple.com",
                "points": "4"
            }


@pytest.fixture
def competitions():
    """Return a list of competitions."""
    return [
        {
            "name": "Spring Festival",
            "date": "2020-03-27 10:00:00",
            "numberOfPlaces": "25"
            },
        {
            "name": "Fall Classic",
            "date": "2020-10-22 13:30:00",
            "numberOfPlaces": "13"
            },
        {
            "name": "Winter Classic",
            "date": "2023-12-31 10:00:00",
            "numberOfPlaces": "10"
            },
        {
            "name": "Summer Classic",
            "date": "2023-06-30 10:00:00",
            "numberOfPlaces": "10"
            }
        ]


@pytest.fixture
def clubs_list():
    """Test the function load_clubs."""
    return [{
        "name": "Simply Lift",
        "email": "john@simplylift.co",
        "points": "13"
        },
            {
                "name": "Iron Temple",
                "email": "admin@irontemple.com",
                "points": "4"
                },
            {
                "name": "She Lifts",
                "email": "kate@shelifts.co.uk",
                "points": "12"
                }
            ]
