import server

class TestLoginIntegration:
    """Integration tests for login using real clubs.json data"""

    def test_valid_real_email_returns_200(self, client):
        """Login with a real email from clubs.json should succeed"""
        response = client.post(
            "/showSummary",
            data={"email": "john@simplylift.co"})
        assert response.status_code == 200