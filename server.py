import json
import datetime
from flask import Flask, render_template, request, redirect, flash, url_for


# ============================================ FLASK APP INITIALIZATION

app = Flask(__name__)
app.secret_key = 'something_special'


def page_not_found(e):
    return render_template('404.html'), 404


app.register_error_handler(404, page_not_found)


# ============================================ CONSTANTS

MAX_PLACES = 12
PATH_JSON_CLUBS = 'clubs.json'
PATH_JSON_COMPETITIONS = 'competitions.json'

# ============================================ LOAD JSON DATA


def loadClubs():
    try:
        if PATH_JSON_COMPETITIONS:
            with open(PATH_JSON_CLUBS) as c:
                listOfClubs = json.load(c)['clubs']
                if listOfClubs and len(listOfClubs) > 0:
                    return listOfClubs
                else:
                    raise Exception("This file is empty, or key not found")

    except Exception as error:
        return str(error)


def loadCompetitions():
    try:
        if PATH_JSON_COMPETITIONS:
            with open(PATH_JSON_COMPETITIONS) as c:
                listOfCompetitions = json.load(c)['competitions']
                listOfCompetitions.sort(key=lambda x: x["date"], reverse=True)
                if listOfCompetitions and len(listOfCompetitions) > 0:
                    return listOfCompetitions
                else:
                    raise Exception("This file is empty, or key not found")

    except Exception as error:
        return str(error)


competitions = loadCompetitions()
clubs = loadClubs()
now = datetime.datetime.now()
current_date = now.strftime("%Y-%m-%d, %H:%M:%S")


# ========================================================= INDEX ROUTE


@app.route('/')
@app.errorhandler(500)
def index():
    """
        Displays home page of the app.
        if no data is available then return :
            - status code 500 and the appropriate template (500.html)
    """

    if isinstance(clubs, list) and isinstance(competitions, list):
        return render_template('index.html')
    else:
        return render_template('500.html'), 500


# =========================================================== SUMMARY PAGE


@app.route('/showSummary', methods=['POST'])
def show_summary():
    """
        Displays the summary of all competitions
        and points available of the connected club
        if email is not found return error message
    """
    try:
        club = [club for club in clubs if club['email'] == request.form['email']][0]

        if club:
            return render_template('welcome.html', club=club, competitions=competitions, current_date=current_date)

    except IndexError:
        flash("Sorry, this email wasn't found. Please try again with a correct email !!")
        return redirect(url_for('index'))


# ====================================================== ROUTE FOR BOOK PLACES


@app.route('/book/<competition>/<club>')
def book(competition, club):
    """
    Displays :
        Competition's name and places available
        & the booking form or displays an error message.
    """
    try:
        foundClub = [c for c in clubs if c['name'] == club][0]
        foundCompetition = [c for c in competitions if c['name'] == competition][0]
        return render_template('booking.html', club=foundClub, competition=foundCompetition)

    except IndexError:
        flash("Sorry, this club or competition wasn't found !!")
        return render_template('welcome.html', club=club, competitions=competitions, current_date=current_date)


# ============================================================ ROUTE FOR PURCHASE PLACES

cart = {
    competition["name"]: {club["name"]: 0 for club in clubs}
    for competition in competitions
}


@app.route('/purchasePlaces', methods=['POST'])
@app.errorhandler(400)
def purchase_places():
    """
        Act like a Controller of the booking form:
        - By validating it,
        - Or handeling errors
    """

    competition = [c for c in competitions if c['name'] == request.form['competition']][0]
    club = [c for c in clubs if c['name'] == request.form['club']][0]
    club_points = int(club['points'])
    placesRequired = int(request.form['places'])
    current_cart = cart[competition["name"]][club["name"]]
    current_places_available = int(competition['numberOfPlaces'])

    if competition['date'] < current_date:
        flash("Sorry, this competition is over !")
        return render_template('welcome.html', club=club, competitions=competitions, current_date=current_date), 400

    elif placesRequired > club_points:
        flash("Sorry, your club doesn't have enough points !")
        return render_template('booking.html', club=club, competition=competition, current_date=current_date), 400

    elif placesRequired > MAX_PLACES:
        flash(f"Sorry, you can't book more than {MAX_PLACES} places !")
        return render_template('booking.html', club=club, competition=competition, current_date=current_date), 400

    elif placesRequired + current_cart > MAX_PLACES:
        flash(f"""Sorry, you have already booked places, for this competition
        and now you have exceeded the limit of {MAX_PLACES} places !""")
        return render_template('booking.html', club=club, competition=competition, current_date=current_date), 400

    elif placesRequired > current_places_available:
        flash("Sorry, you book more places than available !")
        return render_template('booking.html', club=club, competition=competition, current_date=current_date), 400

    else:
        competition['numberOfPlaces'] = int(competition['numberOfPlaces'])-placesRequired

        club['points'] = int(club['points']) - placesRequired

        cart[competition["name"]][club["name"]] += placesRequired

        flash(f"Great you have booked {placesRequired} places! for {competition['name']}")

        return render_template('welcome.html',
                               club=club, competitions=competitions,
                               current_date=current_date,
                               add_to_cart=cart[competition["name"]][club["name"]])

# ================================================= ROUTE FOR BOARD DISPLAY


@app.route('/board', methods=['GET'])
def show_board():
    """
        Displays the Public Board of all clubs with their points.
    """
    return render_template('board.html', all_clubs=clubs)


# ================================================= ROUTE FOR LOGOUT


@app.route('/logout')
def logout():
    return redirect(url_for('index'))
