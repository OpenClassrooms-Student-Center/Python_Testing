from tests.mocked_json import MockedJson


class TestRoutesUnknownValues:
    """ Test the redirection when the given club or the competition is not found.
        The functions would raise a NameError and redirect to the first page. """

    def test_route_book_with_unknown_competition(self, client, monkeypatch):

        MockedJson.generate_a_new_test_file('clubs')
        MockedJson.generate_a_new_test_file('competitions')
        MockedJson.monkeypatch_json_functions(monkeypatch)

        with client.session_transaction() as session:
            session["logged_club"] = MockedJson.load_mocked_json('clubs')[0]  # name_test_club

        response = client.get('/book/name_test_competition_wrong', follow_redirects=True)

        assert response.status_code == 200
        assert "&#39;name_test_club&#39; or &#39;name_test_competition_wrong&#39; wasn&#39;t found" in response.text
        assert "List of competitions" in response.text

    def test_route_purchaseplaces_with_unknown_values(self, client, monkeypatch):

        MockedJson.generate_a_new_test_file('clubs')
        MockedJson.generate_a_new_test_file('competitions')
        MockedJson.monkeypatch_json_functions(monkeypatch)

        with client.session_transaction() as session:
            session["logged_club"] = MockedJson.load_mocked_json('clubs')[0]  # name_test_club

        response = client.post("/purchasePlaces",
                               data={"competition": "name_test_competition_wrong",
                                     "club": "name_test_club",
                                     "places": 5},
                               follow_redirects=True)

        assert response.status_code == 200
        assert "Sorry, &#39;name_test_competition_wrong&#39; or" in response.text
        assert "List of competitions" in response.text
