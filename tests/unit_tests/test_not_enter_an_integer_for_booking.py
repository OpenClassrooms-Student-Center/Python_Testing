import server
from server import app


class TestNotMoreThanTwelvePoints:

    client = app.test_client()
    competition = [
        {
            "name": "Test_Competition",
            "date": "2023-04-27 10:00:00",
            "numberOfPlaces": "20"
        }
    ]

    club = [
        {
            "name": "Test_club2",
            "email": "test2_club@email.com",
            "points": "15"
        }
    ]

    def setup_method(self):
        server.competitions = self.competition
        server.clubs = self.club

    def test_not_enter_integer(self):

        result = self.client.post(
            "/purchasePlaces",
            data={
                "places": "",
                "club": self.club[0]["name"],
                "competition": self.competition[0]["name"]
            }
        )

        assert result.status_code == 403
        assert "You must enter an integer." in result.data.decode()

    def test_enter_integer(self):

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
