import pytest

import server

server.clubs = server.load_clubs("tests/clubs.json")
server.competitions = server.load_competitions("tests/competitions.json")


@pytest.fixture
def client():
    app = server.app
    app.config["TESTING"] = True
    app.secret_key = "testing_secret_key"

    client = app.test_client()
    return client
