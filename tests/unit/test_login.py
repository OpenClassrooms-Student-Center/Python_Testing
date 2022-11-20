from tests.mocked_json import MockedJson


class TestLoginClass:

    def test_index(self, client):
        response = client.get("/")

        assert response.status_code == 200
        assert "Welcome to the GUDLFT" in response.text

    def test_login_fail(self, client):

        response = client.post("/login", data={"email": "wrong@wrong.co"})

        assert response.status_code == 200
        assert "Welcome to the GUDLFT" in response.text
        assert "Sorry, &#39;wrong@wrong.co&#39; wasn&#39;t found" in response.text

    def test_login_with_empty_field(self, client):

        response = client.post("/login", data={"email": ""})

        assert response.status_code == 200
        assert "Welcome to the GUDLFT" in response.text
        assert "Sorry, &#39;&#39; wasn&#39;t found" in response.text

    def test_login_success(self, client, monkeypatch):

        MockedJson.generate_a_new_test_file('clubs')
        MockedJson.monkeypatch_json_functions(monkeypatch)

        response = client.post("/login", data={"email": "test@mail.com"}, follow_redirects=True)

        assert response.status_code == 200
        assert "Welcome, test@mail.com" in response.text

    # ----------------------------------------------------------------------------------------------------
    # Tests routes without being logged ------------------------------------------------------------------

    def test_showcompetitions_without_being_logged(self, client):

        response = client.get('/showCompetitions', follow_redirects=True)

        assert response.status_code == 200
        assert "Welcome to the GUDLFT Registration Portal!" in response.text

    def test_book_without_being_logged(self, client, monkeypatch):

        MockedJson.generate_a_new_test_file('competitions')
        MockedJson.monkeypatch_json_functions(monkeypatch)

        response = client.get('/book/name_test_competition', follow_redirects=True)

        assert response.status_code == 200
        assert "Welcome to the GUDLFT Registration Portal!" in response.text

    def test_purchaseplaces_without_being_logged(self, client):

        response = client.post("/purchasePlaces",
                               data={"competition": "name_test_competition",
                                     "club": "name test club 2",
                                     "places": 1},
                               follow_redirects=True)

        assert response.status_code == 200
        assert "Welcome to the GUDLFT Registration Portal!" in response.text

    def test_showclubs_without_being_logged(self, client):

        response = client.get('/showClubs', follow_redirects=True)

        assert response.status_code == 200
        assert "Welcome to the GUDLFT Registration Portal!" not in response.text
        assert "List of clubs" in response.text
