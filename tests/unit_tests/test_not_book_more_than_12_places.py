import server
from server import app


class TestNotMoreThanTwelvePoints:

    client = app.test_client()
    competition = [
        {
            "name": "Test",
            "date": "2023-03-27 10:00:00",
            "numberOfPlaces": "40"
        }
    ]

    club = [
        {
            "name": "Test_club",
            "email": "test_club@email.com",
            "points": "25"
        }
    ]

    booked_places = [
        {
            "competition": "Test",
            "booked": [5, "Test_club"]
        }
    ]

    def setup_method(self):
        server.competitions = self.competition
        server.clubs = self.club
        server.booked_places = self.booked_places

    def test_more_than_twelve_at_once(self):

        result = self.client.post(
            "/purchasePlaces",
            data={
                "places": 13,
                "club": self.club[0]["name"],
                "competition": self.competition[0]["name"]
            }
        )

        assert result.status_code == 403
        assert "more than 12 places in a competition." in result.data.decode()

    def test_less_than_or_equal_twelve(self):

        result = self.client.post(
            "/purchasePlaces",
            data={
                "places": 7,
                "club": self.club[0]["name"],
                "competition": self.competition[0]["name"]
            }
        )

        assert result.status_code == 200
        assert "Great-booking complete!" in result.data.decode()

    def test_more_than_twelve_in_several_time(self):

        result = self.client.post(
            "/purchasePlaces",
            data={
                "places": 1,
                "club": self.club[0]["name"],
                "competition": self.competition[0]["name"]
            }
        )

        assert result.status_code == 403
        # assert "more than 12 places in a competition." in result.data.decode()
