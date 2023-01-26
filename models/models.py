import json
import datetime


def load_clubs():
    with open('clubs.json') as c:
        listOfClubs = json.load(c)['clubs']
        return listOfClubs


def add_date_information_on_competition(competitions):
    """Add date information on competition."""
    now = datetime.datetime.now()
    for comp in competitions:
        date_as_datetime = datetime.datetime.strptime(
                comp['date'], '%Y-%m-%d %H:%M:%S')
        if now > date_as_datetime:
            comp['passed'] = True
        else:
            comp['passed'] = False
    return competitions


def load_competitions():
    with open('competitions.json') as comps:
        listOfCompetitions = json.load(comps)['competitions']
        return add_date_information_on_competition(listOfCompetitions)
