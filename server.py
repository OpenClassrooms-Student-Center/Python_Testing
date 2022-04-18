import json
from flask import Flask, render_template, request, redirect, flash, url_for
from datetime import datetime


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


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/showSummary', methods=['POST'])
def showSummary():
    try:
        club = [club for club in clubs if club['email']
                == request.form['email']][0]
        return render_template('welcome.html', clubs=clubs, club=club, competitions=competitions)

    except IndexError:
        flash('Email not found')
        return redirect(url_for('index'))


@app.route('/book/<competition>/<club>')
def book(competition, club):
    foundClub = [c for c in clubs if c['name'] == club][0]
    foundCompetition = [c for c in competitions if c['name'] == competition][0]
    if foundClub and foundCompetition:
        return render_template('booking.html', club=foundClub, competition=foundCompetition)
    else:
        flash("Something went wrong-please try again")
        return render_template('welcome.html', club=club, competitions=competitions)


@app.route('/purchasePlaces', methods=['POST'])
def purchasePlaces():
    competition = [c for c in competitions if c['name']
                   == request.form['competition']][0]
    club = [c for c in clubs if c['name'] == request.form['club']][0]
    today = datetime.now()
    today = today.strftime('%Y-%m-%d %H:%M:%S')
    placesRequired = int(request.form['places'])
    price = placesRequired * 3
    if today < competition['date']:
        if (int(club['points']) >= price):
            if placesRequired <= 12:
                competition['numberOfPlaces'] = int(
                    competition['numberOfPlaces'])-placesRequired
                club['points'] = int(club["points"]) - price
                flash('Great, booking complete!')
            else:
                flash('Sorry, you can only book up to 12 places.')
        else:
            flash('Sorry, you do not have enough points.')
    else:
        flash('Sorry, the competition has already started.')
    return render_template('welcome.html', clubs=clubs, club=club, competitions=competitions)


@app.route('/clubs')
def clubsPointsPage():
    return render_template('clubs.html', clubs=clubs)


@app.route('/logout')
def logout():
    return redirect(url_for('index'))
