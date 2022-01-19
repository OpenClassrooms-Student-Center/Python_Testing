import server

# Constants
NUMBER_OF_CLUBS = 3
NUMBER_OF_COMPETITIONS = 2
POINT_FOR_PLACES = 1


class TestDatabase():

    def test_load_clubs(self):
        """
        Test that the clubs.json file is loaded correctly
        we know that the file is loaded correctly because
        listOfClubs has the same number of clubs as the
        clubs.json file
        """
        listOfClubs = server.loadClubs()
        assert len(listOfClubs) == NUMBER_OF_CLUBS

    def test_load_competitions(self):
        """
        Test that the competitions.json file is loaded correctly
        we know that the file is loaded correctly because
        listOfCompetitions has the same number of competitions as the
        competitions.json file
        """
        listOfCompetitions = server.loadCompetitions()
        assert len(listOfCompetitions) == NUMBER_OF_COMPETITIONS


class TestIndex():

    def test_status_code_200(self, client):
        """
        Test that the status code is 200
        """
        response = client.get('/')
        assert response.status_code == 200

    def test_index_should_return_the_right_template(self, client):
        response = client.get('/')
        assert response.status_code == 200
        assert ("GUDLFT Registration") in response.data.decode()


class TestSummary():

    def test_login_with_registered_email_status_code_200(self, client):
        email = "john@simplylift.co"
        response = client.post('/showSummary', data={'email': email})
        assert response.status_code == 200
        assert ("Welcome, " + email) in response.data.decode()

    def test_login_with_unregistered_email_status_code_200(self, client):
        email = "wrong@gmail.com"
        response = client.post('/showSummary', data={'email': email})
        assert response.status_code == 200
        assert ("Sorry") in response.data.decode()

    def test_with_no_email_status_code_200(self, client):
        no_email = ""
        response = client.post('/showSummary', data={'email': no_email})
        assert response.status_code == 200
        assert ("Please enter your email") in response.data.decode()

    def test_should_return_the_right_template(self, client):
        email = "john@simplylift.co"
        response = client.post('/showSummary', data={'email': email})
        assert response.status_code == 200
        assert ("Summary | GUDLFT Registration") in response.data.decode()


class TestBooking():

    def test_satus_code_200(self, client):
        competition_name = "Spring Festival"
        club_name = "Simply Lift"
        response = client.get('/booking/' + competition_name + '/' + club_name)
        assert response.status_code == 200

    def test_too_many_places_wanted_error_message(self, client):
        response = client.post(
            '/purchasePlaces',
            data={'places': '13',
                  'competition': 'Spring Festival',
                  'club': 'Simply Lift'})
        assert str(response.data).find("book more than 12 places") > 0

    def test_club_points_required_to_book_event_are_deducted(self, client):
        club_points = server.clubs[3]['points']
        client.post(
            '/purchasePlaces',
            data={'places': '1',
                  'club': 'club_test',
                  'competition': 'competition_test'},
            follow_redirects=True)
        club_points_left = server.clubs[3]['points']
        assert club_points_left == 10

    def test_booking_message_displays_when_successful_booking(self, client):
        r = client.post(
            '/purchasePlaces',
            data={'places': '1',
                  'club': 'club_test',
                  'competition': 'competition_test'},
            follow_redirects=True
        )
        assert "booking complete" in r.data.decode()

    def test_message_displays_when_not_enough_points(self, client):
        pass

    def test_club_is_not_registered_for_competition(self, client):
        pass

    def test_register_a_club_for_competition(self, client):
        pass

    def test_competition_is_in_the_past(self, client):
        pass

    def test_competition_is_in_the_future(self, client):
        pass


class TestShowPoints():

    def test_status_code_200(self, client):
        response = client.get('/showPoints')
        assert response.status_code == 200

    def test_list_list_of_clubs_should_be_displayed(self, client):
        response = client.get('/showPoints')
        assert response.status_code == 200
        assert ("List of clubs") in response.data.decode()

    def test_book_url_if_competition_and_club_exists(client):
        club = "Simply Lift"

        competitions = server.loadCompetitions()

        for competition in competitions:
            if int(competition['numberOfPlaces']) > 0:
                r = client.get('/book/' + competition['name'] + '/' + club)
                assert r.status_code == 200

    def test_book_url_if_competition_does_not_exist(client):
        club = "Simply Lift"
        wrong_competition = "Wrong Competition"

        competitions = server.loadCompetitions()

        for competition in competitions:
            if int(competition['numberOfPlaces']) > 0:
                r = client.get('/book/' + wrong_competition + '/' + club)
                message_expected = 'Something went wrong'
                data = r.get_data(as_text=True)
                assert message_expected in data

    def test_book_url_if_club_does_not_exist(client):
        wrong_club = "Wrong Club"

        competitions = server.loadCompetitions()

        for competition in competitions:
            if int(competition['numberOfPlaces']) > 0:
                r = client.get('/book/' + competition['name'] + '/' + wrong_club)  # noqa
                message_expected = 'Something went wrong'
                data = r.get_data(as_text=True)
                assert message_expected in data


class TestLogout():

    def test_logout(self, client):
        response = client.get('/logout')
        assert response.status_code == 302
