import os

import pytest
import server


ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
CHROME_DRIVER_PATH = os.path.join(ROOT_DIR, '../chromedriver.exe')

PATH_COMPETITIONS_TESTS = "Sample_Data/test_competitions.json"
PATH_CLUBS_TESTS = "Sample_Data/test_clubs.json"


@pytest.fixture
def client():
    server.app.config['TESTING'] = True
    client = server.app.test_client()
    yield client


@pytest.fixture
def testing_data(mocker):
    """
    Load the testing data
    """

    file_competitions = open(PATH_COMPETITIONS_TESTS, "w")
    file_competitions.write(
        """{"competitions":
        [
        {
            "name": "Competition 1",
            "date": "2020-10-02 10:00:00",
            "numberOfPlaces": "13"
        },
        {
            "name": "Competition 2",
            "date": "2023-12-22 13:30:00",
            "numberOfPlaces": "5"
        },
        {
            "name": "Competition 3",
            "date": "2023-12-22 13:30:00",
            "numberOfPlaces": "25"
        }
        ]
        }"""
    )
    file_competitions.close()

    file_clubs = open(PATH_CLUBS_TESTS, "w")
    file_clubs.write(
        """{"clubs":
        [
        {
            "name":"Simply Lift",
            "email":"john@simplylift.co",
            "points":"13"
        },
        {
            "name":"Iron Temple",
            "email": "admin@irontemple.com",
            "points":"4"
        },
        {   "name":"She Lifts",
            "email": "kate@shelifts.co.uk",
            "points":"12"
        },
        {
            "name":"Test Club (many places)",
            "email": "testclub@club.com",
            "points":"500"
        }
        ]
        }"""
    )
    file_clubs.close()

    path_clubs_json = mocker.patch.object(server,
                                          "PATH_CLUBS",
                                          PATH_CLUBS_TESTS)
    path_competitions_json = mocker.patch.object(server,
                                                 "PATH_COMPETITIONS",
                                                 PATH_COMPETITIONS_TESTS)
    competitions = server.load_competitions()
    clubs = server.load_clubs()

    comps = mocker.patch.object(server, "competitions", competitions)
    c = mocker.patch.object(server, "clubs", clubs)

    data = {
        "competitions": comps,
        "clubs": c,
        "path_clubs_json": path_clubs_json,
        "path_competitions_json": path_competitions_json
    }

    return data
