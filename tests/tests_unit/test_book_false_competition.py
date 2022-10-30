from Python_Testing import server
from Python_Testing.server import purchasePlaces, clubs
from flask import Flask, render_template, request, flash


class MockRequest:
    """
    Mocks Request Object
    """

    def __init__(self):
        self.form = {'places': '13',
                     'competition':'Fall Classic',
                     'club':'Iron Temple'}

    @staticmethod  # defines verbose response in terminal?
    def form_data(self):
        data = {"form": self.form}
        return data

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
