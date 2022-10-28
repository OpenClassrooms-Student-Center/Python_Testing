from Python_Testing import server
from Python_Testing.server import showSummary, loadClubs, clubs
from flask import Flask, render_template


def mockloadClubs():
    """
    Mocks data loading from database
    """
    list_of_clubs = [
    {
        "name":"Simply Lift",
        "email":"john@simplylift.co",
        "points":"13"
    },
    {
        "name":"Iron Temple",
        "email": "admin@irontemple.com",
        "points":"4"
    },
    {   "name":"She Lifts",
        "email": "kate@shelifts.co.uk",
        "points":"12"
    }
    ]

    return list_of_clubs

def test_return_object_clubs():
    server.loadClubs = mockloadClubs()
    result = server.clubs
    assert result == mockloadClubs()

class MockResponse:
    """
    Mocks Request Object
    """
    @staticmethod  # defines verbose response in terminal?
    def get_info():
        return {"form": {"email" : "test@email"},}

def test_return_showSummary_if_mail_does_not_exist(monkeypatch):

    monkeypatch.setattr(server, 'loadClubs', mockloadClubs())

    def mock_get(*args, **kwargs):
        return MockResponse()

    monkeypatch.setattr('Python_Testing.server.request', mock_get())

    # TODO: voir comment mocker render template de flask?
    expected_value = render_template('index.html')

    result = showSummary

    assert result == expected_value

