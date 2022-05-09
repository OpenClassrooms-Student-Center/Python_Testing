import pytest
import server


@pytest.fixture
def client():
    with server.app.test_client() as client:
        yield client


@pytest.fixture
def mock_loadClubs():
    clubs = [
        {"name": "Simply Lift", "email": "john@simplylift.co", "points": "13"},
        {"name": "Iron Temple", "email": "admin@irontemple.com", "points": "4"},
        {"name": "She Lifts", "email": "kate@shelifts.co.uk", "points": "12"},
        {"name": "Wing chun", "email": "yipman@grandmaster.cn", "points": "50"},
    ]
    return clubs


@pytest.fixture
def mock_loadCompetitions():
    competitions = [
        {
            "name": "Spring Festival",
            "date": "2020-03-27 10:00:00",
            "numberOfPlaces": "25",
        },
        {"name": "Fall Classic", "date": "2020-10-22 13:30:00", "numberOfPlaces": "13"},
        {
            "name": "Spring Boxing",
            "date": "2023-06-30 12:00:00",
            "numberOfPlaces": "30",
        },
    ]
    return competitions


@pytest.fixture
def mock_clubs_and_competitions(mocker, mock_loadClubs, mock_loadCompetitions):
    mocker.patch.object(server, "clubs", mock_loadClubs)
    mocker.patch.object(server, "competitions", mock_loadCompetitions)
