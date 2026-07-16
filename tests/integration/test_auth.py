"""Tests d'intégration de l'authentification, de la session et de la déconnexion."""
from flask import session


class TestIndex:
    def test_index_is_accessible(self, client):
        response = client.get("/")
        assert response.status_code == 200
        assert b"GUDLFT" in response.data


class TestLogin:
    def test_login_with_valid_email_creates_session(self, client):
        response = client.post("/showSummary", data={"email": "a@test.com"})
        assert response.status_code == 302  # POST-redirect-GET
        with client.session_transaction() as sess:
            assert sess["club_email"] == "a@test.com"

    def test_login_with_unknown_email_shows_error(self, client):
        response = client.post(
            "/showSummary", data={"email": "ghost@nowhere.com"}, follow_redirects=True
        )
        assert response.status_code == 200
        assert b"Email not found" in response.data

    def test_login_with_unknown_email_does_not_crash(self, client):
        # Régression : un email inconnu levait une IndexError (HTTP 500)
        response = client.post("/showSummary", data={"email": "ghost@nowhere.com"})
        assert response.status_code == 302


class TestSummaryAccess:
    def test_summary_requires_login(self, client):
        response = client.get("/showSummary")
        assert response.status_code == 302

    def test_summary_shown_when_logged_in(self, logged_in_client):
        response = logged_in_client.get("/showSummary")
        assert response.status_code == 200
        assert b"Points available" in response.data


class TestLogout:
    def test_logout_clears_session(self, logged_in_client):
        logout_response = logged_in_client.get("/logout")
        assert logout_response.status_code == 302
        with logged_in_client.session_transaction() as sess:
            assert "club_email" not in sess

    def test_routes_blocked_after_logout(self, logged_in_client):
        logged_in_client.get("/logout")
        response = logged_in_client.get("/showSummary")
        assert response.status_code == 302
