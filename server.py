import json
from datetime import datetime
from flask import Flask, render_template, request, redirect, flash, url_for


def loadclubs():
    with open('clubs.json') as c:
        listofclubs = json.load(c)['clubs']
        return listofclubs


def loadcompetitions():
    with open('competitions.json') as comps:
        listofcompetitions = json.load(comps)['competitions']
        return listofcompetitions


def initialize_booked_places(comps, clublist):
    places = []
    for comp in comps:
        for club in clublist:
            places.append({'competition': comp['name'], 'booked': [0, club['name']]})

    return places


app = Flask(__name__)
app.secret_key = 'something_special'


competitions = loadcompetitions()
clubs = loadclubs()
booked_places = initialize_booked_places(competitions, clubs)


def update_booked_places(competition, club, bkd_places, placesrequired):
    for item in bkd_places:
        if item['competition'] == competition['name']:
            if item['booked'][1] == club['name'] and item['booked'][0] + placesrequired <= 12:
                item['booked'][0] += placesrequired
                break
            else:
                raise ValueError("Sorry, you can't book more than 12 places in a competition.")
    return bkd_places


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/showSummary', methods=['POST'])
def showsummary():
    try:
        club = [club for club in clubs if club['email'] == request.form['email']][0]
        return render_template('welcome.html', club=club, competitions=competitions)
    except IndexError:
        if request.form['email'] == '':
            flash("Please, enter your email.", 'error')
        else:
            flash("No account matches this email.", 'error')
        return render_template('index.html'), 403


@app.route('/book/<competition>/<club>')
def book(competition, club):
    try:
        foundclub = [c for c in clubs if c['name'] == club][0]
        foundcompetition = [c for c in competitions if c['name'] == competition][0]
    except IndexError:
        flash("Something went wrong. Please try again.", 'error')
        return render_template('welcome.html', club=club, competitions=competitions), 404
    if datetime.strptime(foundcompetition['date'], '%Y-%m-%d %H:%M:%S') < datetime.now():
        flash("This competition is over.", 'error')
        return render_template('welcome.html', club=club, competitions=competitions), 403
    elif foundclub and foundcompetition:
        return render_template('booking.html', club=foundclub, competition=foundcompetition), 200



@app.route('/purchasePlaces', methods=['POST'])
def purchaseplaces():
    competition = [c for c in competitions if c['name'] == request.form['competition']][0]
    club = [c for c in clubs if c['name'] == request.form['club']][0]

    try:
        placesrequired = int(request.form['places'])
        if placesrequired > int(club['points']):
            flash('Sorry, you don\'t have enough points.', 'error')
            return render_template('booking.html', club=club, competition=competition), 403
        elif placesrequired > int(competition['numberOfPlaces']):
            flash('Not enough available places.', 'error')
            return render_template('booking.html', club=club, competition=competition), 403
        elif placesrequired > 12:
            flash('Sorry, you can\'t book more than 12 places in a competition.', 'error')
            return render_template('booking.html', club=club, competition=competition), 403
        else:
            try:
                update_booked_places(competition, club, booked_places, placesrequired)
                competition['numberOfPlaces'] = int(competition['numberOfPlaces']) - placesrequired
                club['points'] = int(club['points']) - placesrequired
                flash('Great-booking complete!', 'succes')
                return render_template('welcome.html', club=club, competitions=competitions), 200
            except ValueError as message:
                flash(str(message))
    except ValueError:
        flash('You must enter an integer.', 'error')
    return render_template('booking.html', club=club, competition=competition), 403


@app.route('/showClubsSummary')
def showclubssummary():
    return render_template('clubs_board.html', clubs=clubs)


@app.route('/logout')
def logout():
    return redirect(url_for('index'))


@app.template_filter('to_date')
def to_date_filter(iso_date):
    return datetime.fromisoformat(iso_date)


@app.template_filter('is_future')
def is_future_filter(date):
    return date > datetime.now()
