from tests.unit.test_json import MockedJson


class TestBooking:

    def test_complete_booking_process(self, client, monkeypatch):
        """ Book places and check the informations in return:
                - point balance
                - messages
                - ui limits
                - booking links displayed or not
        """

        MockedJson.generate_a_new_test_file('clubs')
        MockedJson.generate_a_new_test_file('competitions')
        MockedJson.monkeypatch_json_functions(monkeypatch)

        # First, login
        response = client.post("/login", data={"email": "test@mail.com"}, follow_redirects=True)
        assert response.status_code == 200
        assert "Welcome, test@mail.com" in response.text

        # Redirected to the competitions
        assert "List of competitions" in response.text

        # Is competition 1 available with informations and the link to book ?
        assert "name_test_competition" in response.text
        assert "Date: 2027-03-27 10:00:00" in response.text
        assert '<a href="/book/name_test_competition">Book Places</a>' in response.text

        # UI limitations
        response = client.get('/book/name_test_competition')
        assert 'name="places" value="1" min="1" max="12"' in response.text

        # Let's book -->

        # ----------------------------------------------------------------------------------------------------
        # Book 6 places --------------------------------------------------------------------------------------
        # Competition : 41 places | Club : 22 points | Booked : 0
        response = client.post("/purchasePlaces", data={"competition": "name_test_competition",
                                                        "club": "name_test_club",
                                                        "places": 6})

        assert "Great-booking complete" in response.text

        assert "Points available: 16" in response.text
        assert "Remaining places: 35" in response.text
        assert "Already booked by your club: 6" in response.text
        assert '<a href="/book/name_test_competition">Book Places</a>' in response.text

        # New UI limitations
        response = client.get('/book/name_test_competition')
        assert 'name="places" value="1" min="1" max="6"' in response.text

        # ----------------------------------------------------------------------------------------------------
        # Book 10 places will fail ---------------------------------------------------------------------------
        # Competition : 35 places | Club : 16 points | Booked : 6
        response = client.post("/purchasePlaces", data={"competition": "name_test_competition",
                                                        "club": "name_test_club",
                                                        "places": 10})

        assert "You are allowed to book 6 places maximum" in response.text

        # Points balance doesn't change
        assert "Points available: 16" in response.text
        assert "Remaining places: 35" in response.text
        assert "Already booked by your club: 6" in response.text
        assert '<a href="/book/name_test_competition">Book Places</a>' in response.text

        # Same UI limitations
        response = client.get('/book/name_test_competition')
        assert 'name="places" value="1" min="1" max="6"' in response.text

        # ----------------------------------------------------------------------------------------------------
        # Book 6 places --------------------------------------------------------------------------------------
        # Competition : 35 places | Club : 16 points | Booked : 6
        response = client.post("/purchasePlaces", data={"competition": "name_test_competition",
                                                        "club": "name_test_club",
                                                        "places": 6})

        assert "Great-booking complete" in response.text

        assert "Points available: 10" in response.text
        assert "Remaining places: 29" in response.text
        assert "Already booked by your club: 12" in response.text

        # The booking link must be hidden
        assert '<a href="/book/name_test_competition">Book Places</a>' not in response.text

        # New UI limitations
        response = client.get('/book/name_test_competition')
        assert 'name="places" value="1" min="1" max="0"' in response.text

        # ----------------------------------------------------------------------------------------------------
        # Book 8 places will fail ----------------------------------------------------------------------------
        # Competition : 29 places | Club : 10 points | Booked : 12 (maximum)
        response = client.post("/purchasePlaces", data={"competition": "name_test_competition",
                                                        "club": "name_test_club",
                                                        "places": 8})

        assert "You are allowed to book 0 places maximum" in response.text

        assert "Points available: 10" in response.text
        assert "Remaining places: 29" in response.text
        assert "Already booked by your club: 12" in response.text

        # ----------------------------------------------------------------------------------------------------
        # Logout ---------------------------------------------------------------------------------------------
        response = client.get("/logout", follow_redirects=True)

        assert response.status_code == 200
        assert "Welcome to the GUDLFT" in response.text

        # ----------------------------------------------------------------------------------------------------
        # ShowClubs (login not necessary) --------------------------------------------------------------------
        response = client.get("/showClubs")

        assert response.status_code == 200
        assert 'name_test_club' in response.text
        assert 'name test club 2' in response.text
        assert 'name_test_club_3' in response.text
