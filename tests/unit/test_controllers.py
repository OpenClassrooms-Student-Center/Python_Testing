import pytest

from controllers import controllers


@pytest.mark.parametrize(
        "competition_name, club_name, history_of_reservation, expected", [
            ("Spring Festival", "Iron Temple", [], 0),
            ("Spring Festival", "Iron Temple", [
                {'competition': 'Spring Festival',
                 'club': 'Iron Temple',
                 'number_of_places': 1}], 1),
            ("Spring Festival", "Iron Temple", [
                {'competition': 'Spring Festival',
                 'club': 'Iron Temple',
                 'number_of_places': 1},
                {'competition': 'Spring Festival',
                 'club': 'Iron Temple',
                 'number_of_places': 1}], 2)])
def test_get_number_of_place_reserved_for_competition(competition_name,
                                                      club_name,
                                                      history_of_reservation,
                                                      expected):
    """Test the function get_number_of_place_reserved_for_competition."""
    assert controllers.get_number_of_place_reserved_for_competition(
            competition_name, club_name, history_of_reservation) == expected


def test_email_found(mocker, clubs_list):
    """Test the function email_found."""
    request = mocker.Mock()

    request.form = {'email': 'kate@shelifts.co.uk'}
    assert controllers.email_found(request, clubs_list) == {
            "name": "She Lifts",
            "email": "kate@shelifts.co.uk",
            "points": "12"
            }


def test_email_not_found(mocker, clubs_list):
    """Test the function email_not_found."""
    request = mocker.Mock()
    request.form = {'email': 'unknownuser@gmail.com'}
    assert not controllers.email_found(request, clubs_list)


def test_find_club(club_name, clubs_list):
    """Test the function find_club."""
    assert controllers.find_club(club_name, clubs_list) == {
                "name": "Iron Temple",
                "email": "admin@irontemple.com",
                "points": "4"
                }


def test_doesnt_find_club(club_name, clubs_list):
    """Test the function doesnt_find_club."""
    assert not controllers.find_club('unknownclub', clubs_list)


def test_find_competition(competition_name, competitions):
    """Test the function find_competition."""
    assert controllers.find_competition(competition_name, competitions) == {
            "name": "Spring Festival",
            "date": "2020-03-27 10:00:00",
            "numberOfPlaces": "25"
            }


def test_doesnt_find_competition(competition_name, competitions):
    """Test the function doesnt_find_competition."""
    assert not controllers.find_competition('unknowncompetition', competitions)


def test_remove_points_from_competition(competition, competitions):
    """Test the function remove_points_from_competition."""
    assert controllers.remove_points_from_competition(
            competition, competitions, 3) == [
        {
            "name": "Spring Festival",
            "date": "2020-03-27 10:00:00",
            "numberOfPlaces": "22"
            },
        {
            "name": "Fall Classic",
            "date": "2020-10-22 13:30:00",
            "numberOfPlaces": "13"
            },
        {
            "name": "Winter Classic",
            "date": "2023-12-31 10:00:00",
            "numberOfPlaces": "10"
            },
        {
            "name": "Summer Classic",
            "date": "2023-06-30 10:00:00",
            "numberOfPlaces": "10"
            }
        ]


def test_remove_points_from_club(club, clubs_list):
    """Test the function remove_points_from_club."""
    assert controllers.remove_points_from_club(
            club, clubs_list, 4) == [
                    {
                        "name": "Simply Lift",
                        "email": "john@simplylift.co",
                        "points": "13"
                        },
                    {
                        "name": "Iron Temple",
                        "email": "admin@irontemple.com",
                        "points": "0"
                        },
                    {
                        "name": "She Lifts",
                        "email": "kate@shelifts.co.uk",
                        "points": "12"
                        }
                    ]
