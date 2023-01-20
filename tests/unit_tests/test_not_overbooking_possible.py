import server
from server import app


class TestNotOverbookInCompetition:
    client = app.test_client()
    competition = [
        {
            "name": "TestComp",
            "date": "2023-03-27 10:00:00",
            "numberOfPlaces": "2"
        }
    ]

    club = [
        {
            "name": "Test_club2",
            "email": "test_club2@email.com",
            "points": "10"
        }
    ]

    def setup_method(self):
        server.competitions = self.competition
        server.clubs = self.club

    def test_overbook_competition(self):

        result = self.client.post(
            "/purchasePlaces",
            data={
                "places": 3,
                "club": self.club[0]["name"],
                "competition": self.competition[0]["name"]
            }
        )

        assert result.status_code == 403
        assert "Not enough available places." in result.data.decode()
        assert int(self.competition[0]['numberOfPlaces']) == 2

    def test_quantity_booking_ok(self):
        result = self.client.post(
            "/purchasePlaces",
            data={
                "places": 2,
                "club": self.club[0]["name"],
                "competition": self.competition[0]["name"]
            }
        )
        assert int(self.competition[0]['numberOfPlaces']) == 0
        assert result.status_code == 200
        assert "Great-booking complete!" in result.data.decode()
        assert int(self.competition[0]['numberOfPlaces']) >= 0
