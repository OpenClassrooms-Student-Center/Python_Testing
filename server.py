import json
from config import DEBUG
from flask_bootstrap import Bootstrap
from flask import Flask, render_template, request, redirect, flash, url_for


def loadClubs():
    with open('clubs.json') as c:
        listOfClubs = json.load(c)['clubs']
        return listOfClubs


def loadCompetitions():
    with open('competitions.json') as comps:
        listOfCompetitions = json.load(comps)['competitions']
        return listOfCompetitions


def create_app():
    app = Flask(__name__)
    app.secret_key = 'something_special'
    Bootstrap(app)

    if DEBUG:
        app.debug = True

    return app


competitions = loadCompetitions()
clubs = loadClubs()

app = create_app()

# Define the route for the main page


@app.route('/')
def index():
    return render_template('index.html')

# Define the route for handling form submissions


@app.route('/showSummary', methods=['POST'])
def showSummary():
    # Récupérer l'adresse e-mail depuis le formulaire, en supprimant les espaces inutiles
    email = request.form.get('email', '').strip()

    # Check if the email is not provided
    if not email:
        flash('Please enter an email address.')
        return redirect(url_for('index'))

    # Try to find a club with the provided email
    club = [club for club in clubs if club['email'] == email]

    # If no club is found, display an error message
    if not club:
        flash('Sorry, that email wasn\'t found.')
        return redirect(url_for('index'))

    # Display the summary to the user when a correct email is entered
    return render_template('welcome.html', club=club[0], competitions=competitions)


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
    placesRequired = int(request.form['places'])
    competition['numberOfPlaces'] = int(
        competition['numberOfPlaces'])-placesRequired
    flash('Great-booking complete!')
    return render_template('welcome.html', club=club, competitions=competitions)


# TODO: Add route for points display


@app.route('/logout')
def logout():
    return redirect(url_for('index'))
