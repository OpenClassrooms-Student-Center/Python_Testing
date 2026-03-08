import pytest
import server


# ---------------------------------------------------------------------------
# Test Login Functionality
# ---------------------------------------------------------------------------
class TestLogin:
    """Tests for the showSummary route - login behaviour."""
    # ---------------------------------------------------------------------------
    # Sad path
    # ---------------------------------------------------------------------------
    def test_unknown_email_does_not_crash(self, client, patch_server_data):
        """Tests a login with an email not in the database"""
        response = client.post("/showSummary", data={"email": "nope@nope.com"})
        assert response.status_code != 500

    def test_empty_email_does_not_crash(self, client, patch_server_data):
        """Tests a login submitted with an empty email field"""
        response = client.post("/showSummary", data={"email": ""})
        assert response.status_code != 500

    def test_error_message_on_invalid_email(self, client, patch_server_data):
        """Error message must appear in the response when email not found"""
        response = client.post("/showSummary", data={"email": "nope@nope.com"})
        assert b"Please enter a valid email address" in response.data

    # ---------------------------------------------------------------------------
    # Happy path
    # ---------------------------------------------------------------------------
    def test_valid_email_returns_200(self, client, patch_server_data):
        """Tests a login submitted with a valid email address"""
        # Makes request to POST email in form
        response = client.post("/showSummary", data={"email": "powerup@lifting.com"})
        # Make assertion that it's a 200 success
        assert response.status_code == 200

# ---------------------------------------------------------------------------
# Test Booking Functionality
# ---------------------------------------------------------------------------

class TestBooking:
    """Tests for the book() route '/book/<competition>/<club>'"""
    # ---------------------------------------------------------------------------
    # Happy path
    # ---------------------------------------------------------------------------
    def test_found_club_and_competition_references(self, client, patch_server_data):
        """Test that the booking route matches Database"""
        response = client.get("/book/Spring Festival/PowerUP Lifting")
        assert response.status_code == 200

    # ---------------------------------------------------------------------------
    # Sad path
    # ---------------------------------------------------------------------------
    def test_unfound_competition_returns_404(self, client, patch_server_data):
        """Invalid competition should return 404"""
        response = client.get("/book/Summer Time Competition/PowerUP Lifting")
        assert response.status_code == 404

# ---------------------------------------------------------------------------
# Test Reservations for Competitions
# ---------------------------------------------------------------------------

class TestReservationPurchases:
    """Tests for the Reservation making route '/purchasePlaces'"""

    # ---------------------------------------------------------------------------
    # Happy path
    # ---------------------------------------------------------------------------
    def test_successful_reservation(self, client, patch_server_data):
        """Test the successful POST of a form to reserve places = 200 status code"""
        response = client.post(
            "/purchasePlaces",
            data={
                "competition": "Spring Festival",
                "club": "PowerUP Lifting",
                "places": "8"
            }
        )
        assert response.status_code == 200

    def test_reservation_success_message(self, client, patch_server_data):
        """Test the success messaging if posted"""
        response = client.post(
            "/purchasePlaces",
            data={
                "competition": "Spring Festival",
                "club": "PowerUP Lifting",
                "places": "8"
            }
        )
        assert b"Great-booking complete!" in response.data

    def test_compet_num_places_available_decrease(self, client, patch_server_data):
        """
        Verifies that following a reservation, the total number of places available for that competition
        is decreased by the same amount.
        """

        before = int(server.competitions[0]["numberOfPlaces"])

        client.post(
            "/purchasePlaces",
            data={
                "competition": "Spring Festival",
                "club": "PowerUP Lifting",
                "places": "8"
            }
        )

        after = int(server.competitions[0]["numberOfPlaces"])

        assert after == before - 8

    def test_num_club_points_avail_decrease_after_reservation(self, client, patch_server_data):
        """
        Verifies that the club's database file is updated with points available after reservations.
        """

        before = int(server.clubs[0]["points"])

        client.post(
            "/purchasePlaces",
            data={
                "competition": "Spring Festival",
                "club": "PowerUP Lifting",
                "places": "8"
            }
        )

        after = int(server.clubs[0]["points"])

        assert after == before - 8

    # ---------------------------------------------------------------------------
    # Sad path
    # ---------------------------------------------------------------------------

    def test_unknown_competition_does_not_crash(self, client, patch_server_data):
        """Competition name not in database should not cause IndexError"""
        response = client.post("/purchasePlaces", data={
            "competition": "Nonexistent Cup",
            "club": "PowerUP Lifting",
            "places": "2"
        })
        assert response.status_code == 200  # stays on welcome.html

    def test_unknown_club_does_not_crash(self, client, patch_server_data):
        """Club name not in database should not cause IndexError"""
        response = client.post("/purchasePlaces", data={
            "competition": "Spring Festival",
            "club": "Nonexistent Club",
            "places": "2"
        })
        assert response.status_code == 302  # redirects to index

    def test_club_reservations_blocked_at_max_12(self, client, patch_server_data):
        """
        Checks that a single booking cannot exceed the maximum number of reservations (12 places)
        """
        before = int(server.competitions[0]["numberOfPlaces"])

        client.post(
            "/purchasePlaces",
            data={
                "competition": "Spring Festival",
                "club": "PowerUP Lifting",
                "places": "13"
            }
        )

        after = int(server.competitions[0]["numberOfPlaces"])
        assert after == before   # booking was blocked

    def test_club_blocked_from_reservation_if_missing_points(self, client, patch_server_data):
        """
        Blocks a club from reserving more places than their points allow
        """


        before = int(server.clubs[1]["points"])

        # The club StrongWoMen only has 8 points, but tries to reserve 10 places
        response = client.post(
            "/purchasePlaces",
            data={
                "competition": "Spring Festival",
                "club": "StrongWoMen",
                "places": "10"
            }
        )

        after = int(server.clubs[1]["points"])

        assert before == after  # places unchanged — booking was blocked

    def test_failed_reservation_message(self, client, patch_server_data):
        pass

    def test_club_blocked_if_not_enough_places_available(self, client, patch_server_data):
        """A booking cannot exceed the number of places available in the competition"""
        pass