import pytest
from .. import server 
from pathlib import Path


current_path = Path(__file__).absolute().parent
PATH_COMPETITIONS_TESTS = current_path/"test_data/test_competitions.json"
PATH_CLUBS_TESTS = current_path/"test_data/test_clubs.json"

@pytest.fixture
def client():
    server.app.config['TESTING']=True
    client = server.app.test_client()
    yield client

@pytest.fixture
def testing_data(mocker):
    path_clubs_json = mocker.patch.object(server,
                                        "PATH_CLUBS",
                                        PATH_CLUBS_TESTS)
    path_competitions_json = mocker.patch.object(server,
                                                "PATH_COMPETITIONS",
                                                PATH_COMPETITIONS_TESTS)
    competitions = server.loadCompetitions()
    clubs = server.loadClubs()

    competitions_test = mocker.patch.object(server, "competitions", competitions)
    clubs_test = mocker.patch.object(server, "clubs", clubs)

    data = {
        "competitions": competitions_test,
        "clubs": clubs_test,
        "path_clubs_json": path_clubs_json,
        "path_competitions_json": path_competitions_json
    }

    return data
