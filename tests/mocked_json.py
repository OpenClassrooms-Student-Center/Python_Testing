import json


class MockedJson():
    """ Class created to mock the database.
        Use generate_a_new_test_file() to create a test_json with the dictionaries underneath.
        Then use monkeypatch_json_functions(), all json functions will use the generated test files
        instead of the regular json files """

    @staticmethod
    def load_mocked_json(file_name):
        """ Used to mock load_json() by returning a false list with one dict (a club or a competition) """

        if 'clubs' in file_name:
            return [{"id": "1",
                     "name": "name_test_club",
                     "email": "test@mail.com",
                     "points": "22"},
                    {
                     "id": "2",
                     "name": "name test club 2",
                     "email": "test2@mail.com",
                     "points": "5"},
                    {
                     "id": "3",
                     "name": "name_test_club_3",
                     "email": "test3@mail.com",
                     "points": "0"}]

        elif 'competitions' in file_name:
            return [{"name": "name_test_competition",
                     "date": "2027-03-27 10:00:00",
                     "numberOfPlaces": "41"},
                    {
                     "name": "name test competition 2",
                     "date": "2025-01-01 10:00:00",
                     "numberOfPlaces": "8",
                     "2": "11",  # 11 places booked by the club 2
                     "1": "2"},
                    {
                     "name": "name_test_competition_3",
                     "date": "2023-05-05 10:00:00",
                     "numberOfPlaces": "14",
                     "1": 12,
                     "2": 4},
                    {
                     "name": "name_test_competition_4",
                     "date": "2020-05-05 10:00:00",
                     "numberOfPlaces": "15",
                     "2": "3",
                     "1": "9"}]
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
