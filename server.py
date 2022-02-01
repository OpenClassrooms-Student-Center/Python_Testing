# server.py
# created 27/01/2021 at 10:50 by Antoine 'AatroXiss' BEAUDESSON
# last modified 25/01/2021 at 10:50 by Antoine 'AatroXiss' BEAUDESSON

""" server.py

To do:
    - pep8 corrections
"""

__author__ = "Antoine 'AatroXiss' BEAUDESSON"
__copyright__ = "Copyright 2021, Antoine 'AatroXiss' BEAUDESSON"
__credits__ = ["Antoine 'AatroXiss' BEAUDESSON"]
__license__ = ""
__version__ = "0.2.1"
__maintainer__ = "Antoine 'AatroXiss' BEAUDESSON"
__email__ = "antoine.beaudesson@gmail.com"
__status__ = "Development"

# standard library imports
from datetime import datetime
import json

# third party imports
from flask import (
    Flask,
    render_template,
    request,
    redirect,
    flash,
    url_for
)

# local application imports

# other imports

# constants


def load_clubs():
    with open('clubs.json') as c:
        list_of_clubs = json.load(c)['clubs']
        return list_of_clubs


def load_competitions():
    with open('competitions.json') as comps:
        list_of_competitions = json.load(comps)['competitions']
        return list_of_competitions


app = Flask(__name__)
app.secret_key = 'something_special'

competitions = load_competitions()
clubs = load_clubs()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/showSummary', methods=['POST'])
def show_summary():
    """
    Allow user to login in the site if the email is in the database

    :return: Ok if the email is in the DB, else throw an error
    """

    email = request.form['email']

    try:
        club = [club for club in clubs if club['email'] == email][0]
        return render_template(
            'welcome.html',
            club=club,
            competitions=competitions
        )
    except IndexError:
        if email == "":
            flash("Error: field is empty")
            return render_template('index.html')
        else:
            flash("Error: email is not registered")
            return render_template('index.html')


@app.route('/book/<competition>/<club>')
def book(competition, club):
    found_club = [c for c in clubs if c['name'] == club][0]
    found_competition = [c for c in competitions if c['name'] == competition][0]  # noqa
    if found_club and found_competition:
        return render_template(
            'booking.html',
            club=found_club,
            competition=found_competition
        )
    else:
        flash("Something went wrong-please try again")
        return render_template(
            'welcome.html',
            club=club,
            competitions=competitions
        )


@app.route('/purchasePlaces', methods=['POST'])
def purchase_places():
    competition = [c for c in competitions if c['name'] == request.form['competition']][0]  # noqa
    club = [c for c in clubs if c['name'] == request.form['club']][0]
    places_required = int(request.form['places'])
    places_remaining = int(competition['numberOfPlaces'])
    if places_required > int(club['points']):
        flash('Error: you do not have enough points')
        return render_template(
            'booking.html',
            club=club,
            competition=competition
        )
    elif datetime.now() > datetime.strptime(competition['date'], '%Y-%m-%d %H:%M:%S'):  # noqa
        flash("Error: you can't book a place for past competitions")
        return render_template(
            'booking.html',
            club=club,
            competition=competition
        )
    elif places_required > places_remaining:
        flash('Error: there are not enough places available')
        return render_template(
            'booking.html',
            club=club,
            competition=competition
        )
    elif places_required > 12:
        flash('Error: you cannot book more than 12 places')
        return render_template(
            'booking.html',
            club=club,
            competition=competition
        )
    else:
        competition['numberOfPlaces'] = int(competition['numberOfPlaces'])-places_required  # noqa
        flash('Great-booking complete!')
        club['points'] = int(club['points'])-places_required
        return render_template(
            'welcome.html',
            club=club,
            competitions=competitions
        )


# TODO: Add route for points display


@app.route('/logout')
def logout():
    return redirect(url_for('index'))
