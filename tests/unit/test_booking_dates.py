from tests.mocked_json import MockedJson


class TestBookingDates:

    def test_booking_a_future_competition(self, client, monkeypatch):

        MockedJson.generate_a_new_test_file('clubs')
        MockedJson.generate_a_new_test_file('competitions')
        MockedJson.monkeypatch_json_functions(monkeypatch)

        # Force logged club
        with client.session_transaction() as session:
            session["logged_club"] = MockedJson.load_mocked_json('clubs')[0]  # name_test_club

        # Competition : 8 places  | Club : 22 points | Booked : 2 | Date limit : 2025-01-01 10:00:00
        response = client.post("/purchasePlaces", data={"competition": "name test competition 2",
                                                        "club": "name_test_club",
                                                        "places": 6})

        assert response.status_code == 200
        assert "Welcome, test@mail.com" in response.text
        assert "Points available: 16" in response.text
        assert "Remaining places: 2" in response.text
        assert "Great-booking complete" in response.text

    def test_booking_in_a_past_competition(self, client, monkeypatch):

        MockedJson.generate_a_new_test_file('clubs')
        MockedJson.generate_a_new_test_file('competitions')
        MockedJson.monkeypatch_json_functions(monkeypatch)

        # Force logged club
        with client.session_transaction() as session:
            session["logged_club"] = MockedJson.load_mocked_json('clubs')[0]  # name_test_club

        # Competition : 15 places  | Club : 22 points | Booked : 17 | Date limit : 2020-03-27 10:00:00
        response = client.post("/purchasePlaces", data={"competition": "name_test_competition_4",
                                                        "club": "name_test_club",
                                                        "places": 2})

        assert response.status_code == 200
        assert "Welcome, test@mail.com" in response.text
        assert "Points available: 22" in response.text
        assert "Remaining places: 15" in response.text
        assert "This competition is closed" in response.text
