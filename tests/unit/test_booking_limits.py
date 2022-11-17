from tests.mocked_json import MockedJson


class TestBookingLimits:

    def test_connection(self, client, monkeypatch):

        # Create test files, then monkeypatch the json functions
        MockedJson.generate_a_new_test_file('clubs')
        MockedJson.generate_a_new_test_file('competitions')
        MockedJson.monkeypatch_json_functions(monkeypatch)

        response = client.get("/book/name_test_competition/name_test_club")
        assert response.status_code == 200

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

        response = client.post("/purchasePlaces", data={"competition": "name_test_competition",
                                                        "club": "name test club 2",
                                                        "places": 10000})

        assert response.status_code == 200
        assert "Points available: 5" in response.text
        assert "Remaining places: 41" in response.text
        assert "You are allowed to book 5 places maximum" in response.text

    def test_book_with_a_negative_number_or_text(self, client, monkeypatch):

        MockedJson.generate_a_new_test_file('clubs')
        MockedJson.generate_a_new_test_file('competitions')
        MockedJson.monkeypatch_json_functions(monkeypatch)

        # Competition : 41 places  | Club : 22 points | Booked : 0
        response = client.post("/purchasePlaces", data={"competition": "name_test_competition",
                                                        "club": "name_test_club",
                                                        "places": -1000})

        assert response.status_code == 200
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
        assert "Points available: 22" in response.text
        assert "Remaining places: 41" in response.text
