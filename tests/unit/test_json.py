import json
import server


class MockedJson():

    @staticmethod
    def load_mocked_json(file_name):
        """ Used to mock load_json() by returning a false list with one dict (a club or a competition) """

        if 'clubs' in file_name:
            return [{"name": "name_test_club",
                     "email": "test@mail.com",
                     "points": "22"}]

        elif 'competitions' in file_name:
            return [{"name": "name_test_competition",
                     "date": "2020-03-27 10:00:00",
                     "numberOfPlaces": "41"}]
        else:
            return []

    @staticmethod
    def load_test_json(file_name):
        """ Copy/past of server.load_json to modify 'file_name' by 'test_file_name' """

        file_name = f"test_{file_name}"
        with open(f'database/{file_name}.json') as file:
            return json.load(file)[file_name]

    @staticmethod
    def save_test_json(file_name, data):
        """ Copy/past of server.save_json to modify 'file_name' by 'test_file_name' """

        file_name = f"test_{file_name}"
        with open(f'database/{file_name}.json', 'w') as file:
            json.dump({file_name: data}, file)

    @staticmethod
    def generate_a_new_test_file(file_name):
        """ Use 'load_mocked_json()' and save data
            into a real file named '<test_file_name>.json' """

        mocked_data = MockedJson.load_mocked_json(file_name)
        MockedJson.save_test_json(file_name, mocked_data)

    @staticmethod
    def monkeypatch_json_functions(monkeypatch):
        monkeypatch.setattr('server.load_json', MockedJson.load_test_json)
        monkeypatch.setattr('server.save_json', MockedJson.save_test_json)


class TestJson:

    def test_save_clubs(self, monkeypatch):

        # Create a new clubs test file, then monkeypatch the json functions
        MockedJson.generate_a_new_test_file('clubs')
        MockedJson.monkeypatch_json_functions(monkeypatch)

        # Load the mocked list of clubs and add a new one
        mocked_clubs = server.load_json('clubs')
        mocked_clubs.append({"name": "Super_Club", "email": "none", "points": "555"})

        # Save it (inside a test json file)
        server.save_json('clubs', mocked_clubs)

        # Open the test json file and check if the new club has been saved
        clubs = server.load_json('clubs')

        assert clubs[0]['name'] == "name_test_club"
        assert clubs[0]['points'] == "22"
        assert clubs[1]['name'] == "Super_Club"
        assert clubs[1]['points'] == "555"

    def test_save_competitions(self, monkeypatch):

        MockedJson.generate_a_new_test_file('competitions')
        MockedJson.monkeypatch_json_functions(monkeypatch)

        mocked_comp = server.load_json('competitions')
        mocked_comp.append({"name": "Super_Competition", "date": "1985-01-01 07:00:00", "numberOfPlaces": "5000"})

        server.save_json('competitions', mocked_comp)
        competitions = server.load_json('competitions')

        assert competitions[0]['name'] == "name_test_competition"
        assert competitions[0]['numberOfPlaces'] == "41"
        assert competitions[1]['name'] == "Super_Competition"
        assert competitions[1]['date'] == "1985-01-01 07:00:00"
        assert competitions[1]['numberOfPlaces'] == "5000"

    def test_update_a_club(self, monkeypatch):

        # Generate a test file with the mocked club, then monkeypatch the json functions
        MockedJson.generate_a_new_test_file('clubs')
        MockedJson.monkeypatch_json_functions(monkeypatch)

        # Take the first (and the only) entry and update it
        club_to_update = server.load_json('clubs')[0]
        club_to_update['email'] = 'updated@mail.com'
        club_to_update['points'] = '10000'
        server.update_json('clubs', club_to_update)

        # Open the file and check if the update has been executed
        updated_list_of_clubs = server.load_json('clubs')

        assert updated_list_of_clubs[0]['name'] == 'name_test_club'
        assert updated_list_of_clubs[0]['email'] == 'updated@mail.com'
        assert updated_list_of_clubs[0]['points'] == '10000'

    def test_update_a_competition(self, monkeypatch):

        MockedJson.generate_a_new_test_file('competitions')
        MockedJson.monkeypatch_json_functions(monkeypatch)

        comp_to_update = server.load_json('competitions')[0]
        comp_to_update['date'] = '1990-02-02 05:05:05'
        comp_to_update['numberOfPlaces'] = '44'
        server.update_json('competitions', comp_to_update)

        updated_list_of_comp = server.load_json('competitions')

        assert updated_list_of_comp[0]['name'] == 'name_test_competition'
        assert updated_list_of_comp[0]['date'] == '1990-02-02 05:05:05'
        assert updated_list_of_comp[0]['numberOfPlaces'] == '44'

    def test_add_a_club(self, monkeypatch):

        # Generate a test file with the mocked club, then monkeypatch the json functions
        MockedJson.generate_a_new_test_file('clubs')
        MockedJson.monkeypatch_json_functions(monkeypatch)

        # Create and add a new club
        new_club = {'name': 'new_club', 'email': 'new@mail.com', 'points': '5'}
        server.update_json('clubs', new_club)

        # Open the file and check if the add has been executed
        club = [c for c in server.load_json('clubs') if c['name'] == 'new_club'][0]

        assert club['email'] == 'new@mail.com'
        assert club['points'] == '5'

    def test_add_a_competition(self, monkeypatch):

        MockedJson.generate_a_new_test_file('competitions')
        MockedJson.monkeypatch_json_functions(monkeypatch)

        new_competition = {'name': 'new_competition', 'date': '1970-06-06 04:04:00', 'numberOfPlaces': '88'}
        server.update_json('competitions', new_competition)

        comp = [c for c in server.load_json('competitions') if c['name'] == 'new_competition'][0]

        assert comp['date'] == '1970-06-06 04:04:00'
        assert comp['numberOfPlaces'] == '88'
