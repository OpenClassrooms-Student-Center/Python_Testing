from tests.mocked_json import MockedJson


class TestClubsList:

    def test_display_list(self, client, monkeypatch):

        # Create test files, then monkeypatch the json functions
        MockedJson.generate_a_new_test_file('clubs')
        MockedJson.monkeypatch_json_functions(monkeypatch)

        response = client.get('/showClubs')

        assert response.status_code == 200
        assert 'name_test_club' in response.text
        assert 'test@mail.com' in response.text
        assert 'Points: 22' in response.text

        assert 'name test club 2' in response.text
        assert 'test2@mail.com' in response.text
        assert 'Points: 5' in response.text

        assert 'name_test_club_3' in response.text
        assert 'test3@mail.com' in response.text
        assert 'Points: 0' in response.text
