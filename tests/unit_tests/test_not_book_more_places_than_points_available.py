import server
from server import app


class TestMorePointsThanAllowedPlaces:

    client = app.test_client()
    competition = [
        {
            "name": "Test",
            "date": "2023-03-27 10:00:00",
            "numberOfPlaces": "30"
        }
    ]

    club = [
        {
            "name": "Test_club",
            "email": "test_club@email.com",
            "points": "10"
        }
    ]

    def setup_method(self):
        server.competitions = self.competition
        server.clubs = self.club

    def test_more_points_used_than_allowed(self):
        self.client.post(
            "/purchasePlaces",
            data={
                "places": 100,
                "club": self.club[0]["name"],
                "competition": self.competition[0]["name"]
            }
        )

        assert int(self.club[0]["points"]) >= 0
