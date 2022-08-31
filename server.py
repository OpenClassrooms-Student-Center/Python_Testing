import json
from flask import Flask,render_template,request,redirect,flash,url_for


def load_clubs():
    with open('clubs.json') as c:
        list_of_clubs = json.load(c)['clubs']
        return list_of_clubs


def load_competitions():
    with open('competitions.json') as comps:
        list_of_competitions = json.load(comps)['competitions']
        return list_of_competitions


app = Flask(__name__)
app.secret_key = 'something_special'

competitions = load_competitions()
clubs = load_clubs()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/showSummary', methods=['POST'])
def show_summary():
    filtered_clubs = [club for club in clubs if club['email'] == request.form['email']]
    if filtered_clubs:
        club = filtered_clubs[0]
        return render_template('welcome.html', club=club, competitions=competitions)
    else:
        message = "Email was not found. Please enter a valid email"
        return render_template('index.html', message=message), 404


@app.route('/book/<competition>/<club>')
def book(competition,club):
    foundClub = [c for c in clubs if c['name'] == club][0]
    foundCompetition = [c for c in competitions if c['name'] == competition][0]
    if foundClub and foundCompetition:
        return render_template('booking.html',club=foundClub,competition=foundCompetition)
    else:
        flash("Something went wrong-please try again")
        return render_template('welcome.html', club=club, competitions=competitions)


@app.route('/purchasePlaces', methods=['POST'])
def purchase_places():
    competition = [c for c in competitions if c['name'] == request.form['competition']][0]
    club = [c for c in clubs if c['name'] == request.form['club']][0]

    if not request.form['places']:
        flash("You did not send a number of places")
        return render_template('welcome.html', club=club, competitions=competitions)

    else:
        places_required = int(request.form['places'])
        if places_required <= 0:
            flash("Please choice a positif number of places")
        elif places_required > int(club["points"]):
            flash("You do not have enough points")
        else:
            club['points'] = int(club['points']) - places_required
            competition['numberOfPlaces'] = int(competition['numberOfPlaces'])-places_required
            flash('Great-booking complete!')

        return render_template('welcome.html', club=club, competitions=competitions)


# TODO: Add route for points display


@app.route('/logout')
def logout():
    return redirect(url_for('index'))
