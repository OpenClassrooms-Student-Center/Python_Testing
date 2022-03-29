class TestLogin:

    def test_should_return_status_200(self, client, testing_data):

        user = testing_data["clubs"][3]["email"]
        response = client.post('/showSummary', data={"email": user})
        assert response.status_code == 200

    def test_should_return_message_no_match_email(self, client, testing_data):
        response = client.post('/showSummary', data={"email": "test@club.com"})
        data = response.data.decode()
        message = "Aucune adresse de club ne correspond"
        print(data)
        assert response.status_code == 200
        assert message in data
