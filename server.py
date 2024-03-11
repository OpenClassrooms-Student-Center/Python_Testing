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

def total_reserved_places(club_name, competition_name):
    club = next((c for c in clubs if c['name'] == club_name), None)
    if club:
        return sum(int(booking['places']) for booking in club['booking'] if booking['competition'] == competition_name)
    else:
        return 0

app = Flask(__name__)
app.secret_key = 'something_special'

competitions = loadCompetitions()
clubs = loadClubs()

@app.route('/')
def index():
    return render_template('index.html', clubs=clubs)

@app.route('/showSummary',methods=['POST'])
def showSummary():
    try:
        club = [club for club in clubs if club['email'] == request.form['email']][0]
        return render_template('welcome.html', club=club, competitions=competitions)
    except Exception:
        return render_template('index.html', clubs=clubs)

@app.route('/book/<competition>/<club>')
def book(competition,club):
    try:
        foundClub = [c for c in clubs if c['name'] == club][0]
        foundCompetition = [c for c in competitions if c['name'] == competition][0]
        dateCompetition = datetime.strptime(foundCompetition['date'], "%Y-%m-%d %H:%M:%S")
        if dateCompetition >= datetime.now():
            if foundClub and foundCompetition:
                return render_template('booking.html',club=foundClub,competition=foundCompetition)
            else:
                flash("Something went wrong-please try again")
                return render_template('welcome.html', club=foundClub, competitions=competitions)
        else:
            flash('Competition is over. You can not buy places')
            return render_template('welcome.html', club=foundClub, competitions=competitions)
    except Exception:
        flash("Something went wrong-please try again")
        return render_template('welcome.html', club=club, competitions=competitions)

@app.route('/purchasePlaces',methods=['POST'])
def purchasePlaces():
    try:
        competition_name = request.form['competition']
        club_name = request.form['club']
        competition = [c for c in competitions if c['name'] == competition_name][0]
        club = [c for c in clubs if c['name'] == club_name][0]
        placesRequired = int(request.form['places'])
        total_places_reserved = total_reserved_places(club_name, competition_name)
        max_places = 12
        if total_places_reserved + placesRequired <= max_places:
            if placesRequired <= int(club['points']):
                competition['numberOfPlaces'] = int(competition['numberOfPlaces'])-placesRequired
                club['points'] = int(club['points'])-placesRequired
                booking = {'competition': competition_name, 'places': placesRequired}
                club['booking'].append(booking)
                flash('Great-booking complete!')
                return render_template('welcome.html', club=club, competitions=competitions)
            else:
                flash('You do not have enougth points')
                return render_template('welcome.html', club=club, competitions=competitions)
        else:
            flash('You can not buy more than 12 places')
            return render_template('welcome.html', club=club, competitions=competitions)
    except Exception:
        flash("Something went wrong-please try again")
        return render_template('welcome.html', club=club, competitions=competitions)

# Issue#7 route for points display
@app.route('/displaypoints')
def display_points():
    points_table = [{'name': club['name'], 'points': club['points']} for club in clubs]
    return render_template('displaypoints.html', points_table=points_table)

@app.route('/logout')
def logout():
    return redirect(url_for('index'))
