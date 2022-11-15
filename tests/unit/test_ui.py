from tests.unit.test_json import MockedJson


class TestUI:

    def test_booking_ui_maximum_allowed(self, client, monkeypatch):
        """ Check UI limits with severals competition / club combinations """

        # Create test files, then monkeypatch the json functions
        MockedJson.generate_a_new_test_file('clubs')
        MockedJson.generate_a_new_test_file('competitions')
        MockedJson.monkeypatch_json_functions(monkeypatch)

        # Competition : 41 places  | Club : 22 points | Booked : 0
        response = client.get('/book/name_test_competition/name_test_club')
        assert response.status_code == 200
        assert 'name="places" value="1" min="1" max="12"' in response.text

        # Competition : 41 places  | Club : 5 points | Booked : 0
        response = client.get('/book/name_test_competition/name test club 2')
        assert 'name="places" value="1" min="1" max="5"' in response.text

        # Competition : 8 places  | Club : 22 points | Booked : 2
        response = client.get('/book/name test competition 2/name_test_club')
        assert 'name="places" value="1" min="1" max="8"' in response.text

        # Competition : 8 places  | Club : 5 points | Booked : 11
        response = client.get('/book/name test competition 2/name test club 2')
        assert 'name="places" value="1" min="1" max="1"' in response.text

    def test_booking_link_displayed_only_for_comp_with_places(self, client, monkeypatch):
        """ Test for three users, if the booking links are displayed or not. """

        MockedJson.generate_a_new_test_file('clubs')
        MockedJson.generate_a_new_test_file('competitions')
        MockedJson.monkeypatch_json_functions(monkeypatch)

        # Club 1 : already booked 12 in the third competition
        response = client.post("/showSummary", data={"email": "test@mail.com"})

        assert response.status_code == 200
        assert '<a href="/book/name_test_competition/name_test_club">Book Places</a>' in response.text
        assert '<a href="/book/name%20test%20competition%202/name_test_club">Book Places</a>' in response.text
        assert '<a href="/book/name_test_competition_3/name_test_club">Book Places</a>' not in response.text

        # Club 2 : all competitions are available
        response = client.post("/showSummary", data={"email": "test2@mail.com"})

        assert response.status_code == 200
        assert '<a href="/book/name_test_competition/name%20test%20club%202">Book Places</a>' in response.text
        assert '<a href="/book/name%20test%20competition%202/name%20test%20club%202">Book Places</a>' in response.text
        assert '<a href="/book/name_test_competition_3/name%20test%20club%202">Book Places</a>' in response.text

        # Club 3 : 0 point left, no link displayed
        response = client.post("/showSummary", data={"email": "test3@mail.com"})

        assert response.status_code == 200
        assert '<a href="/book/name_test_competition/name_test_club_3">Book Places</a>' not in response.text
        assert '<a href="/book/name%20test%20competition%202/name_test_club_3">Book Places</a>' not in response.text
        assert '<a href="/book/name_test_competition_3/name_test_club_3">Book Places</a>' not in response.text

    def test_booking_link_not_displayed_for_old_competitions(self, client, monkeypatch):
        """ The third competition is passed, it has to be displayed, without the link to book though. """

        MockedJson.generate_a_new_test_file('clubs')
        MockedJson.generate_a_new_test_file('competitions')
        MockedJson.monkeypatch_json_functions(monkeypatch)

        response = client.post("/showSummary", data={"email": "test@mail.com"})

        assert response.status_code == 200
        assert '<a href="/book/name_test_competition/name_test_club">Book Places</a>' in response.text
        assert '<a href="/book/name%20test%20competition%202/name_test_club">Book Places</a>' in response.text
        assert '<a href="/book/name_test_competition_3/name_test_club">Book Places</a>' not in response.text
