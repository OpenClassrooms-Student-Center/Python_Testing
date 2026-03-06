import pytest


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

