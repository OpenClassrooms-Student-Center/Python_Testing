
class TestIntegration:

    def test_go_to_index_and_go_to_welcome(self, client, test_club):
        client.get("/")
        data = {"email": test_club[0]["email"]}
        response = client.post("/showSummary", data=data)
        assert response.status_code == 200

    def test_get_index_and_logout(self, client, test_club):
        client.get("/")
        client.get("/logout")
        data = {"email": test_club[0]["email"]}
        response = client.post("/showSummary", data=data)
        assert response.status_code == 200

    def test_booking_place(self, client, test_valid_data):
        assert client.get('/').status_code == 200
        client.get(f"/book/{test_valid_data['competition']}/{test_valid_data['club']}")
        response = client.post("/purchasePlaces", data=test_valid_data)
        assert response.status_code == 200
        assert client.get("/logout").status_code == 302
