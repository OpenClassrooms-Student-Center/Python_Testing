from tests.unit.test_json import MockedJson


class TestBookingLimits:

    # def test_check_booking_links(self, client, monkeypatch):
        # """ The third competition is passed, it has to be displayed, without the link to book though. """

        # MockedJson.generate_a_new_test_file('clubs')
        # MockedJson.generate_a_new_test_file('competitions')
        # MockedJson.monkeypatch_json_functions(monkeypatch)

        # response = client.post("/showSummary", data={"email": "test@mail.com"})

        # assert response.status_code == 200
        # assert '<a href="/book/name_test_competition/name_test_club">Book Places</a>' in response.text
        # assert '<a href="/book/name%20test%20competition%202/name_test_club">Book Places</a>' in response.text
        # assert '<a href="/book/name_test_competition_3/name_test_club">Book Places</a>' not in response.text



    def test_connection(self, client, monkeypatch):

        # Create test files, then monkeypatch the json functions
        MockedJson.generate_a_new_test_file('clubs')
        MockedJson.generate_a_new_test_file('competitions')
        MockedJson.monkeypatch_json_functions(monkeypatch)

        # Connection
        response = client.get("/book/name_test_competition/name_test_club")

        assert response.status_code == 200

    def test_book_ui_limits(self, client, monkeypatch):
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

    def test_booking_ok(self, client, monkeypatch):
        """ Check a regular booking """

        MockedJson.generate_a_new_test_file('clubs')
        MockedJson.generate_a_new_test_file('competitions')
        MockedJson.monkeypatch_json_functions(monkeypatch)

        response = client.post("/purchasePlaces", data={"competition": "name_test_competition",
                                                        "club": "name_test_club",
                                                        "places": 5})

        assert response.status_code == 200
        assert "Welcome, test@mail.com" in response.text
        assert "Points available: 17" in response.text
        assert "Remaining places: 36" in response.text

    def test_book_with_10000_places(self, client, monkeypatch):

        MockedJson.generate_a_new_test_file('clubs')
        MockedJson.generate_a_new_test_file('competitions')
        MockedJson.monkeypatch_json_functions(monkeypatch)

        response = client.get('/book/name_test_competition/name test club 2')
        assert 'min="1" max="5"' in response.text

        response = client.post("/purchasePlaces", data={"competition": "name_test_competition",
                                                        "club": "name test club 2",
                                                        "places": 10000})

        assert response.status_code == 200
        assert "Welcome, test2@mail.com" in response.text
        assert "Points available: 5" in response.text
        assert "Remaining places: 41" in response.text
        assert "You are allowed to book 5 places maximum" in response.text

    def test_book_with_a_negative_number_or_text(self, client, monkeypatch):

        MockedJson.generate_a_new_test_file('clubs')
        MockedJson.generate_a_new_test_file('competitions')
        MockedJson.monkeypatch_json_functions(monkeypatch)

        response = client.post("/purchasePlaces", data={"competition": "name_test_competition",
                                                        "club": "name_test_club",
                                                        "places": -1000})

        assert response.status_code == 200
        assert "Welcome, test@mail.com" in response.text
        assert "Points available: 22" in response.text
        assert "Remaining places: 41" in response.text
        assert "Invalid value" in response.text

        response = client.post("/purchasePlaces", data={"competition": "name_test_competition",
                                                        "club": "name_test_club",
                                                        "places": ""})

        assert response.status_code == 200
        assert "Invalid value" in response.text

        response = client.post("/purchasePlaces", data={"competition": "name_test_competition",
                                                        "club": "name_test_club",
                                                        "places": "aaaaaa"})

        assert response.status_code == 200
        assert "Invalid value" in response.text

    def test_book_more_places_than_available(self, client, monkeypatch):

        MockedJson.generate_a_new_test_file('clubs')
        MockedJson.generate_a_new_test_file('competitions')
        MockedJson.monkeypatch_json_functions(monkeypatch)

        # Competition : 8 places  | Club : 22 points | Booked : 2
        # Book 10 places will fail
        response = client.post("/purchasePlaces", data={"competition": "name test competition 2",
                                                        "club": "name_test_club",
                                                        "places": 10})

        assert "Points available: 22" in response.text
        assert "Remaining places: 8" in response.text
        assert "You are allowed to book 8 places maximum" in response.text

    def test_book_more_places_than_club_points(self, client, monkeypatch):

        MockedJson.generate_a_new_test_file('clubs')
        MockedJson.generate_a_new_test_file('competitions')
        MockedJson.monkeypatch_json_functions(monkeypatch)

        # Competition : 41 places  | Club : 5 points | Booked : 0
        # Book 10 places will fail
        response = client.post("/purchasePlaces", data={"competition": "name_test_competition",
                                                        "club": "name test club 2",
                                                        "places": 10})

        assert "Points available: 5" in response.text
        assert "Remaining places: 41" in response.text
        assert "You are allowed to book 5 places maximum" in response.text

    def test_booking_link_displayed_only_for_comp_with_places(self, client, monkeypatch):

        """ Test for three users, if the booking links are displayed or not. """

        MockedJson.generate_a_new_test_file('clubs')
        MockedJson.generate_a_new_test_file('competitions')
        MockedJson.monkeypatch_json_functions(monkeypatch)

        # Club 1 : already booked 12 in the third competition
        response = client.post("/showSummary", data={"email": "test@mail.com"})

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

        assert '<a href="/book/name_test_competition/name_test_club_3">Book Places</a>' not in response.text
        assert '<a href="/book/name%20test%20competition%202/name_test_club_3">Book Places</a>' not in response.text
        assert '<a href="/book/name_test_competition_3/name_test_club_3">Book Places</a>' not in response.text

    def test_book_more_than_12_places_in_several_steps(self, client, monkeypatch):
        """ Book places and check the informations in returnself.
            The differents numbers, a potential message and the booking link existence """

        MockedJson.generate_a_new_test_file('clubs')
        MockedJson.generate_a_new_test_file('competitions')
        MockedJson.monkeypatch_json_functions(monkeypatch)

        # Competition : 41 places  | Club : 22 points | Booked : 0
        # Book 6 places
        response = client.post("/purchasePlaces", data={"competition": "name_test_competition",
                                                        "club": "name_test_club",
                                                        "places": 6})

        assert "Points available: 16" in response.text
        assert "Remaining places: 35" in response.text
        assert "Already booked by your club: 6" in response.text

        assert '<a href="/book/name_test_competition/name_test_club">Book Places</a>' in response.text
        assert '<a href="/book/name%20test%20competition%202/name_test_club">Book Places</a>' in response.text

        # Competition : 35 places  | Club : 16 points | Booked : 6
        # Book 10 places will fail
        response = client.post("/purchasePlaces", data={"competition": "name_test_competition",
                                                        "club": "name_test_club",
                                                        "places": 10})

        assert "Points available: 16" in response.text
        assert "Remaining places: 35" in response.text
        assert "Already booked by your club: 6" in response.text
        assert "You are allowed to book 6 places maximum" in response.text

        assert '<a href="/book/name_test_competition/name_test_club">Book Places</a>' in response.text
        assert '<a href="/book/name%20test%20competition%202/name_test_club">Book Places</a>' in response.text

        # Competition : 35 places  | Club : 16 points | Booked : 6
        # Book 6 places
        response = client.post("/purchasePlaces", data={"competition": "name_test_competition",
                                                        "club": "name_test_club",
                                                        "places": 6})

        assert "Points available: 10" in response.text
        assert "Remaining places: 29" in response.text
        assert "Already booked by your club: 12" in response.text

        assert '<a href="/book/name_test_competition/name_test_club">Book Places</a>' not in response.text
        assert '<a href="/book/name%20test%20competition%202/name_test_club">Book Places</a>' in response.text

        # Competition : 29 places  | Club : 10 points | Booked : 12 (maximum)
        # Book 8 places (will fail)
        response = client.post("/purchasePlaces", data={"competition": "name_test_competition",
                                                        "club": "name_test_club",
                                                        "places": 8})

        assert "Points available: 10" in response.text
        assert "Remaining places: 29" in response.text
        assert "Already booked by your club: 12" in response.text
        assert "You are allowed to book 0 places maximum" in response.text

        assert '<a href="/book/name_test_competition/name_test_club">Book Places</a>' not in response.text
        assert '<a href="/book/name%20test%20competition%202/name_test_club">Book Places</a>' in response.text
