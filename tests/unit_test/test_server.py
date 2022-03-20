from tests.unit_test.conftest import client, club, competition
from server import loadClubs, loadCompetitions


def test_loadClubs():
    assert loadClubs("./tests/unit_test/fixture_files/fixture_load.json") == club()

def test_loadCompetitions():
    assert loadCompetitions("./tests/unit_test/fixture_files/fixture_load.json") == competition()