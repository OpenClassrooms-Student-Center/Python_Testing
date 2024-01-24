import server 

class TestShowSummary:
    def test_show_summary_valid_email(self, monkeypatch, client, clubs, competitions):
        monkeypatch.setattr(server, "competitions", competitions)
        monkeypatch.setattr(server, "clubs", clubs)
        
        response = client.post("/showSummary", data={"email": "john@simplylift.co"})

        assert response.status_code == 200

    def test_show_summary_invalid_email(self, monkeypatch, client, clubs, competitions):
        monkeypatch.setattr(server, "competitions", competitions)
        monkeypatch.setattr(server, "clubs", clubs)

        response = client.post("/showSummary", data={"email": "user@test.com"})

        assert response.status_code == 200
        assert b"Email not found." in response.data
