"""Tests unitaires de la validation métier des réservations (validate_purchase)."""
import server


class TestValidatePurchaseHappyPath:
    def test_valid_purchase_returns_none(self, clubs_data, competitions_data):
        club = clubs_data[0]           # 15 points
        competition = competitions_data[0]  # Future Comp, 25 places
        assert server.validate_purchase(club, competition, 5) is None


class TestValidatePurchaseSadPath:
    def test_zero_places_is_rejected(self, clubs_data, competitions_data):
        error = server.validate_purchase(clubs_data[0], competitions_data[0], 0)
        assert error == "Number of places must be at least 1."

    def test_negative_places_is_rejected(self, clubs_data, competitions_data):
        error = server.validate_purchase(clubs_data[0], competitions_data[0], -3)
        assert error == "Number of places must be at least 1."

    def test_past_competition_is_rejected(self, clubs_data, competitions_data):
        past_competition = competitions_data[1]  # Past Comp
        error = server.validate_purchase(clubs_data[0], past_competition, 2)
        assert error == "This competition has already taken place."

    def test_more_than_twelve_places_is_rejected(self, clubs_data, competitions_data):
        error = server.validate_purchase(clubs_data[0], competitions_data[0], 13)
        assert "Cannot book more than 12" in error

    def test_full_competition_is_rejected(self, clubs_data, competitions_data):
        full_competition = competitions_data[2]  # Full Comp, 0 place
        error = server.validate_purchase(clubs_data[0], full_competition, 1)
        assert error == "Competition is full."

    def test_not_enough_places_is_rejected(self, clubs_data, competitions_data):
        competition = dict(competitions_data[0], numberOfPlaces="3")
        error = server.validate_purchase(clubs_data[0], competition, 5)
        assert "Not enough places available" in error

    def test_not_enough_points_is_rejected(self, clubs_data, competitions_data):
        club = clubs_data[1]  # Test Club B, 4 points
        error = server.validate_purchase(club, competitions_data[0], 6)
        assert error == "Not enough points available."


class TestValidatePurchaseCumulativeLimit:
    def test_cumulative_over_twelve_is_rejected(self, clubs_data, competitions_data):
        club = clubs_data[0]
        competition = competitions_data[0]
        server.record_purchase(club, competition, 8)
        error = server.validate_purchase(club, competition, 5)
        assert "you can only book 4 more" in error

    def test_no_more_places_allowed_when_limit_reached(self, clubs_data, competitions_data):
        club = clubs_data[0]
        competition = competitions_data[0]
        server.record_purchase(club, competition, 12)
        error = server.validate_purchase(club, competition, 1)
        assert "Cannot book more than 12 places per competition for your club" in error
