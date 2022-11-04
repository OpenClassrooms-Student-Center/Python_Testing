import json
import datetime
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
now = datetime.datetime.now()
current_date = now.strftime("%Y-%m-%d, %H:%M:%S")


@app.route('/')
def index():
    return render_template('index.html')

# =========================================================== SUMMARY PAGE


@app.route('/showSummary', methods=['POST'])
def show_summary():
    """
    Displays the summary of all competitions
    and points available by the connected club
    """

    try:
        club = [club for club in clubs if club['email'] == request.form['email']][0]
        return render_template('welcome.html', club=club, competitions=competitions, current_date=current_date)
    except IndexError:
        flash("Sorry, this email wasn't found. Please try again with a correct email !!")
        return redirect(url_for('index'))


# ====================================================== ROUTE FOR BOOK PLACES


@app.route('/book/<competition>/<club>')
def book(competition,club):
    """
    Displays :
        Competition's name and places available
        & the booking form
    """
    foundClub = [c for c in clubs if c['name'] == club][0]
    foundCompetition = [c for c in competitions if c['name'] == competition][0]
    if foundClub and foundCompetition:
        return render_template('booking.html',club=foundClub,competition=foundCompetition)
    else:
        flash("Something went wrong-please try again")
        return render_template('welcome.html', club=club, competitions=competitions, current_date=current_date)


# ============================================================ ROUTE FOR PURCHASE PLACES


@app.route('/purchasePlaces',methods=['POST'])
@app.errorhandler(400)
def purchase_places():
    competition = [c for c in competitions if c['name'] == request.form['competition']][0]
    club = [c for c in clubs if c['name'] == request.form['club']][0]
    club_points = int(club['points'])
    placesRequired = int(request.form['places'])

    if competition['date'] < current_date:
        flash("Sorry, this competition is over !")
        return render_template('welcome.html', club=club, competitions=competitions, current_date=current_date), 400

    elif placesRequired > club_points:
        flash("Sorry, your club doesn't have enough points !")
        return render_template('booking.html', club=club, competition=competition, current_date=current_date), 400

    else:
        competition['numberOfPlaces'] = int(competition['numberOfPlaces'])-placesRequired
        club['points'] = int(club['points'])-placesRequired
        flash(f'''Great you have booked {placesRequired} places !
        for {competition['name']}''')
        return render_template('welcome.html', club=club, competitions=competitions, current_date=current_date)

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
