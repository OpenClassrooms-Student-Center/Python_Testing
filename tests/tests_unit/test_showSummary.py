from Python_Testing import server
from Python_Testing.server import showSummary
from flask import Flask, render_template, request, render_template_string


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
        {
            "name": "Iron Temple",
            "email": "admin@irontemple.com",
            "points": "4"
        },
        {"name": "She Lifts",
         "email": "kate@shelifts.co.uk",
         "points": "12"
         }]

    return list_of_clubs


def test_return_object_clubs():
    server.loadClubs = mockloadClubs()
    result = server.clubs
    assert result == mockloadClubs()


# def mockrequestForm():
# return {"email" : "test@email"}

class MockRequest:
    """
    Mocks Request Object
    """

    def __init__(self):
        self.form = {'email': 'test@email'}

    @staticmethod  # defines verbose response in terminal?
    def form_data(self):
        data = {"form": self.form}
        return data


def test_return_showSummary_if_mail_does_not_exist(monkeypatch):
    monkeypatch.setattr(server, 'loadClubs', mockloadClubs())

    def mock_post(*args, **kwarg):
        return MockRequest()

    # monkey patch une saisie de mauvais e-mail:
    monkeypatch.setattr(server, 'request', mock_post())

    # remplace render_template par fonction string, pour juste pouvoir vérifier le titre du fichier template retourné
    # vérifie que va bien chercher le fichier 'index.html' en cas de mauvaise saisie
    monkeypatch.setattr(server, 'render_template', str)

    # TODO: voir comment mocker render template de flask?
    expected_value = 'index.html'
    result = showSummary()

    assert result == expected_value


