import server
from server import app


class TestDeductionClubPoints:

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
            "points": "12"
        }
    ]

    def setup_method(self):
        server.competitions = self.competition
        server.clubs = self.club

    def test_deduction_points(self):
        club_points_origin = int(self.club[0]["points"])
        booked_places = 10

        result = self.client.post(
            "/purchasePlaces",
            data={
                "places": booked_places,
                "club": self.club[0]["name"],
                "competition": self.competition[0]["name"]
            }
        )

        assert result.status_code == 200
        assert int(self.club[0]["points"]) == club_points_origin - booked_places
