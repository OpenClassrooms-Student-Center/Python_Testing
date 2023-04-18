import pytest
from ..utilities import loadClubs, loadCompetitions
from ...config import (CLUBS_TEST_PATH,
                       COMPETITIONS_TEST_PATH,
                       COMPETITIONS_PATH,
                       CLUBS_PATH)


CLUBS = loadClubs(CLUBS_PATH)
COMPETITIONS = loadCompetitions(COMPETITIONS_PATH)

CLUBS_TEST = loadClubs(CLUBS_TEST_PATH)
COMPETITIONS_TEST = loadCompetitions(COMPETITIONS_TEST_PATH)


@pytest.mark.parametrize("path", [CLUBS_PATH, CLUBS_TEST_PATH])
def test_load_clubs(path):
    clubs = loadClubs(path)
    assert clubs is not None
    assert type(clubs) == list


@pytest.mark.parametrize("path", [COMPETITIONS_PATH, COMPETITIONS_TEST_PATH])
def test_load_competitions(path):
    competitions = loadCompetitions(path)
    assert competitions is not None
    assert type(competitions) == list
