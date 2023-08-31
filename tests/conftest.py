import pytest

import server


def set_test_bdd():
    server.clubs = server.load_data("tests/clubs.json")["clubs"]
    server.competitions = server.load_data("tests/competitions.json")["competitions"]


@pytest.fixture(scope="module")
def client():
    set_test_bdd()
    app = server.app
    app.config["TESTING"] = True
    app.secret_key = "testing_secret_key"

    client = app.test_client()
    return client
