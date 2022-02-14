
class TestIntegration:

    def test_should_go_to_index_and_go_to_welcome(self, client, test_club):
        client.get("/")
        data = {"email": test_club[0]["email"]}
        response = client.post("/showSummary", data=data)
        assert response.status_code == 200

    def test_should_get_index_and_logout(self, client, test_club):
        client.get("/")
        client.get("/logout")
        data = {"email": test_club[0]["email"]}
        response = client.post("/showSummary", data=data)
        assert response.status_code == 200
    
