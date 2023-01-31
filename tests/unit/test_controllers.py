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
            "date": "2023-03-27 10:00:00",
            "numberOfPlaces": "25",
            "passed": False
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
            "date": "2023-03-27 10:00:00",
            "numberOfPlaces": "22",
            "passed": False
            },
        {
            "name": "Fall Classic",
            "date": "2020-10-22 13:30:00",
            "numberOfPlaces": "13",
            "passed": True
            },
        {
            "name": "Winter Classic",
            "date": "2023-12-31 10:00:00",
            "numberOfPlaces": "10",
            "passed": False
            },
        {
            "name": "Summer Classic",
            "date": "2023-06-30 10:00:00",
            "numberOfPlaces": "10",
            "passed": False
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


def test_verify_user_input_good_case(mocker, clubs_list, competitions):
    """Test the function verify_user_input."""
    request = mocker.Mock()
    request.form = {
            'competition': 'Spring Festival',
            'club': 'Simply Lift',
            'places': '2'
            }
    competition, club, places_required = controllers.verify_user_input(
            request,
            clubs_list,
            competitions)

    expected_competition = {
            "name": "Spring Festival",
            "date": "2023-03-27 10:00:00",
            "numberOfPlaces": "25",
            "passed": False
            }
    expected_club = {
            "name": "Simply Lift",
            "email": "john@simplylift.co",
            "points": "13"
            }
    expected_places_required = 2
    assert competition == expected_competition
    assert club == expected_club
    assert places_required == expected_places_required


def test_verify_user_input_missing_competition(
        mocker, clubs_list, competitions):
    """Test the function verify_user_input with a bad competition."""
    request = mocker.Mock()
    request.form = {
            'competition': 'unknowncompetition',
            'club': 'Simply Lift',
            'places': '2'
            }
    with pytest.raises(controllers.ValueMissing):
        controllers.verify_user_input(
                request,
                clubs_list,
                competitions)


def test_verify_user_input_missing_club(
        mocker, clubs_list, competitions):
    """Test the function verify_user_input with a bad club."""
    request = mocker.Mock()
    request.form = {
            'competition': 'Spring Festival',
            'club': 'unknownclub',
            'places': '2'
            }
    with pytest.raises(controllers.ValueMissing):
        controllers.verify_user_input(
                request,
                clubs_list,
                competitions)


def test_verify_user_input_place_is_alpha(
        mocker, clubs_list, competitions):
    """Test the function verify_user_input with a bad places."""
    request = mocker.Mock()
    request.form = {
            'competition': 'Spring Festival',
            'club': 'Simply Lift',
            'places': 'a'
            }
    with pytest.raises(ValueError):
        controllers.verify_user_input(
                request,
                clubs_list,
                competitions)


def test_verify_user_input_place_is_negative(
        mocker, clubs_list, competitions):
    """Test the function verify_user_input with a bad places."""
    request = mocker.Mock()
    request.form = {
            'competition': 'Spring Festival',
            'club': 'Simply Lift',
            'places': '-1'
            }
    with pytest.raises(controllers.CannotBookLessThanOnePlace):
        controllers.verify_user_input(
                request,
                clubs_list,
                competitions)


def test_verify_user_input_place_is_zero(
        mocker, clubs_list, competitions):
    """Test the function verify_user_input with a bad places."""
    request = mocker.Mock()
    request.form = {
            'competition': 'Spring Festival',
            'club': 'Simply Lift',
            'places': '0'
            }
    with pytest.raises(controllers.CannotBookLessThanOnePlace):
        controllers.verify_user_input(
                request,
                clubs_list,
                competitions)


def test_club_has_enough_points(club):
    """Test the function club_has_enough_points."""
    assert controllers.club_has_enough_points(
            club, 3)
    assert controllers.club_has_enough_points(
            club, 4)
    assert not controllers.club_has_enough_points(
            club, 5)


def test_club_wants_more_than_twelve_places():
    """Test the function club_wants_more_than_twelve_places."""
    assert not controllers.club_wants_more_than_twelve_places(6, 6)
    assert controllers.club_wants_more_than_twelve_places(6, 7)
    assert controllers.club_wants_more_than_twelve_places(6, 12)
    assert not controllers.club_wants_more_than_twelve_places(0, 0)


def test_club_wants_more_than_available_places(competition):
    """Test the function club_wants_more_than_available_places."""

    assert not controllers.club_wants_more_than_available_places(
            24, competition)
    assert not controllers.club_wants_more_than_available_places(
            25, competition)
    assert controllers.club_wants_more_than_available_places(
            26, competition)
    assert controllers.club_wants_more_than_available_places(
            27, competition)


def test_verify_club_can_book(
        competition, club):
    """Test the function verify_club_can_book.
    Place required, and already_required."""
    place_required = 1
    already_required = 0
    assert controllers.verify_club_can_book(
            competition,
            club,
            place_required,
            already_required)


def test_verify_club_can_book_more_than_available_places(
        competition_1_place, club):
    """Test the raise of the BookMoreThanAvailablePlaces exception."""

    place_required = 2
    already_required = 0
    with pytest.raises(controllers.BookMoreThanAvailablePlaces):
        controllers.verify_club_can_book(
                competition_1_place,
                club,
                place_required,
                already_required)


def test_verify_club_can_book_raise_exception_not_enough_points(
        competition, club_4_points):
    """Test the raise of the NotEnoughPoints exception."""
    place_required = 5
    already_required = 0
    with pytest.raises(controllers.NotEnoughPoints):
        controllers.verify_club_can_book(
                competition,
                club_4_points,
                place_required,
                already_required)


def test_verify_club_can_book_raise_exception_more_than_twelve_places(
        competition, club_15_points):
    """Test the raise of the MoreThanTwelvePlaces exception."""

    place_required = 13
    already_required = 0
    with pytest.raises(controllers.BookMoreThanTwelvePlaces):
        controllers.verify_club_can_book(
                competition,
                club_15_points,
                place_required,
                already_required)


def test_add_reservation_to_history(competition, club):
    """Test the function add_reservation_to_history."""
    history_of_reservation = []
    controllers.add_reservation_to_history(
            competition,
            club,
            1,
            history_of_reservation)
    assert history_of_reservation == [
            {
                "competition": "Spring Festival",
                "club": "Iron Temple",
                "number_of_places": 1,
            }]
    controllers.add_reservation_to_history(
            competition,
            club,
            1,
            history_of_reservation)
    assert history_of_reservation == [
            {
                "competition": "Spring Festival",
                "club": "Iron Temple",
                "number_of_places": 1,
            },
            {
                "competition": "Spring Festival",
                "club": "Iron Temple",
                "number_of_places": 1,
            }]


def test_handle_purchase_happy_path(mocker, competitions, clubs_list):
    """Test the function handle_purchase."""
    request = mocker.Mock()
    request.form = {
            'competition': 'Summer Classic',
            'club': 'Simply Lift',
            'places': '2'
            }
    message, page, club = controllers.handle_purchase(
            request,
            [],
            competitions,
            clubs_list)
    assert message == 'Congratulation for booking 2 places !'
    assert page == "welcome.html"


def test_handle_purchase_ask_too_much(mocker, competitions, clubs_list):
    """Test the function handle_purchase."""
    request = mocker.Mock()
    request.form = {
            'competition': 'Spring Festival',
            'club': 'Simply Lift',
            'places': '22'
            }
    message, page, club = controllers.handle_purchase(
            request,
            [],
            competitions,
            clubs_list)
    assert message == "You don't have enough points to book 22 places."
    assert page == "welcome.html"


def test_handle_purchase_negative_value(mocker, competitions, clubs_list):
    """Test the function handle_purchase."""
    request = mocker.Mock()
    request.form = {
            'competition': 'Spring Festival',
            'club': 'Simply Lift',
            'places': '-6'
            }
    message, page, club = controllers.handle_purchase(
            request,
            [],
            competitions,
            clubs_list)
    assert message == "You can't book less than 1 place."
    assert page == "index.html"


def test_handle_purchase_missing_value(mocker, competitions, clubs_list):
    """Test the function handle_purchase."""
    request = mocker.Mock()
    request.form = {
            'competition': '',
            'club': 'Simply Lift',
            'places': '6'
            }
    message, page, club = controllers.handle_purchase(
            request,
            [],
            competitions,
            clubs_list)
    assert message == "Please fill all the fields."
    assert page == "index.html"


def test_handle_purchase_alpha_value(mocker, competitions, clubs_list):
    """Test the function handle_purchase."""
    request = mocker.Mock()
    request.form = {
            'competition': 'Spring Festival',
            'club': 'Simply Lift',
            'places': 'salut'
            }
    message, page, club = controllers.handle_purchase(
            request,
            [],
            competitions,
            clubs_list)
    assert message == "Please enter a number for the number of places."
    assert page == "index.html"


def test_handle_purchase_too_much_value(mocker, competitions, clubs_list):
    """Test the function handle_purchase."""
    request = mocker.Mock()
    request.form = {
            'competition': 'Spring Festival',
            'club': 'Iron Temple',
            'places': '5'
            }
    message, page, club = controllers.handle_purchase(
            request,
            [],
            competitions,
            clubs_list)
    assert message == "You don't have enough points to book 5 places."
    assert page == "welcome.html"


def test_handle_purchase_more_than_twelve_place(
        mocker, competitions, clubs_list):
    """Test the function handle_purchase."""
    request = mocker.Mock()
    request.form = {
            'competition': 'Spring Festival',
            'club': 'Simply Lift',
            'places': '13'
            }
    message, page, club = controllers.handle_purchase(
            request,
            [],
            competitions,
            clubs_list)
    assert message == "You can only book 12 places per competition."
    assert page == "welcome.html"


def test_handle_purchase_more_than_place_available(
        mocker, competitions, clubs_list):
    """Test the function handle_purchase."""
    request = mocker.Mock()
    request.form = {
            'competition': 'Winter Classic',
            'club': 'Simply Lift',
            'places': '11'
            }
    message, page, club = controllers.handle_purchase(
            request,
            [],
            competitions,
            clubs_list)
    assert message == ("Sorry, you can't book for this competition as there "
                       "are not enough places.")
    assert page == "welcome.html"
