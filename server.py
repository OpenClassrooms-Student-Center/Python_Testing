import json
from flask import Flask,render_template,request,redirect,flash,url_for


def loadClubs(path='clubs.json'):
    with open(path) as c:
         listOfClubs = json.load(c)['clubs']
         return listOfClubs


def loadCompetitions(path='competitions.json'):
    with open(path) as comps:
         listOfCompetitions = json.load(comps)['competitions']
         return listOfCompetitions


app = Flask(__name__)
app.secret_key = 'something_special'

competitions = loadCompetitions()
clubs = loadClubs()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/showSummary',methods=['POST'])
def showSummary():
    club = [club for club in clubs if club['email'] == request.form['email']]
    if len(club):
        return render_template('welcome.html',club=club[0] ,competitions=competitions), 200
      
    flash("No user found")
    return render_template('index.html'), 401


@app.route('/book/<competition>/<club>')
def book(competition,club):
    foundClub = [c for c in clubs if c['name'] == club][0]
    foundCompetition = [c for c in competitions if c['name'] == competition][0]
    if foundClub and foundCompetition:
        return render_template('booking.html',club=foundClub,competition=foundCompetition)
    else:
        flash("Something went wrong-please try again")
        return render_template('welcome.html', club=club, competitions=competitions)


def can_club_buy_places(club, places_required):
    club_wallet = int(club.get('points'))
    if places_required <= club_wallet:
        return True
        
@app.route('/purchasePlaces',methods=['POST'])
def purchasePlaces():
    competition = [c for c in competitions if c['name'] == request.form['competition']][0]
    club = [c for c in clubs if c['name'] == request.form['club']][0]
    placesRequired = int(request.form['places'])
    code = 200
    if can_club_buy_places(club, placesRequired):
        competition['numberOfPlaces'] = int(competition['numberOfPlaces'])-placesRequired
        flash('Great-booking complete!')
    else:
        flash('You do not have enough of points !')
        code = 403
        
    return render_template('welcome.html', club=club, competitions=competitions), code


# TODO: Add route for points display


@app.route('/logout')
def logout():
    return redirect(url_for('index'))