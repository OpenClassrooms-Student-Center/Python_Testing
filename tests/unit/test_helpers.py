"""Tests unitaires des fonctions utilitaires (clubs, compteur de réservations)."""
import server


class TestGetClubByEmail:
    def test_returns_club_for_known_email(self):
        club = server.get_club_by_email("a@test.com")
        assert club is not None
        assert club["name"] == "Test Club A"

    def test_returns_none_for_unknown_email(self):
        assert server.get_club_by_email("unknown@nowhere.com") is None


class TestBookingCounter:
    def test_no_booking_returns_zero(self, clubs_data, competitions_data):
        club = clubs_data[0]
        competition = competitions_data[0]
        assert server.get_places_already_booked(club, competition) == 0

    def test_record_purchase_accumulates(self, clubs_data, competitions_data):
        club = clubs_data[0]
        competition = competitions_data[0]
        server.record_purchase(club, competition, 3)
        server.record_purchase(club, competition, 2)
        assert server.get_places_already_booked(club, competition) == 5

    def test_counter_is_isolated_per_club_and_competition(self, clubs_data, competitions_data):
        club_a, club_b = clubs_data
        competition = competitions_data[0]
        server.record_purchase(club_a, competition, 4)
        assert server.get_places_already_booked(club_a, competition) == 4
        assert server.get_places_already_booked(club_b, competition) == 0
