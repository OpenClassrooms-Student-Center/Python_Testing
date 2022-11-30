from tests.mocked_json import MockedJson


class TestLoginLogout:

    def test_login_then_logout(self, client, monkeypatch):

        MockedJson.generate_a_new_test_file('clubs')
        MockedJson.monkeypatch_json_functions(monkeypatch)

        response = client.get("/")
        assert response.status_code == 200
        assert "Welcome to the GUDLFT" in response.text

        response = client.post("/login", data={"email": "test2@mail.com"}, follow_redirects=True)
        assert response.status_code == 200
        assert "Welcome, test2@mail.com" in response.text

        response = client.get("/logout", follow_redirects=True)
        assert response.status_code == 200
        assert "Welcome to the GUDLFT" in response.text

    def test_login_then_visit_all_routes(self, client, monkeypatch):

        MockedJson.generate_a_new_test_file('clubs')
        MockedJson.generate_a_new_test_file('competitions')
        MockedJson.monkeypatch_json_functions(monkeypatch)

        # ----------------------------------------------------------------------------------------------------
        # Login and redirect to showCompetitions -------------------------------------------------------------
        response = client.post("/login", data={"email": "test@mail.com"}, follow_redirects=True)

        assert response.status_code == 200
        assert "Welcome, test@mail.com" in response.text

        assert "name_test_competition" in response.text
        assert "Remaining places: 41" in response.text
        assert '<a href="/book/name_test_competition">Book Places</a>' in response.text

        assert "name test competition 2" in response.text
        assert "Remaining places: 8" in response.text
        assert "Already booked by your club: 2" in response.text
        assert '<a href="/book/name%20test%20competition%202">Book Places</a>' in response.text

        assert "name_test_competition_3" in response.text
        assert "Remaining places: 8" in response.text
        assert "Already booked by your club: 12" in response.text
        assert '<a href="/book/name_test_competition_3">Book Places</a>' not in response.text

        assert "name_test_competition_4" in response.text
        assert "Remaining places: 15" in response.text
        assert "Already booked by your club: 9" in response.text
        assert '<a href="/book/name_test_competition_4">Book Places</a>' not in response.text

        # ----------------------------------------------------------------------------------------------------
        # ShowClubs ------------------------------------------------------------------------------------------
        response = client.get("/showClubs")

        assert response.status_code == 200
        assert 'name_test_club' in response.text
        assert 'name test club 2' in response.text
        assert 'name_test_club_3' in response.text

        # ----------------------------------------------------------------------------------------------------
        # Logout ---------------------------------------------------------------------------------------------
        response = client.get("/logout", follow_redirects=True)

        assert response.status_code == 200
        assert "Welcome to the GUDLFT" in response.text
