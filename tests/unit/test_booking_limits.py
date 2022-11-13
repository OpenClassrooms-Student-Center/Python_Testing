from tests.unit.test_json import MockedJson


class TestBookingLimits:

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
        assert 'min="1" max="12"' in response.text

        # Competition : 41 places  | Club : 5 points | Booked : 0
        response = client.get('/book/name_test_competition/name test club 2')
        assert 'min="1" max="5"' in response.text

        # Competition : 8 places  | Club : 22 points | Booked : 2
        response = client.get('/book/name test competition 2/name_test_club')
        assert 'min="1" max="8"' in response.text

        # Competition : 8 places  | Club : 5 points | Booked : 11
        response = client.get('/book/name test competition 2/name test club 2')
        assert 'min="1" max="1"' in response.text

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

    def test_book_with_a_negative_number(self, client, monkeypatch):

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

    def test_book_more_than_12_places_in_several_steps(self, client, monkeypatch):

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

        # Competition : 35 places  | Club : 16 points | Booked : 6
        # Book 10 places will fail
        response = client.post("/purchasePlaces", data={"competition": "name_test_competition",
                                                        "club": "name_test_club",
                                                        "places": 10})

        assert "Points available: 16" in response.text
        assert "Remaining places: 35" in response.text
        assert "Already booked by your club: 6" in response.text
        assert "You are allowed to book 6 places maximum" in response.text

        # Competition : 35 places  | Club : 16 points | Booked : 6
        # Book 6 places
        response = client.post("/purchasePlaces", data={"competition": "name_test_competition",
                                                        "club": "name_test_club",
                                                        "places": 6})

        assert "Points available: 10" in response.text
        assert "Remaining places: 29" in response.text
        assert "Already booked by your club: 12" in response.text

        # Competition : 29 places  | Club : 10 points | Booked : 12 (maximum)
        # Book 8 places (will fail)
        response = client.post("/purchasePlaces", data={"competition": "name_test_competition",
                                                        "club": "name_test_club",
                                                        "places": 8})

        assert "Points available: 10" in response.text
        assert "Remaining places: 29" in response.text
        assert "Already booked by your club: 12" in response.text
        assert "You are allowed to book 0 places maximum" in response.text
