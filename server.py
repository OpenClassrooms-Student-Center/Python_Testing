import json
from flask import Flask,render_template,request,redirect,flash,url_for
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

def competition():
    comps = loadCompetitions()
    now = datetime.now() # current date and time
    competitions = list()
    for comp in comps:
        date_time_comp = datetime.strptime(comp["date"], '%Y-%m-%d %H:%M:%S')
        if now < date_time_comp:
            competitions.append(comp)
    return competitions

competitions = competition()
clubs = loadClubs()

@app.route('/')
def index():
    return render_template('index.html')

<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
=======



>>>>>>> bug#4
=======

>>>>>>> bug#5
@app.route('/showSummary',methods=['POST'])
def showSummary():
    try:
        club = [club for club in clubs if club['email'] == request.form['email']][0]
<<<<<<< HEAD
        return render_template('welcome.html',club=club,competitions=competitions)
=======
        return render_template('welcome.html',club=club,clubs=clubs, competitions=competitions)
>>>>>>> bug#5
    except IndexError:
        return render_template('index.html')


@app.route('/book/<competition>/<club>')
def book(competition,club):
    foundClub = [c for c in clubs if c['name'] == club][0]
    points = foundClub['points']
    foundCompetition = [c for c in competitions if c['name'] == competition][0]
    if foundClub and foundCompetition:
        return render_template('booking.html',club=foundClub,clubs=clubs,competition=foundCompetition)
    else:
        flash("Something went wrong-please try again")
        return render_template('welcome.html', club=club,clubs=clubs, competitions=competitions)


@app.route('/purchasePlaces',methods=['POST'])
def purchasePlaces():
    competition = [c for c in competitions if c['name'] == request.form['competition']][0]
    club = [c for c in clubs if c['name'] == request.form['club']][0]
    placesRequired = int(request.form['places'])
    if placesRequired > 12:
        flash("you cannot book more than 12 places")
        return render_template('welcome.html', club=club,clubs=clubs, competitions=competitions)
    if placesRequired > int(club['points']):
        flash("you don't have enough points !")
        return render_template('welcome.html', club=club,clubs=clubs, competitions=competitions)
    else:
        competition['numberOfPlaces'] = int(competition['numberOfPlaces'])-placesRequired
        club['points'] = int(club['points']) - placesRequired
        flash('Great-booking complete!')
        return render_template('welcome.html', club=club,clubs=clubs, competitions=competitions)


# TODO: Add route for points display


@app.route('/logout')
def logout():
    return redirect(url_for('index'))
