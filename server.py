import json
from flask import Flask, render_template, request, redirect, flash, url_for
import os
from flask_testing import TestCase

app = Flask(__name__)
app.secret_key = 'something_special'

is_testing = 'testing'

# Si l'application est en mode test, utilisez les données prédéfinies dans le code
if is_testing == 'testing':
    clubs = [
        {
            "name": "Simply Lift",
            "email": "john@simplylift.co",
            "points": "13"
        },
        {
            "name": "Iron Temple",
            "email": "admin@irontemple.com",
            "points": "4"
        },
        {
            "name": "She Lifts",
            "email": "kate@shelifts.co.uk",
            "points": "12"
        }
    ]

    competitions = [
        {
            "name": "Spring Festival",
            "date": "2020-03-27 10:00:00",
            "numberOfPlaces": "25"
        },
        {
            "name": "Fall Classic",
            "date": "2020-10-22 13:30:00",
            "numberOfPlaces": "13"
        }
    ]
# Sinon, chargez les données à partir des fichiers JSON comme d'habitude
else:
    def loadClubs():
        with open('clubs.json') as c:
            listOfClubs = json.load(c)['clubs']
            return listOfClubs


    def loadCompetitions():
        with open('competitions.json') as comps:
            listOfCompetitions = json.load(comps)['competitions']
            return listOfCompetitions

    # Load data from JSON
    clubs = loadClubs()
    competitions = loadCompetitions()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/showSummary', methods=['POST'])
def showSummary():
    club = [club for club in clubs if club['email'] == request.form['email']][0]
    return render_template('welcome.html', club=club, competitions=competitions)

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
    global clubs, competitions

    club_name = request.form['club']
    competition_name = request.form['competition']
    places_required = int(request.form['places'])

    club = next((c for c in clubs if c['name'] == club_name), None)
    competition = next((c for c in competitions if c['name'] == competition_name), None)

    if club and competition:
        # Check if the user has already bought 12 places for this club
        user_club_bookings = [b for b in club.get('bookings', []) if b.get('competition') == competition_name]
        user_total_places = sum(b.get('places', 0) for b in user_club_bookings)
        print('ici', user_total_places + places_required)
        if user_total_places + places_required <= 12:
            if int(competition['numberOfPlaces']) >= places_required:
                competition['numberOfPlaces'] = str(int(competition['numberOfPlaces']) - places_required)
                club_points = int(club['points'])
                if club_points >= places_required:
                    club_points -= places_required
                    club['points'] = str(club_points)
                    # Save booking
                    club.setdefault('bookings', []).append({
                        'competition': competition_name,
                        'places': places_required
                    })
                    # Save in JSON
                    with open('clubs.json', 'w') as clubs_file:
                        json.dump({'clubs': clubs}, clubs_file, indent=4)
                    with open('competitions.json', 'w') as competitions_file:
                        json.dump({'competitions': competitions}, competitions_file, indent=4)

                    flash('Great-booking complete!')
                else:
                    flash('Not enough points to make the booking.')
            else:
                flash('Not enough places available in the competition.')
        else:
            flash('You can only purchase up to 12 places for the same club in one competition.')
    else:
        flash('Club or competition not found.')

    return render_template('welcome.html', club=club, competitions=competitions)

# Route to display points
@app.route('/points', methods=['GET'])
def points():
    club_points = [{'name': club['name'], 'points': int(club['points'])} for club in clubs]
    sorted_clubs = sorted(club_points, key=lambda x: x['points'], reverse=True)
    return render_template('points.html', clubs=sorted_clubs)

# Logout route
@app.route('/logout')
def logout():
    return redirect(url_for('index'))
