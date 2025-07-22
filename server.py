import os
import json
from flask import Flask, render_template, request, redirect, flash, url_for
from services.services import validate_places_request, is_competition_in_future

app = Flask(__name__)
app.secret_key = 'something_special'

clubs = []
competitions = []

# ------------------ Loaders ------------------

def load_clubs():
    with open('clubs.json') as c:
        return json.load(c)['clubs']

def load_competitions():
    with open('competitions.json') as comps:
        return json.load(comps)['competitions']

def initialize_data():
    if os.getenv("FLASK_ENV") == "testing":
        return
    global clubs, competitions
    clubs[:] = load_clubs()
    competitions[:] = load_competitions()

initialize_data()



@app.route('/')
def index():
    return render_template('index.html')

@app.route('/showSummary', methods=['POST'])
def show_summary():
    club = next((c for c in clubs if c['email'] == request.form['email']), None)
    if club:
        return render_template('welcome.html', club=club, competitions=competitions)
    flash("Club not found.")
    return redirect(url_for('index'))

@app.route('/book/<competition>/<club>')
def book(competition, club):
    found_club = next((c for c in clubs if c['name'] == club), None)
    found_competition = next((c for c in competitions if c['name'] == competition), None)

    if found_club and found_competition:
        if not is_competition_in_future(found_competition):
            flash("Sorry, the competition is already over. Please try another competition.")
            return render_template('welcome.html', club=found_club, competitions=competitions)
        return render_template('booking.html', club=found_club, competition=found_competition)

    flash("Something went wrong – please try again.")
    return render_template('welcome.html', club=found_club or {}, competitions=competitions)

@app.route('/purchasePlaces', methods=['POST'])
def purchase_places():
    competition = next((c for c in competitions if c['name'] == request.form['competition']), None)
    club = next((c for c in clubs if c['name'] == request.form['club']), None)

    if not competition or not club:
        flash("Club or competition not found.")
        return redirect(url_for('index'))

    places_required = int(request.form['places'])

    if not validate_places_request(places_required):
        flash('You cannot book more than 12 tickets!')
        return render_template('booking.html', club=club, competition=competition)

    if int(club['points']) < places_required:
        flash('Not enough points to book these places.')
        return render_template('booking.html', club=club, competition=competition)

    if int(competition['numberOfPlaces']) < places_required:
        flash('Not enough places left in this competition.')
        return render_template('booking.html', club=club, competition=competition)

    competition['numberOfPlaces'] = int(competition['numberOfPlaces']) - places_required
    club['points'] = int(club['points']) - places_required

    flash('Great - booking complete!')
    return render_template('welcome.html', club=club, competitions=competitions)

@app.route('/logout')
def logout():
    return redirect(url_for('index'))
