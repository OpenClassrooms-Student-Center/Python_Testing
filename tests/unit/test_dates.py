"""Tests unitaires du filtrage des compétitions par date (Phase 1)."""
import server


class TestIsCompetitionUpcoming:
    def test_future_competition_is_upcoming(self):
        competition = {"name": "X", "date": "2050-01-01 10:00:00", "numberOfPlaces": "10"}
        assert server.is_competition_upcoming(competition) is True

    def test_past_competition_is_not_upcoming(self):
        competition = {"name": "X", "date": "2000-01-01 10:00:00", "numberOfPlaces": "10"}
        assert server.is_competition_upcoming(competition) is False


class TestGetUpcomingCompetitions:
    def test_only_future_competitions_are_returned(self, competitions_data):
        upcoming = server.get_upcoming_competitions()
        names = [competition["name"] for competition in upcoming]
        assert "Future Comp" in names
        assert "Full Comp" in names
        assert "Past Comp" not in names

    def test_returns_a_list(self):
        assert isinstance(server.get_upcoming_competitions(), list)
