class TestRoutesUnknownValues:
    """ Test the redirection when the given club or the competition is not found.
        The functions would raise a NameError and redirect to the first page. """

    def test_route_showcompetition_with_unknown_values(self, client):

        response = client.get('/showCompetitions/name_test_club_wrong', follow_redirects=True)

        assert response.status_code == 200
        assert "Welcome to the GUDLFT" in response.text

    def test_route_book_with_unknown_values(self, client):

        response = client.get('/book/name_test_competition_wrong/name_test_club_wrong', follow_redirects=True)

        assert response.status_code == 200
        assert "Welcome to the GUDLFT" in response.text

    def test_route_purchaseplaces_with_unknown_values(self, client):

        response = client.post("/purchasePlaces",
                               data={"competition": "name_test_competition_wrong",
                                     "club": "name_test_club_wrong",
                                     "places": 5},
                               follow_redirects=True)

        assert response.status_code == 200
        assert "Welcome to the GUDLFT" in response.text

    def test_route_showclubs_with_unknown_values(self, client):

        response = client.get('/show_clubs/name_test_club_wrong', follow_redirects=True)

        assert response.status_code == 200
        assert "Welcome to the GUDLFT" in response.text
