def mock_load_json(file_name):

    if file_name == 'clubs':
        return [{"name": "Test club",
                 "email": "test@mail.com",
                 "points": "8"}]

    elif file_name == 'competitions':
        return [{"name": "Test_festival",
                 "date": "2020-03-27 10:00:00",
                 "numberOfPlaces": "12"}]

    else:
        return []


class TestLoginClass:

    def test_index(self, client):
        response = client.get("/")

        assert response.status_code == 200
        assert "Welcome to the GUDLFT" in response.text

    def test_login_fail(self, client, monkeypatch):

        monkeypatch.setattr('server.load_json', mock_load_json)
        response = client.post("/showSummary", data={"email": "wrong@mail.com"})

        assert response.status_code == 200
        assert "Welcome to the GUDLFT" in response.text
        assert "Sorry, wrong@mail.com wasn't found" in response.text

    def test_login_success(self, client, monkeypatch):

        monkeypatch.setattr('server.load_json', mock_load_json)
        response = client.post("/showSummary", data={"email": "test@mail.com"})

        assert response.status_code == 200
        assert "Welcome, test@mail.com" in response.text
