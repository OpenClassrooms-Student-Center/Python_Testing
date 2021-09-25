import unittest
from server import getClubByEmail, checkPlacesRequired, checkDateCompetition
from exceptions import EmailNotFound, ClubNotEnoughPoints, CompetitionNotEnoughPlaces, BookingLimitPlaces, \
    CompetitionIsClosed
from datetime import datetime, timedelta


class TestFormEmail(unittest.TestCase):

    def setUp(self):
        self.clubs = [{'name': 'club_1', 'email': 'email_club_1', 'points': 1},
                      {'name': 'club_2', 'email': 'email_club_2', 'points': 2}]

    def test_exception_is_raised_if_email_does_not_exist(self):
        wrong_email = 'email_club_3'
        with self.assertRaises(EmailNotFound):
            getClubByEmail(wrong_email, self.clubs)

    def test_returned_club_if_email_does_exist(self):
        club = getClubByEmail('email_club_1', self.clubs)
        self.assertEqual(club['name'], 'club_1')


class TestFormBooking(unittest.TestCase):

    def setUp(self):
        self.points_club = 10
        self.competition_places = 15

    def test_exception_is_raised_if_places_required_are_greater_than_points_club(self):
        with self.assertRaises(ClubNotEnoughPoints):
            checkPlacesRequired(11, self.competition_places, self.points_club)

    def test_exception_is_raised_if_places_required_are_greater_than_competition_places(self):
        with self.assertRaises(CompetitionNotEnoughPlaces):
            checkPlacesRequired(16, self.competition_places, self.points_club)

    def test_return_if_places_required_are_less_or_equal_than_points_club_and_competition_places(self):
        self.assertEqual(checkPlacesRequired(10, self.competition_places, self.points_club), 10)

    def test_exception_is_raised_if_places_required_are_greater_than_limit_booking_places(self):
        with self.assertRaises(BookingLimitPlaces):
            checkPlacesRequired(13, self.competition_places, points_club=14)

    def test_exception_is_raised_if_competition_is_closed(self):
        date = datetime.now() - timedelta(days=1)
        str_date = date.strftime('%Y-%m-%d %H:%M:%S')
        with self.assertRaises(CompetitionIsClosed):
            checkDateCompetition(str_date)

    def test_exception_not_raised_if_competition_is_not_closed(self):
        date = datetime.now() + timedelta(days=1)
        str_date = date.strftime('%Y-%m-%d %H:%M:%S')
        checkDateCompetition(str_date)


if __name__ == '__main__':
    unittest.main()