import pytest
from server import app
from selenium import webdriver


@pytest.fixture
def mock_clubs(mocker):
    data = [{
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
    mocker.patch.object('Python_Testing.controllers.clubs_list', data)


@pytest.fixture
def mock_competitions(mocker):
    data = [
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
    mocker.patch('Python_Testing.controllers.competitions_list', data)


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


@pytest.fixture
def club_15_points():
    """Return a club with 15 points."""
    return {
            "name": "Simply Lift",
            "email": "toto@mail.com",
            "points": "15"
            }


@pytest.fixture
def club_4_points():
    """Return a club with 4 points."""
    return {
            "name": "Simply Lift",
            "email": "not_relevant@email.com",
            "points": "4"
            }


@pytest.fixture
def competition_1_place():
    """Competition with 1 place."""
    return {
            "name": "Spring Festival",
            "date": "2020-03-27 10:00:00",
            "numberOfPlaces": "1"
            }


@pytest.fixture
def client():
    """Test the function load_clubs."""
    return app.test_client()


@pytest.fixture(autouse=True)
def load_clubs(mocker):
    """Create test data for clubs."""
    test_data = {"clubs": [
        {
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
        ]}
    mocker.patch('models.models.load_clubs', test_data)


@pytest.fixture(autouse=True)
def load_competitions(mocker):
    """Mock of the load_competitors fonction."""
    competition_file = {
            "competitions": [
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
                    "numberOfPlaces": "13"
                    },
                {
                    "name": "Summer Classic",
                    "date": "2023-06-30 10:00:00",
                    "numberOfPlaces": "10"
                    }
                ]
            }
    mocker.patch('models.models.load_competitions', competition_file)


@pytest.fixture()
def driver():
    """Return a driver."""
    return webdriver.Firefox()
