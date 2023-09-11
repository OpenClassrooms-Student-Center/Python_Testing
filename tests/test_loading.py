import json
from ..server import loadClubs, loadCompetitions


def test_should_load_club_correctly():
    expected_club = {
        "name": "He Tests",
        "email": "test@test.fr",
        "points": "15",
    }
    clubs = loadClubs()
    test_club = [club for club in clubs if club["name"] == "He Tests"]
    assert test_club == [expected_club]


def test_should_load_competition_correctly():
    expected_competition = {
        "name": "Test me !",
        "date": "2023-09-11 12:00:00",
        "numberOfPlaces": "10",
    }
    competitions = loadCompetitions()
    test_competition = [c for c in competitions if c["name"] == "Test me !"]
    assert test_competition == [expected_competition]
