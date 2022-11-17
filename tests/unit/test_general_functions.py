import pytest
from tests.mocked_json import MockedJson
from server import maximum_points_allowed, is_competition_pass_the_deadline, find_or_raise


class TestGeneralFunctions:

    def test_maximum_points_allowed(self):

        clubs = MockedJson.load_mocked_json('clubs')
        competitions = MockedJson.load_mocked_json('competitions')

        assert maximum_points_allowed(competitions[0], clubs[0]) == 12
        assert maximum_points_allowed(competitions[1], clubs[0]) == 8
        assert maximum_points_allowed(competitions[1], clubs[1]) == 1
        assert maximum_points_allowed(competitions[2], clubs[0]) == 0
        assert maximum_points_allowed(competitions[2], clubs[2]) == 0
        assert maximum_points_allowed(competitions[2], clubs[1]) == 5
        assert maximum_points_allowed(competitions[3], clubs[0]) == 3

    def test_is_competition_pass_the_deadline(self):

        competitions = MockedJson.load_mocked_json('competitions')

        assert is_competition_pass_the_deadline(competitions[0]) is False
        assert is_competition_pass_the_deadline(competitions[3]) is True

    def test_find_or_raise(self, monkeypatch):

        MockedJson.generate_a_new_test_file('clubs')
        MockedJson.generate_a_new_test_file('competitions')
        MockedJson.monkeypatch_json_functions(monkeypatch)

        club = find_or_raise('clubs', 'name_test_club')
        assert club['name'] == 'name_test_club'
        assert club['points'] == '22'

        competition = find_or_raise('competitions', 'name test competition 2')
        assert competition['name'] == 'name test competition 2'
        assert competition['date'] == '2025-01-01 10:00:00'

        with pytest.raises(NameError):
            find_or_raise('clubs', 'aaaaaaaaa')
            find_or_raise('competition', 'bbbbbbbbbbb')
