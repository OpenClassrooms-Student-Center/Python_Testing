import pytest

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
        # Makes request to POST email in form
        response = client.post("/showSummary", data={"email": "powerup@lifting.com"})
        # Make assertion that it's a 200 success
        assert response.status_code == 200

