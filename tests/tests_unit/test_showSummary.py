from Python_Testing import server
from Python_Testing.server import showSummary
from flask import Flask, render_template


class MockResponse:
    """
    Mocks Request Object
    """

    @staticmethod  # defines verbose response in terminal?
    def get_info():
        return {"form": {"email" : "test@email"},}

def test_showSummary(monkeypatch):

    def mockloadClubs():
        """
        Mocks data loading from database
        """
        list_of_clubs = [
            {
                "name": "Simply Lift",
                "email": "john@simplylift.co",
                "points": "13"
            },
        ]

        return list_of_clubs

    monkeypatch.setattr(server, 'loadClubs', mockloadClubs())

    club = mockloadClubs()[0]

    competitions = [
        {
            "name": "Spring Festival",
            "date": "2020-03-27 10:00:00",
            "numberOfPlaces": "25"
        },
        {
            "name": "Fall Classic",
            "date": "2020-10-22 13:30:00",
            "numberOfPlaces": "13"
        }
    ]

    def mock_get(*args, **kwargs):
        return MockResponse()

    monkeypatch.setattr('server.request', mock_get())

    expected_value = render_template('welcome.html',
                                     club=club,
                                     competitions=competitions,)

    assert showSummary() == expected_value

