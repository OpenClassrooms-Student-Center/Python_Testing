import json
from flask import Flask, render_template, request, redirect, flash, url_for
from datetime import datetime


def loadClubs(clubs_json):
    with open(clubs_json) as c:
        listOfClubs = json.load(c)['clubs']
        return listOfClubs


def loadCompetitions(competitions_json):
    with open(competitions_json) as comps:
        listOfCompetitions = json.load(comps)['competitions']
        return listOfCompetitions


def competition(competitions_json):
    comps = loadCompetitions(competitions_json)
    now = datetime.now()
    competitions = list()
    for comp in comps:
        date_comp = datetime.strptime(comp["date"], '%Y-%m-%d %H:%M:%S')
        if now < date_comp:
            competitions.append(comp)
    return competitions


def create_app(config={}):
    app = Flask(__name__)
    app.config.update(config)
    app.secret_key = 'something_special'
    clubs_json = 'clubs.json'
    competitions_json = 'competitions.json'
    if app.config["TESTING"] == True:
        clubs_json = 'tests/test_data_clubs.json'
        competitions_json = 'tests/test_data_comp.json'
    competitions = competition(competitions_json)
    clubs = loadClubs(clubs_json)


    @app.route('/')
    def index():
        return render_template('index.html')

    @app.route('/showSummary',methods=['POST'])
    def showSummary():
        try:
            club = [club for club in clubs if club['email'] == request.form['email']][0]
            return render_template('welcome.html',club=club,clubs=clubs, competitions=competitions)
        except IndexError:
            flash("Your address mail is not valid !")
            return render_template('index.html')

    @app.route('/book/<competition>/<club>')
    def book(competition, club):
        try:
            foundClub = [c for c in clubs if c['name'] == club][0]
            foundCompetition = [c for c in competitions if c['name'] == competition][0]
            return render_template('booking.html', club=foundClub,
                                competition=foundCompetition)
        except IndexError:
            flash("Something went wrong-please try again")
            return render_template('welcome.html', club=club,clubs=clubs, competition=competition)

    @app.route('/purchasePlaces', methods=['POST'])
    def purchasePlaces():
        competition = [c for c in competitions if c['name']
                       == request.form['competition']][0]
        club = [c for c in clubs if c['name'] == request.form['club']][0]
        placesRequired = int(request.form['places'])
        if placesRequired > 12:
            flash("you cannot book more than 12 places")
            return render_template('welcome.html', club=club,
                                   clubs=clubs, competitions=competitions)
        elif (placesRequired * 3) > int(club['points']):
            flash("you dont have enough points !")
            return render_template('welcome.html', club=club,
                                   clubs=clubs, competitions=competitions)
        elif placesRequired > int(competition['numberOfPlaces']):
            flash("not enought places !")
            return render_template('welcome.html', club=club,
                                   clubs=clubs, competitions=competitions)
        else:
            competition['numberOfPlaces'] = int(competition['numberOfPlaces'])-placesRequired
            club['points'] = int(club['points']) - (placesRequired * 3)
            flash('Great-booking complete!')
            return render_template('welcome.html', club=club, clubs=clubs,
                                   competitions=competitions)

    @app.route('/clubs')
    def clubs_page():
        return render_template('clubs.html',clubs=clubs)

    @app.route('/logout')
    def logout():
        return redirect(url_for('index'))

    return app