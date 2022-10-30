from Python_Testing import server
from Python_Testing.server import purchasePlaces, clubs
from flask import Flask, render_template, request, flash


class MockRequest13places:
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

class MockRequest12places:
    """
    Mocks Request Object
    """

    def __init__(self):
        self.form = {'places': '12',
                     'competition':'Fall Classic',
                     'club':'Iron Temple'}

    @staticmethod  # defines verbose response in terminal?
    def form_data(self):
        data = {"form": self.form}
        return data

class MockRequestInThePast3places:
    """
    Mocks Request Object
    """

    def __init__(self):
        self.form = {'places': '3',
                     'competition':'Spring Festival',
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
            "date": "2023-10-22 13:30:00",
            "numberOfPlaces": "13"
        }]
    return list_of_competitions

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

def mock_render_template(file_name, club, competitions=1, competition=1):
    return_list = [file_name, club, competitions, competition]
    return return_list

def test_purchase_more_than_12_places_in_one_competition(monkeypatch):

    monkeypatch.setattr(server, 'loadCompetitions', mockloadCompetitions())

    def mock_post(*args, **kwarg):
        return MockRequest13places()

    # monkey patch une saisie de 13 places réservées:
    monkeypatch.setattr(server, 'request', mock_post())

    # flash function needs an active HTTP request,
    # so mocks it with print function for testing purposes:
    monkeypatch.setattr(server, 'flash', str)


    # remplace render_template par fonction mock_render_template
    # qui retourne une liste, pour juste pouvoir vérifier le titre du fichier template retourné
    # vérifie que va bien chercher le fichier 'booking.html' en cas de réservation de trop de places
    monkeypatch.setattr(server, 'render_template', mock_render_template)

    expected_value = ['booking.html']
    result = purchasePlaces()

    assert result[0] == expected_value[0]

def test_purchase_more_than_clubs_remaining_places(monkeypatch):

    monkeypatch.setattr(server, 'loadClubs', mockloadClubs())

    monkeypatch.setattr(server, 'loadCompetitions', mockloadCompetitions())

    def mock_post(*args, **kwarg):
        return MockRequest12places()

    # monkey patch une saisie de 13 places réservées pour l'Iron Temple qui n'a que 4 points:
    monkeypatch.setattr(server, 'request', mock_post())

    # remplace render_template par fonction mock_render_template
    # qui retourne une liste, pour juste pouvoir vérifier le titre du fichier template retourné
    # vérifie que va bien chercher le fichier 'booking.html' en cas de réservation de trop de places
    monkeypatch.setattr(server, 'render_template', mock_render_template)

    monkeypatch.setattr(server, 'flash', str)

    expected_value = ['booking.html']
    result = purchasePlaces()

    assert result[0] == expected_value[0]

def test_purchase_places_for_a_past_competition(monkeypatch):

    monkeypatch.setattr(server, 'loadCompetitions', mockloadCompetitions())

    def mock_post(*args, **kwarg):
        return MockRequestInThePast3places()

    # monkey patch une saisie de 3 places réservées pour la competition Spring Festival
    # qui a eu lieu dans le passé:
    monkeypatch.setattr(server, 'request', mock_post())

    # remplace render_template par fonction mock_render_template
    # qui retourne une liste, pour juste pouvoir vérifier le titre du fichier template retourné
    # vérifie que va bien chercher le fichier 'booking.html' en cas de réservation de trop de places
    monkeypatch.setattr(server, 'render_template', mock_render_template)

    monkeypatch.setattr(server, 'flash', str)

    expected_value = ['booking.html']
    result = purchasePlaces()

    assert result[0] == expected_value[0]

# def purchasePlaces():
    # competition = [c for c in competitions if c['name'] == request.form['competition']][0]
    # club = [c for c in clubs if c['name'] == request.form['club']][0]
    # placesRequired = int(request.form['places'])
    # competition['numberOfPlaces'] = int(competition['numberOfPlaces'])-placesRequired
    # flash('Great-booking complete!')
    # return render_template('welcome.html', club=club, competitions=competitions)