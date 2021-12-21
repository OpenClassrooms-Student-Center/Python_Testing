import datetime
import json
import shutil

from os import environ
from flask import Flask, render_template, request, redirect, flash, url_for, session

########################## UTILITIES #################################
# Global variables
MAX_BOOKED_PLACES = 12
DB_CLUBS = 'clubs.json'
DB_COMP = 'competitions.json'

# General utility functions
def load_config(mode=environ.get('MODE')):
    try:
        global DB_CLUBS
        global DB_COMP
        if mode == 'DEV':
            DB_CLUBS = environ.get('DB_CLUBS', 'clubs.json')
            DB_COMP = environ.get('DB_COMP', 'competitions.json')

        elif mode == 'TESTING':
            shutil.copyfile('clubs.json', 'test_clubs.json')
            shutil.copyfile('competitions.json', 'test_competitions.json')
            DB_CLUBS = environ.get('DB_CLUBS', 'test_clubs.json')
            DB_COMP = environ.get('DB_COMP', 'test_competitions.json')

        else:
            print('Could not find .env file.')

    except ImportError as e:
        print(e)

def already_booked(club, competition):
    """Check if the selected club already booked places in the competition by
    checking the length of its 'competitions' key in the db. If it's above 0,
    check if the competition is in the list and return the number of places. Else, return 0."""
    if len(club["competitions"]) > 0:
        booked_list = [competition['name'] for competition in club['competitions']]
        if competition["name"] in booked_list:
            index = booked_list.index(competition["name"])
            comp = club["competitions"][index]

            return int(comp["places"])

    return 0

def return_smallest(club, competition):
    club_points = int(club["points"])
    available_places = int(competition["numberOfPlaces"])

    return min([club_points, available_places, MAX_BOOKED_PLACES])


# Json db utility functions
def load_clubs():
    with open(DB_CLUBS) as c:
         list_of_clubs = json.load(c)['clubs']
         return list_of_clubs

def load_competitions():
    with open(DB_COMP) as comps:
         list_of_competitions = json.load(comps)['competitions']
         return list_of_competitions

def update_clubs(content):
    open(DB_CLUBS,'w').write(content)

def update_competitions(content):
    open(DB_COMP,'w').write(content)

########################## FLASK SPECIFICS #################################
# Global variables
load_config()
competitions = load_competitions()
clubs = load_clubs()
app = Flask(__name__)
app.secret_key = environ.get('SECRET_KEY')


# Routes
@app.route('/')
def index():
    """Shows the form whose data will inform show_summary()"""
    return render_template('index.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

@app.route('/showSummary', methods=['POST'])
def show_summary():
    """Check whether the entered email exists.
    If so, store the user's email in a new cession (barring user ids)
    and show the welcome page, which lists all competitions.
    If not, redirect the user to the index page.
    """
    if request.method == "POST":
        email = request.form["email"]
        error = None
        try:
            user = [club for club in clubs if club['email'] == request.form['email']][0]
        except:
            error = "Identifiants incorrects ou inexistants."

        if error is None:
            session.clear()
            session["user_id"] = user["email"]
            club = [club for club in clubs if club['email'] == request.form['email']][0]
            past_competitions = [comp for comp in competitions
                if datetime.datetime.fromisoformat(comp['date']) < datetime.datetime.now()]

            return render_template('welcome.html', club=club, competitions=competitions,
                                    past_competitions=past_competitions)

        flash(error)
        return redirect(url_for('index'))

@app.route('/book/<competition>/<club>')
def book(competition, club):
    """Show the form to book places for a competition.
    Check that conditions for booking are met, setting maximum available places
    per competition and such."""
    found_club = [c for c in clubs if c['name'] == club][0]
    found_competition = [c for c in competitions if c['name'] == competition][0]
    max_selector = MAX_BOOKED_PLACES
    available_points = int(found_club['points'])
    places_booked = already_booked(found_club, found_competition)

    try:
        if found_club and found_competition and session["user_id"] == found_club["email"]:
            # Check that the url is valid and that the right club is booking
            if datetime.datetime.fromisoformat(found_competition['date']) > datetime.datetime.now():
                # Check that the competition has not occured yet.
                if places_booked == MAX_BOOKED_PLACES:
                    #Check that the club has not booked more than its allowed maximum.
                    flash(f"You have already booked {MAX_BOOKED_PLACES} places!")
                    return render_template('welcome.html', club=club, competitions=competitions)

                elif places_booked > 0:
                    # If places have already been booked, substract them from the MAX limit for that club.
                    max_selector = MAX_BOOKED_PLACES - places_booked

                if available_points < max_selector or int(found_competition['numberOfPlaces']) < MAX_BOOKED_PLACES:
                    # Determine the max value for the number of places widget on the jinja template.
                    max_selector = return_smallest(found_club, found_competition)

                return render_template('booking.html',club=found_club, competition=found_competition, max_selector=max_selector)

            else:
                flash("You cannot book places for a past event.")
                return render_template('welcome.html', club=club, competitions=competitions)

        else:
            flash("Something went wrong - please try again")
            return redirect(url_for('index'))

    except:
        flash("Something went wrong - please try again")
        return redirect(url_for('index'))


@app.route('/purchasePlaces', methods=['POST'])
def purchase_places():
    """
    Checks that the user is logged in, that they can stil book the same number
    of place (things can change between the book page loading and their reservation).
    """
    global competitions
    competition = [c for c in competitions if c['name'] == request.form['competition']][0]
    club = [c for c in clubs if c['name'] == request.form['club']][0]
    places_required = int(request.form['places'])


    try:
        if session["user_id"] == club["email"]:
            double_check_comp = load_competitions()
            double_check_club = load_clubs()
            competition = [c for c in double_check_comp if c['name'] == request.form['competition']][0]
            club = [c for c in double_check_club if c['name'] == request.form['club']][0]
            double_check = return_smallest(club, competition)
            has_booked = already_booked(club, competition)
            print(competition)
            print(club)
            print(double_check)
            print(has_booked)

            if places_required <= double_check and places_required <= (MAX_BOOKED_PLACES - already_booked) :
                competition['numberOfPlaces'] = str(int(competition['numberOfPlaces']) - places_required)
                club['points'] = str(int(club['points']) - places_required)

                if has_booked == 0:
                    club['competitions'] = club['competitions'].append({'name': competition['name'],
                                                                        'places': places_required})
                else:
                    for comp in club['competitions']:
                        if comp['name'] == competition['name']:
                            comp['places'] = str(int(comp['places']) + places_required)
                clubs_to_json = json.dumps({"clubs": double_check_club})
                competitions_to_json = json.dumps({"competitions": double_check_comp})
                update_clubs(clubs_to_json)
                update_competitions(competitions_to_json)
                competitions = load_competitions()
                flash('Great-booking complete!')

                return render_template('welcome.html', club=club, competitions=competitions)

            else:
                flash("Places were reserved by another club before your validation. Please retry.")
                return render_template('welcome.html', club=club, competitions=competitions)

        else:
            flash("Something went wrong-please try again")
            return render_template('welcome.html', club=club, competitions=competitions)

    except:
        flash("You are not logged in.")
        return redirect(url_for('index'))

@app.route('/fullDisplay')
def full_display():
    clubs_list = [club["email"] for club in clubs]

    try:
        if session["user_id"] in clubs_list:
            return render_template('full_display.html', clubs=clubs)
        else:
            flash("Please log in to access this page.")
            return redirect(url_for('index'))

    except:
        flash("Something went wrong-please try again.")
        return redirect(url_for('index'))
