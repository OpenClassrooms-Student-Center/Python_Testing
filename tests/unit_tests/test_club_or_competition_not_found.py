import server
from server import app


class TestBookingWithUnknownClubOrCompetition:

    client = app.test_client()
    competition = [
        {
            "name": "Test_comp",
            "date": "2024-03-27 10:00:00",
            "numberOfPlaces": "15"
        }
    ]

    club = [
        {
            "name": "Test_club",
            "email": "test_club@email.com",
            "points": "15"
        }
    ]

    def setup_method(self):
        server.competitions = self.competition
        server.clubs = self.club

    def test_unknown_competition(self):
        result = self.client.get(
            f"/book/Unknown_comp/{self.club[0]['name']}")

        assert result.status_code == 404
        assert "Something went wrong. Please try again." in result.data.decode()

    def test_unknown_club(self):
        result = self.client.get(
            f"/book/{self.competition[0]['name']}/Unknown_club")
        assert result.status_code == 404
        assert "Something went wrong. Please try again." in result.data.decode()

    def test_known_competition_and_club(self):
        result = self.client.get(
            f"/book/{self.competition[0]['name']}/{self.club[0]['name']}")
        assert result.status_code == 200
