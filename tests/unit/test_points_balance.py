from tests.mocked_json import MockedJson


class TestPointsBalance:

    def test_balance_after_booking(self, client, monkeypatch):

        # Create test files, then monkeypatch the json functions
        MockedJson.generate_a_new_test_file('clubs')
        MockedJson.generate_a_new_test_file('competitions')
        MockedJson.monkeypatch_json_functions(monkeypatch)

        # Competition : 8 places  | Club : 22 points | Booked : 2
        response = client.get('/book/name%20test%20competition%202/name_test_club')

        assert response.status_code == 200
        assert "Remaining places for this competition: 8" in response.text
        assert "Already booked by your club: 2" in response.text
        assert "Club points: 22" in response.text
        assert "Available places for your club: 8" in response.text

        # --
        response = client.post("/purchasePlaces", data={"competition": "name test competition 2",
                                                        "club": "name_test_club",
                                                        "places": 3})

        assert response.status_code == 200
        assert "Points available: 19" in response.text
        assert "Remaining places: 5" in response.text
        assert "Already booked by your club: 5" in response.text

        # --
        response = client.post("/purchasePlaces", data={"competition": "name test competition 2",
                                                        "club": "name_test_club",
                                                        "places": 5})

        assert response.status_code == 200
        assert "Points available: 14" in response.text
        assert "Remaining places: 0" in response.text
        assert "Already booked by your club: 10" in response.text
