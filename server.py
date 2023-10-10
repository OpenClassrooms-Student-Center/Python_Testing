import json

from datetime import datetime
from flask import Flask, render_template, request, redirect, flash,url_for, session


class CompetitionNotFoundException(Exception):
    flash_message = 'Competition not found.'


class CompetitionPassedException(Exception):
    flash_message = 'The competition has already passed.'


class CompetitionFullException(Exception):
    flash_message = 'The competition is already full.'


class InvalidPlacesException(Exception):
    flash_message = 'Please enter a valid number for places.'


class MaximumPlacesException(Exception):
    flash_message = 'You can book a maximum of 12 athletes at once.'


class NotEnoughPointsException(Exception):
    flash_message = 'You do not have enough points to make this booking.'


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


@app.route('/showSummary', methods=['GET', 'POST'])
def showSummary():
    if request.method == 'POST':
        try:
            club = [club for club in clubs if club['email'] == request.form['email']][0]
            session['club'] = club
            return render_template('welcome.html', club=club, competitions=competitions)
        except IndexError:
            if request.form['email'] == "":
                flash("Enter your email", 'error')
                return redirect(url_for('index'))
            else:
                flash("Email invalid", 'error')
            return redirect(url_for('index'))
    else:
        club = session.get('club')
        return render_template('welcome.html', club=club, competitions=competitions)


@app.route('/book/<competition>/<club>')
def book(competition, club):
    try:
        foundClub = [c for c in clubs if c['name'] == club][0]
        foundCompetition = [c for c in competitions if c['name'] == competition][0]

        return render_template('booking.html', club=foundClub, competition=foundCompetition)
    except IndexError:
        flash("The competition or club does not exist. Please try again.", 'error')
        return redirect(url_for('showSummary'))


@app.route('/purchasePlaces', methods=['POST'])
def purchasePlaces():
    try:
        competition_name = request.form['competition']
        club_name = request.form['club']
        places_input = request.form['places']

        # Rechercher la compétition et le club dans la liste des compétitions et des clubs
        competition = next((c for c in competitions if c['name'] == competition_name), None)
        club = next((c for c in clubs if c['name'] == club_name), None)

        # Vérifier si la compétition existe
        if competition is None:
            raise CompetitionNotFoundException()

        # Vérifier si la compétition est passée
        competition_date = datetime.strptime(competition['date'], '%Y-%m-%d %H:%M:%S')
        current_date = datetime.now()

        if competition_date < current_date:
            raise CompetitionPassedException()

        # Vérifier si la compétition est complète
        if int(competition['numberOfPlaces']) <= 0:
            raise CompetitionFullException()

        # Vérifier si le champ "places" est vide, n'est pas un nombre ou est un nombre négatif
        if not places_input or not places_input.isdigit() or int(places_input) <= 0:
            raise InvalidPlacesException()

        placesRequired = int(places_input)

        # Vérifier si l'utilisateur a suffisamment de points (maximum 12 athlètes)
        if placesRequired > 12:
            raise MaximumPlacesException()

        # Convertir club['points'] et competition['numberOfPlaces'] en entiers
        club_points = int(club['points']) if club['points'] else 0
        competition_places = int(competition['numberOfPlaces']) if competition['numberOfPlaces'] else 0

        # Vérifier si l'utilisateur a suffisamment de points (1 point par inscription)
        if club_points < placesRequired:
            raise NotEnoughPointsException()

        # Effectuer la réservation
        competition_places -= placesRequired
        club_points -= placesRequired

        # Mettre à jour les valeurs dans les dictionnaires
        competition['numberOfPlaces'] = str(competition_places)
        club['points'] = str(club_points)

        flash('Great-booking complete!')
        return render_template('welcome.html', club=club, competitions=competitions)

    except CompetitionNotFoundException:
        flash(CompetitionNotFoundException.flash_message, 'error')
        return redirect(url_for('index'))

    except CompetitionPassedException:
        flash(CompetitionPassedException.flash_message, 'error')
        return redirect(url_for('book', competition=competition_name, club=club_name))

    except CompetitionFullException:
        flash(CompetitionFullException.flash_message, 'error')
        return redirect(url_for('book', competition=competition_name, club=club_name))

    except InvalidPlacesException:
        flash(InvalidPlacesException.flash_message, 'error')
        return redirect(url_for('book', competition=competition_name, club=club_name))

    except MaximumPlacesException:
        flash(MaximumPlacesException.flash_message, 'error')
        return redirect(url_for('book', competition=competition_name, club=club_name))
    
    except NotEnoughPointsException:
        flash(NotEnoughPointsException.flash_message, 'error')
        return redirect(url_for('book', competition=competition_name, club=club_name))


@app.route('/displayPointsClubs')
def display_points_clubs():
    clubs_list = sorted(clubs, key=lambda club: club['name'])
    return render_template('points_table_clubs.html', clubs=clubs_list)


@app.route('/logout')
def logout():
    return redirect(url_for('index'))
