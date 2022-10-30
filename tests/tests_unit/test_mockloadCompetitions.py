from Python_Testing import server

def mockloadCompetitions():
    """
    Mocks data loading from database
    """
    list_of_competitions = [
        {
            "name": "Spring Festival",
            "date": "2020-03-27 10:00:00",
            "numberOfPlaces": "25"
        },
        {
            "name": "Fall Classic",
            "date": "2020-10-22 13:30:00",
            "numberOfPlaces": "13"
        }]
    return list_of_competitions

def test_return_object_competitions():
    server.loadCompetitions = mockloadCompetitions()
    result = server.competitions
    assert result == mockloadCompetitions()
