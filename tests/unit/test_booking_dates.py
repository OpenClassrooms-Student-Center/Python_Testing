from tests.unit.test_json import MockedJson


class TestBookingDates:

    def test_booking_ok(self, client, monkeypatch):

        MockedJson.generate_a_new_test_file('clubs')
        MockedJson.generate_a_new_test_file('competitions')
        MockedJson.monkeypatch_json_functions(monkeypatch)

        # Competition : 8 places  | Club : 22 points | Booked : 2 | Date limit : 2025-01-01 10:00:00
        response = client.post("/purchasePlaces", data={"competition": "name test competition 2",
                                                        "club": "name_test_club",
                                                        "places": 6})

        assert response.status_code == 200
        assert "Welcome, test@mail.com" in response.text
        assert "Points available: 16" in response.text
        assert "Remaining places: 2" in response.text

    def test_booking_in_a_past_competition(self, client, monkeypatch):

        MockedJson.generate_a_new_test_file('clubs')
        MockedJson.generate_a_new_test_file('competitions')
        MockedJson.monkeypatch_json_functions(monkeypatch)

        # Competition : 41 places  | Club : 22 points | Booked : 0 | Date limit : 2020-03-27 10:00:00
        response = client.post("/purchasePlaces", data={"competition": "name_test_competition",
                                                        "club": "name_test_club",
                                                        "places": 5})

        assert response.status_code == 200
        assert "Welcome, test@mail.com" in response.text
        # assert "Points available: 22" in response.text
        # assert "Remaining places: 41" in response.text
