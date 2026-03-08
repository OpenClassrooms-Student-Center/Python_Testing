import pytest
import server

@pytest.fixture(autouse=True)
def reset_server_data():
    server.clubs = server.load_clubs()
    server.competitions = server.load_competitions()
    yield

class TestLoginIntegration:
    """Integration tests for login using real clubs.json data"""

    def test_login_flow_with_welcome_display(self, client):
        """
        Tests that a correct email leads to
        1) redirect page to 'welcome.html'
        2) checks content matches object (ex. points, email)
        3) checks at least one competition appears
        4) 'Book Places' button appears if places available > 0
        """
        response = client.post("/showSummary", data={"email": "john@simplylift.co"})

        # 1) successful response
        assert response.status_code == 200

        # 2) email and points appear
        assert b"john@simplylift.co" in response.data
        assert b"13" in response.data

        # 3) at least one real competition appears
        assert b"Fall Classic" in response.data

        # 4) booking link appears since competitions have places
        assert b"Book Places" in response.data

class TestPurchasePlacesIntegration:
    """Integration tests for the full purchase flow with real data"""

    def test_full_successful_purchase_flow(self, client):
        """
        Tests complete reservation flow:
        1) Booking succeeds
        2) Success message appears
        3) Competition places decrease
        4) Club points decrease
        """
        before_places = int(server.competitions[0]["numberOfPlaces"])
        before_points = int(server.clubs[0]["points"])

        response = client.post("/purchasePlaces", data={
            "competition": "Spring Festival",
            "club": "Simply Lift",
            "places": "12"
        })

        # 1) successful response
        assert response.status_code == 200
        # 2) success message
        assert b"Great-booking complete!" in response.data
        # 3) competition places decreased
        assert int(server.competitions[0]["numberOfPlaces"]) == before_places - 12
        # 4) club points decreased
        assert int(server.clubs[0]["points"]) == before_points - 12

    def test_failed_purchase_does_not_alter_real_data(self, client):
        """Blocked flows to change database if validations fail"""
        before_places = int(server.competitions[0]["numberOfPlaces"])
        before_points = int(server.clubs[0]["points"])

        client.post("/purchasePlaces", data={
            "competition": "Spring Festival",
            "club": "Simply Lift",
            "places": "13"  # over limit
        })

        assert int(server.competitions[0]["numberOfPlaces"]) == before_places
        assert int(server.clubs[0]["points"]) == before_points


class TestPointsBoardIntegration:
    """Integration tests for the points board flow with real data"""
    def test_points_board_displays_real_clubs(self, client):
        """Tests appearance of real club names"""
        response = client.get('/pointsByClub')
        assert b"Simply Lift" in response.data
        assert b"Iron Temple" in response.data
        assert b"She Lifts" in response.data