from tests.mocked_json import MockedJson


class TestLoginClass:

    def test_index(self, client):
        response = client.get("/")

        assert response.status_code == 200
        assert "Welcome to the GUDLFT" in response.text

    def test_login_fail(self, client):

        response = client.post("/showSummary", data={"email": "wrong@wrong.co"})

        assert response.status_code == 200
        assert "Welcome to the GUDLFT" in response.text
        assert "Sorry, &#39;wrong@wrong.co&#39; wasn&#39;t found" in response.text

    def test_login_with_empty_field(self, client):

        response = client.post("/showSummary", data={"email": ""})

        assert response.status_code == 200
        assert "Welcome to the GUDLFT" in response.text
        assert "Sorry, &#39;&#39; wasn&#39;t found" in response.text

    def test_login_success(self, client, monkeypatch):

        MockedJson.generate_a_new_test_file('clubs')
        MockedJson.monkeypatch_json_functions(monkeypatch)

        response = client.post("/showSummary", data={"email": "test@mail.com"}, follow_redirects=True)

        assert response.status_code == 200
        assert "Welcome, test@mail.com" in response.text
