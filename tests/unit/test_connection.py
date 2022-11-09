from tests.unit.test_json import MockedJson


class TestLoginClass:

    def test_index(self, client):
        response = client.get("/")

        assert response.status_code == 200
        assert "Welcome to the GUDLFT" in response.text

    def test_login_fail(self, client, monkeypatch):

        response = client.post("/showSummary", data={"email": "wrong@wrong.co"})

        assert response.status_code == 200
        assert "Welcome to the GUDLFT" in response.text
        assert "Sorry, wrong@wrong.co wasn't found" in response.text

    def test_login_success(self, client, monkeypatch):

        MockedJson.generate_a_new_test_file('clubs')
        MockedJson.monkeypatch_json_functions(monkeypatch)

        response = client.post("/showSummary", data={"email": "test@mail.com"})

        assert response.status_code == 200
        assert "Welcome, test@mail.com" in response.text
