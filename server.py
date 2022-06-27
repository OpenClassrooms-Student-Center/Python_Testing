import json
from flask import Flask,render_template,request,redirect,flash,url_for


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

@app.route('/showSummary',methods=['POST'])
def showSummary():

    for club in clubs:
        if club['email'] == request.form['email']:
            return render_template('welcome.html',club=club,competitions=competitions)    
    
    message = 'Sorry, the email could not be found.'
    return render_template('index.html', loginFormErrorMsg=message)


@app.route('/book/<competition>/<club>')
def book(competition,club):
    foundClub = [c for c in clubs if c['name'] == club][0]
    foundCompetition = [c for c in competitions if c['name'] == competition][0]
    if foundClub and foundCompetition:
        return render_template('booking.html',club=foundClub,competition=foundCompetition)
    else:
        flash("Something went wrong-please try again")
        return render_template('welcome.html', club=club, competitions=competitions)


@app.route('/purchasePlaces',methods=['POST'])
def purchasePlaces():

    # 1. Check if the number of points entered if superior to the current maximum number of points
    # 2. Correctly deduct number from the club ['points'] category

    competition = [c for c in competitions if c['name'] == request.form['competition']][0]
    club = [c for c in clubs if c['name'] == request.form['club']][0]
    
    placesRequired = int(request.form['places'])
    clubPoints = int(club['points'])
    
    if placesRequired <= clubPoints:
        # Update competition "numberOfPlaces" and club "points"
        competition['numberOfPlaces'] = int(competition['numberOfPlaces'])-placesRequired
        club['points'] = int(club['points'])-placesRequired

        flash('Great-booking complete!')
        return render_template('welcome.html', club=club, competitions=competitions)
    else:
        message = "The input number exceed the maximum of places for this club."
        return render_template('booking.html', club=club,competition=competition,bookFormErrorMsg=message)
        

# TODO: Add route for points display


@app.route('/logout')
def logout():
    return redirect(url_for('index'))