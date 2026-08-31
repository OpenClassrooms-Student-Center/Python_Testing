import pytest
import copy
import server


@pytest.fixture
def client():
    server.app.config['TESTING'] = True
    with server.app.test_client() as client:
        yield client

@pytest.fixture(autouse=True)
def reset_data():
    clubs_sauvegarde = copy.deepcopy(server.clubs)
    competition_sauvegarde = copy.deepcopy(server.competitions)
    yield
    server.clubs[:] = clubs_sauvegarde
    server.competitions[:] = competition_sauvegarde