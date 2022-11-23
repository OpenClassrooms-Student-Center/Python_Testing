import json
from tests.mocked_json import MockedJson


def raise_json_decode(filename):
    raise json.JSONDecodeError(doc=filename, msg='prout', pos=0)


class TestRedirectionAfterDatabaseRaise:

    """ Test route behaviours with impossible access to database (raise a JSONDecodeError on each attempt) """

    def test_on_login(self, client, monkeypatch):

        monkeypatch.setattr('server.load_json', raise_json_decode)

        response = client.post("/login", data={"email": "test@mail.com"}, follow_redirects=True)
        assert response.status_code == 200
        assert "Database access failed" in response.text

    def test_on_show_competitions(self, client, monkeypatch):

        MockedJson.generate_a_new_test_file('clubs')
        MockedJson.monkeypatch_json_functions(monkeypatch)

        # Normal Connection
        response = client.post("/login", data={"email": "test@mail.com"}, follow_redirects=True)
        assert response.status_code == 200
        assert "Welcome, test@mail.com" in response.text

        # Then raise an error on each access
        monkeypatch.setattr('server.load_json', raise_json_decode)

        # Go to route
        response = client.get('/showCompetitions', follow_redirects=True)
        assert response.status_code == 200
        assert "Database access failed" in response.text

    def test_on_book(self, client, monkeypatch):

        MockedJson.generate_a_new_test_file('clubs')
        MockedJson.monkeypatch_json_functions(monkeypatch)

        # Normal Connection
        response = client.post("/login", data={"email": "test@mail.com"}, follow_redirects=True)
        assert response.status_code == 200
        assert "Welcome, test@mail.com" in response.text

        # Then raise an error on each access
        monkeypatch.setattr('server.load_json', raise_json_decode)
        monkeypatch.setattr('server.save_json', raise_json_decode)

        # Go to route
        response = client.get('/book/name_test_competition', follow_redirects=True)
        assert response.status_code == 200
        assert "Database access failed" in response.text

    def test_on_purchase_places(self, client, monkeypatch):

        MockedJson.generate_a_new_test_file('clubs')
        MockedJson.monkeypatch_json_functions(monkeypatch)

        # Normal Connection
        response = client.post("/login", data={"email": "test@mail.com"}, follow_redirects=True)
        assert response.status_code == 200
        assert "Welcome, test@mail.com" in response.text

        # Then raise an error on each access
        monkeypatch.setattr('server.load_json', raise_json_decode)
        monkeypatch.setattr('server.save_json', raise_json_decode)

        # Go to route
        response = client.post("/purchasePlaces",
                               data={"competition": "name_test_competition",
                                     "club": "name_test_club",
                                     "places": 1},
                               follow_redirects=True)
        assert response.status_code == 200
        assert "Database access failed" in response.text

    def test_on_show_clubs(self, client, monkeypatch):

        MockedJson.generate_a_new_test_file('clubs')
        MockedJson.monkeypatch_json_functions(monkeypatch)

        # Normal Connection
        response = client.post("/login", data={"email": "test@mail.com"}, follow_redirects=True)
        assert response.status_code == 200
        assert "Welcome, test@mail.com" in response.text

        # Then raise an error on each access
        monkeypatch.setattr('server.load_json', raise_json_decode)
        monkeypatch.setattr('server.save_json', raise_json_decode)

        # Go to route
        response = client.get('/showClubs', follow_redirects=True)
        assert response.status_code == 200
        assert "Database access failed" in response.text
