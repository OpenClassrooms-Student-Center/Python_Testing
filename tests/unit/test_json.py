import server


class MockedJson():

    CLUBS = 'test_clubs'
    COMPETITIONS = 'test_competitions'

    def load_json(self, file_name):

        if file_name == MockedJson.CLUBS:
            return [{"name": "name_test_club",
                     "email": "test@mail.com",
                     "points": "22"}]

        elif file_name == MockedJson.COMPETITIONS:
            return [{"name": "name_test_competition",
                     "date": "2020-03-27 10:00:00",
                     "numberOfPlaces": "41"}]

        else:
            return []

    def generate_a_new_test_file(self, file_name, monkeypatch):
        """ Use the mocked function 'load_json()' and save datas into a real file named '<test_file_name>.json'
            Then deactivate the monkeypatch """
        monkeypatch.setattr('server.load_json', self.load_json)  # >>

        mocked_datas = server.load_json(file_name)
        server.save_json(file_name, mocked_datas)

        monkeypatch.undo()  # <<


class TestJson:

    mocked_json = MockedJson()

    def test_save_clubs(self, monkeypatch):

        monkeypatch.setattr('server.load_json', self.mocked_json.load_json)  # >>

        # Load the mocked list of clubs and add one
        mocked_clubs = server.load_json(MockedJson.CLUBS)
        mocked_clubs.append({"name": "Super_Club", "email": "none", "points": "555"})

        # Save it (inside a test json file) and remove the monkeypatch
        server.save_json(MockedJson.CLUBS, mocked_clubs)
        monkeypatch.undo()  # <<

        # Open the test json file and check if the new club has been saved
        clubs = server.load_json(MockedJson.CLUBS)

        assert clubs[0]['name'] == "name_test_club"
        assert clubs[0]['points'] == "22"
        assert clubs[1]['name'] == "Super_Club"
        assert clubs[1]['points'] == "555"

    def test_save_competitions(self, monkeypatch):

        monkeypatch.setattr('server.load_json', self.mocked_json.load_json)  # >>

        mocked_comp = server.load_json(MockedJson.COMPETITIONS)
        mocked_comp.append({"name": "Super_Competition", "date": "1985-01-01 07:00:00", "numberOfPlaces": "5000"})

        server.save_json(MockedJson.COMPETITIONS, mocked_comp)
        monkeypatch.undo()  # <<

        competitions = server.load_json(MockedJson.COMPETITIONS)

        assert competitions[0]['name'] == "name_test_competition"
        assert competitions[0]['numberOfPlaces'] == "41"
        assert competitions[1]['name'] == "Super_Competition"
        assert competitions[1]['date'] == "1985-01-01 07:00:00"
        assert competitions[1]['numberOfPlaces'] == "5000"

    def test_update_a_club(self, monkeypatch):

        # Open the mocked json file and save it inside test_clubs.json
        self.mocked_json.generate_a_new_test_file(MockedJson.CLUBS, monkeypatch)

        # Take the first (and the only) entry and update it
        club_to_update = server.load_json(MockedJson.CLUBS)[0]
        club_to_update['email'] = 'updated@mail.com'
        club_to_update['points'] = '10000'
        server.update_json(MockedJson.CLUBS, club_to_update)

        # Open the file and check if the update has been executed
        updated_list_of_clubs = server.load_json(MockedJson.CLUBS)

        assert updated_list_of_clubs[0]['name'] == 'name_test_club'
        assert updated_list_of_clubs[0]['email'] == 'updated@mail.com'
        assert updated_list_of_clubs[0]['points'] == '10000'

    def test_update_a_competition(self, monkeypatch):

        self.mocked_json.generate_a_new_test_file(MockedJson.COMPETITIONS, monkeypatch)

        comp_to_update = server.load_json(MockedJson.COMPETITIONS)[0]
        comp_to_update['date'] = '1990-02-02 05:05:05'
        comp_to_update['numberOfPlaces'] = '44'
        server.update_json(MockedJson.COMPETITIONS, comp_to_update)

        updated_list_of_comp = server.load_json(MockedJson.COMPETITIONS)

        assert updated_list_of_comp[0]['name'] == 'name_test_competition'
        assert updated_list_of_comp[0]['date'] == '1990-02-02 05:05:05'
        assert updated_list_of_comp[0]['numberOfPlaces'] == '44'

    def test_add_a_club(self, monkeypatch):

        # Open the mocked json file and save it inside test_clubs.json
        self.mocked_json.generate_a_new_test_file(MockedJson.CLUBS, monkeypatch)

        # Create and add a new club
        new_club = {'name': 'new_club', 'email': 'new@mail.com', 'points': '5'}
        server.update_json(MockedJson.CLUBS, new_club)

        # Open the file and check if the add has been executed
        club = [c for c in server.load_json(MockedJson.CLUBS) if c['name'] == 'new_club'][0]

        assert club['email'] == 'new@mail.com'
        assert club['points'] == '5'

    def test_add_a_competition(self, monkeypatch):

        self.mocked_json.generate_a_new_test_file(MockedJson.COMPETITIONS, monkeypatch)

        new_competition = {'name': 'new_competition', 'date': '1970-06-06 04:04:00', 'numberOfPlaces': '88'}
        server.update_json(MockedJson.COMPETITIONS, new_competition)

        comp = [c for c in server.load_json(MockedJson.COMPETITIONS) if c['name'] == 'new_competition'][0]

        assert comp['date'] == '1970-06-06 04:04:00'
        assert comp['numberOfPlaces'] == '88'
