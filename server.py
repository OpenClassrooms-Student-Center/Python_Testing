import json
from datetime import datetime
from flask import Flask,render_template,request,redirect,flash,url_for


def loadClubs():
    with open('clubs.json') as c:
         listOfClubs = json.load(c)['clubs']
         return listOfClubs


def loadCompetitions():
    with open('competitions.json') as comps:
        listOfCompetitions = json.load(comps)['competitions']
        for comp in listOfCompetitions:
            if datetime.strptime(comp['date'], "%Y-%m-%d %H:%M:%S") < datetime.now():
                print(comp, 'is outdated')
                comp['finished'] = True
            else:
                comp['finished'] = False
        return listOfCompetitions


app = Flask(__name__)
app.secret_key = 'something_special'

competitions = loadCompetitions()
clubs = loadClubs()

@app.route('/')
def index():
    return render_template('index.html', club_list=clubs)

@app.route('/showSummary',methods=['POST'])
def showSummary():
    try:
        club = [club for club in clubs if club['email'] == request.form['email']][0]
    except IndexError:
        flash("Sorry, that email wasn't found.")
        return redirect(url_for('index'))
    return render_template('welcome.html', club=club, competitions=competitions, club_list=clubs)


@app.route('/book/<competition>/<club>')
def book(competition,club):
    foundClub = [c for c in clubs if c['name'] == club][0]
    foundCompetition = [c for c in competitions if c['name'] == competition][0]
    if foundClub and foundCompetition:
        return render_template('booking.html',club=foundClub,competition=foundCompetition)
    else:
        flash("Something went wrong-please try again")
        return render_template('welcome.html', club=club, competitions=competitions, club_list=clubs)


@app.route('/purchasePlaces',methods=['POST'])
def purchasePlaces():
    competition = [c for c in competitions if c['name'] == request.form['competition']][0]
    club = [c for c in clubs if c['name'] == request.form['club']][0]
    if competition["finished"]:
        return render_template('welcome.html', club=club, competitions=competitions, club_list=clubs), 302
    placesRequired = int(request.form['places'])
    point_price = placesRequired

    print(placesRequired)
    enough_point = placesRequired <= int(club['points'])
    enough_place = 0 < placesRequired <= int(competition['numberOfPlaces']) and placesRequired <= 12
    if not enough_place or not enough_point:
        if not enough_place:
            flash('Not enough place in the competition')
        if not enough_point:
            flash('Not enough point')
    else:
        competition['numberOfPlaces'] = int(competition['numberOfPlaces']) - placesRequired
        club['points'] = str(int(club['points']) - point_price)
        flash('Great-booking complete!')
    return render_template('welcome.html', club=club, competitions=competitions, club_list=clubs)


# TODO: Add route for points display
@app.route('/clubpointboard')
def display_club_points_board():
    return render_template('display-board.html', club_list=clubs)

@app.route('/logout')
def logout():
    return redirect(url_for('index'))