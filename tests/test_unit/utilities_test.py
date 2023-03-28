from ..utilities import loadClubs, loadCompetitions, search_club, retrieveDateCompetition
from ...config import CLUBS_TEST_PATH, COMPETITIONS_TEST_PATH, COMPETITIONS_PATH, CLUBS_PATH

CLUBS = loadClubs(CLUBS_PATH)
COMPETITIONS = loadCompetitions(COMPETITIONS_PATH)

CLUBS_TEST = loadClubs(CLUBS_TEST_PATH)
COMPETITIONS_TEST = loadCompetitions(COMPETITIONS_TEST_PATH)

def test_load_clubs():
    clubs = loadClubs(CLUBS_PATH)
    assert clubs is not None
    assert type(clubs) == list

def test_load_competitions():
    competitions = loadCompetitions(COMPETITIONS_PATH)
    assert competitions is not None
    assert type(competitions) == list

def test_load_clubs_test():
    clubs_test = loadClubs(CLUBS_TEST_PATH)
    assert clubs_test is not None
    assert type(clubs_test) == list

def test_load_competitions_test():
    competitions = loadCompetitions(COMPETITIONS_TEST_PATH)
    assert competitions is not None
    assert type(competitions) == list
