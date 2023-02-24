import server
from server import app


class TestSummaryPointsUpdated:
    client = app.test_client()
    competition = [
        {
            "name": "Test",
            "date": "2023-04-27 10:00:00",
            "numberOfPlaces": "20"
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

    def test_points_updated(self):
        club_points_before = int(self.club[0]["points"])
        booked_places = 3

        self.client.post(
            "/purchasePlaces",
            data={
                "places": booked_places,
                "club": self.club[0]["name"],
                "competition": self.competition[0]["name"]
            }
        )

        result = self.client.post("/showSummary", data={"email": "test_club@email.com"})

        assert result.status_code == 200
        assert f"{self.club[0]['name']}" in result.data.decode()
        assert f"{club_points_before - booked_places}" in result.data.decode()
