from tests.mocked_json import MockedJson


class TestUI:

    def test_booking_ui_maximum_allowed(self, client, monkeypatch):
        """ Check UI limits with severals competition / club combinations """

        # Create test files, then monkeypatch the json functions
        MockedJson.generate_a_new_test_file('clubs')
        MockedJson.generate_a_new_test_file('competitions')
        MockedJson.monkeypatch_json_functions(monkeypatch)

        # Session : Club 1 ---
        with client.session_transaction() as session:
            session["logged_club"] = {'name': 'name_test_club'}

        # Competition : 41 places  | Club : 22 points | Booked : 0
        response = client.get('/book/name_test_competition')
        assert response.status_code == 200
        assert 'name="places" value="1" min="1" max="12"' in response.text

        # Competition : 8 places  | Club : 22 points | Booked : 2
        response = client.get('/book/name test competition 2')
        assert 'name="places" value="1" min="1" max="8"' in response.text

        # Session : Club 2 ---
        with client.session_transaction() as session:
            session["logged_club"] = {'name': 'name test club 2'}

        # Competition : 41 places  | Club : 5 points | Booked : 0
        response = client.get('/book/name_test_competition')
        assert 'name="places" value="1" min="1" max="5"' in response.text

        # Competition : 8 places  | Club : 5 points | Booked : 11
        response = client.get('/book/name test competition 2')
        assert 'name="places" value="1" min="1" max="1"' in response.text

    def test_booking_link_displayed_only_for_comp_with_places(self, client, monkeypatch):
        """ Test for three users, if the booking links are displayed or not. """

        MockedJson.generate_a_new_test_file('clubs')
        MockedJson.generate_a_new_test_file('competitions')
        MockedJson.monkeypatch_json_functions(monkeypatch)

        # Club 1 : already booked 12 in the third competition
        with client.session_transaction() as session:
            session["logged_club"] = MockedJson.load_mocked_json('clubs')[0]  # name_test_club

        response = client.get("/showCompetitions")

        assert response.status_code == 200
        assert '<a href="/book/name_test_competition">Book Places</a>' in response.text
        assert '<a href="/book/name%20test%20competition%202">Book Places</a>' in response.text
        assert '<a href="/book/name_test_competition_3">Book Places</a>' not in response.text

        # Club 2 : all competitions are available
        with client.session_transaction() as session:
            session["logged_club"] = MockedJson.load_mocked_json('clubs')[1]  # name test club 2

        response = client.get("/showCompetitions")

        assert response.status_code == 200
        assert '<a href="/book/name_test_competition">Book Places</a>' in response.text
        assert '<a href="/book/name%20test%20competition%202">Book Places</a>' in response.text
        assert '<a href="/book/name_test_competition_3">Book Places</a>' in response.text

        # Club 3 : 0 point left, no link displayed
        with client.session_transaction() as session:
            session["logged_club"] = MockedJson.load_mocked_json('clubs')[2]  # name_test_club_3

        response = client.get("/showCompetitions")

        assert response.status_code == 200
        assert '<a href="/book/name_test_competition">Book Places</a>' not in response.text
        assert '<a href="/book/name%20test%20competition%202">Book Places</a>' not in response.text
        assert '<a href="/book/name_test_competition_3">Book Places</a>' not in response.text

    def test_booking_link_not_displayed_for_old_competitions(self, client, monkeypatch):
        """ The third competition is passed, it has to be displayed, without the link to book though. """

        MockedJson.generate_a_new_test_file('clubs')
        MockedJson.generate_a_new_test_file('competitions')
        MockedJson.monkeypatch_json_functions(monkeypatch)

        with client.session_transaction() as session:
            session["logged_club"] = MockedJson.load_mocked_json('clubs')[0]  # name_test_club

        response = client.get("/showCompetitions")

        assert response.status_code == 200
        assert '<a href="/book/name_test_competition">Book Places</a>' in response.text
        assert '<a href="/book/name%20test%20competition%202">Book Places</a>' in response.text
        assert '<a href="/book/name_test_competition_3">Book Places</a>' not in response.text
