from tests.unit.test_json import MockedJson


class TestBooking:

    def test_connection(self, client, monkeypatch):

        # Create test files, then monkeypatch the json functions
        MockedJson.generate_a_new_test_file('clubs')
        MockedJson.generate_a_new_test_file('competitions')
        MockedJson.monkeypatch_json_functions(monkeypatch)

        # Connection
        response = client.get("/book/name_test_competition/name_test_club")

        assert response.status_code == 200

    def test_book_a_competition_ok(self, client, monkeypatch):

        # Create test files, then monkeypatch the json functions
        MockedJson.generate_a_new_test_file('clubs')
        MockedJson.generate_a_new_test_file('competitions')
        MockedJson.monkeypatch_json_functions(monkeypatch)

        response = client.post("/purchasePlaces", data={"competition": "name_test_competition",
                                                        "club": "name_test_club",
                                                        "places": 5})

        assert response.status_code == 200
        assert "Welcome, test@mail.com" in response.text
        assert "Points available: 17" in response.text
        assert "Number of Places: 36" in response.text

    def test_book_a_competition_with_too_much_places(self, client, monkeypatch):

        MockedJson.generate_a_new_test_file('clubs')
        MockedJson.generate_a_new_test_file('competitions')
        MockedJson.monkeypatch_json_functions(monkeypatch)

        response = client.post("/purchasePlaces", data={"competition": "name_test_competition",
                                                        "club": "name_test_club",
                                                        "places": 10000})

        assert response.status_code == 200
        assert "Welcome, test@mail.com" in response.text
        assert "Points available: 22" in response.text
        assert "Number of Places: 41" in response.text
        assert "You are allowed to book 22 places maximum" in response.text

    def test_book_a_competition_with_a_negative_number(self, client, monkeypatch):

        MockedJson.generate_a_new_test_file('clubs')
        MockedJson.generate_a_new_test_file('competitions')
        MockedJson.monkeypatch_json_functions(monkeypatch)

        response = client.post("/purchasePlaces", data={"competition": "name_test_competition",
                                                        "club": "name_test_club",
                                                        "places": -1000})

        assert response.status_code == 200
        assert "Welcome, test@mail.com" in response.text
        assert "Points available: 22" in response.text
        assert "Number of Places: 41" in response.text
        assert "You are allowed to book 22 places maximum" in response.text
