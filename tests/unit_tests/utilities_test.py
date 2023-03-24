'''import pytest
from ..utilities import loadClubs, loadCompetitions, loadClubs_test_data, loadCompetitions_test_data, search_club, retrieveDateCompetition

clubs_test = loadClubs_test_data()
competitions_test = loadCompetitions_test_data()

def test_load_clubs():
    clubs = loadClubs()
    assert clubs is not None
    assert type(clubs) == list

def test_load_competitions():
    competitions = loadCompetitions()
    assert competitions is not None
    assert type(competitions) == list

def test_load_clubs_test():
    clubs = loadClubs_test_data()
    assert clubs is not None
    assert type(clubs) == list

def test_load_competitions_test():
    competitions = loadCompetitions_test_data()
    assert competitions is not None
    assert type(competitions) == list

@pytest.mark.parametrize("club_email, all_clubs, expected_output", [
    ("mail1@test.co", clubs_test, {"name": "club test base", "email": "mail1@test.co", "points": "6"}),
    ("mail2@test.co", clubs_test, {"name": "club test not enough points", "email": "mail2@test.co", "points": "3"}),
    ("mail3@test.co", clubs_test, {"name": "club test more than 12 points", "email": "mail3@test.co", "points": "13"}),
])
def test_search_club_right(club_email, all_clubs, expected_output):
    assert search_club(club_email, all_clubs) == expected_output

@pytest.mark.parametrize("club_email, all_clubs, expected_output", [
    ("wrongmail1@test.co", clubs_test, None),
    ("wrongmail2@test.co", clubs_test, None),
    ("wrongmail3@test.co", clubs_test, None),
])
def test_search_club_wrong(club_email, all_clubs, expected_output):
    assert search_club(club_email, all_clubs) == None

@pytest.mark.parametrize("my_request, expected_output", [
    ('Competition Test base', "2023-03-27 10:00:00"),
    ('out dated', "2020-10-22 13:30:00"),
])
def test_retrieve_date(my_request, expected_output):
    date = retrieveDateCompetition(my_request)
    assert date == expected_output

def test_init_db_clubs():
    pass

def test_init_db_competitions():
    pass

def test_writer_json():
    pass'''