import json
from flask import Flask, render_template, request, redirect, flash, url_for
from services.services import validate_places_request

app = Flask(__name__)
app.secret_key = 'something_special'

clubs = []
competitions = []

def load_clubs():
    with open('clubs.json') as c:
        return json.load(c)['clubs']

def load_competitions():
    with open('competitions.json') as comps:
        return json.load(comps)['competitions']

@app.before_first_request
def initialize_data():
    global clubs, competitions
    clubs = load_clubs()
    competitions = load_competitions()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/showSummary', methods=['POST'])
def show_summary():
    club = [club for club in clubs if club['email'] == request.form['email']][0]
    return render_template('welcome.html', club=club, competitions=competitions)

@app.route('/book/<competition>/<club>')
def book(competition, club):
    found_club = next((c for c in clubs if c['name'] == club), None)
    found_competition = next((c for c in competitions if c['name'] == competition), None)
    if found_club and found_competition:
        return render_template('booking.html', club=found_club, competition=found_competition)
    else:
        flash("Something went wrong – please try again.")
        return render_template('welcome.html', club=club, competitions=competitions)

@app.route('/purchasePlaces', methods=['POST'])
def purchase_places():
    competition = next((c for c in competitions if c['name'] == request.form['competition']), None)
    club = next((c for c in clubs if c['name'] == request.form['club']), None)
    places_required = int(request.form['places'])

    if not validate_places_request(places_required):
        flash('You cannot book more than 12 tickets !')
        return render_template('booking.html', club=club, competition=competition)

    competition['numberOfPlaces'] = int(competition['numberOfPlaces']) - places_required
    flash('Great-booking complete!')
    return render_template('welcome.html', club=club, competitions=competitions)

@app.route('/logout')
def logout():
    return redirect(url_for('index'))
