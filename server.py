import json
from flask import (
        Flask,
        render_template,
        request,
        redirect,
        flash,
        url_for,
        )


def loadClubs():
    with open('clubs.json') as c:
        listOfClubs = json.load(c)['clubs']
        return listOfClubs


def loadCompetitions():
    with open('competitions.json') as comps:
        listOfCompetitions = json.load(comps)['competitions']
        return listOfCompetitions


app = Flask(__name__)
app.secret_key = 'something_special'

competitions = loadCompetitions()
clubs = loadClubs()
history_of_reservation = []


def get_number_of_place_reserved_for_competition(competition_name, club_name):
    """Return the number of places reserved for a competition."""
    number_of_place_reserved = 0
    for reservation in history_of_reservation:
        if (reservation['competition'] == competition_name and
                reservation['club'] == club_name):
            number_of_place_reserved += reservation['numberOfPlaces']
    return number_of_place_reserved


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/showSummary', methods=['POST'])
def showSummary():
    for club in clubs:
        if club['email'] == request.form['email']:
            return render_template('welcome.html',
                                   club=club,
                                   competitions=competitions)
    return render_template('index.html',
                           error="Sorry, that email wasn't found.")


@app.route('/book/<competition>/<club>')
def book(competition, club):
    foundClub = [c for c in clubs if c['name'] == club][0]
    foundCompetition = [c for c in competitions if c['name'] == competition][0]
    if foundClub and foundCompetition:
        return render_template('booking.html',
                               club=foundClub,
                               competition=foundCompetition)
    else:
        flash("Something went wrong-please try again")
        return render_template('welcome.html',
                               club=club,
                               competitions=competitions)


@app.route('/purchasePlaces', methods=['POST'])
def purchasePlaces():
    for c in competitions:
        if c['name'] == request.form['competition']:
            competition = c
    for c in clubs:
        if c['name'] == request.form['club']:
            club = c

    placesRequired = int(request.form['places'])
    alreadyReserved = get_number_of_place_reserved_for_competition(
            competition['name'], club['name'])

    if placesRequired > int(club['points']):
        flash(f"You don't have enough points to book {placesRequired} places")
        return render_template('welcome.html',
                               club=club,
                               competitions=competitions)
    elif (placesRequired + alreadyReserved) > 12:
        flash("You can only book 12 places per competition")
        return render_template('welcome.html',
                               club=club,
                               competitions=competitions)
    else:
        competition['numberOfPlaces'] = int(
                competition['numberOfPlaces'])-placesRequired
        club['points'] = str(int(club['points'])-placesRequired)
        history_of_reservation.append({
            'competition': competition['name'],
            'club': club['name'],
            'numberOfPlaces': placesRequired,
            })
        flash('Great-booking complete!')
        return render_template('welcome.html',
                               club=club,
                               competitions=competitions)


# TODO: Add route for points display


@app.route('/logout')
def logout():
    return redirect(url_for('index'))
