import pytest

import server

server.clubs = server.load_clubs('tests/clubs.json')
server.competitions = server.load_competitions('tests/competitions.json')

@pytest.fixture
def app():
    app = server.app
    app.config["TESTING"] = True
    app.secret_key = "testing_secret_key"
    return app
