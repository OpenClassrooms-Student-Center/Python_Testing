import server
from server import app


class TestLogin:

    client = app.test_client()

    club = [
        {
            "email": "test_club@email.com"
        }
    ]

    def setup_method(self):
        server.clubs = self.club

    def test_email_ok(self):
        result = self.client.post("/showSummary", data={"email": "test_club@email.com"})
        assert result.status_code == 200

    def test_invalid_email(self):
        result = self.client.post("/showSummary", data={"email": "test@test.com"})
        assert result.status_code == 403

    def test_empty_email(self):
        result = self.client.post("/showSummary", data={"email": ""})
        assert result.status_code == 403
