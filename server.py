import json
from flask import Flask, render_template, request, redirect, flash, url_for, session

MAX_CLUB_POINTS = 12

def load_clubs():
    with open('clubs.json') as c:
         list_of_clubs = json.load(c)['clubs']
         return list_of_clubs

def load_competitions():
    with open('competitions.json') as comps:
         list_of_competitions = json.load(comps)['competitions']
         return list_of_competitions

def update_clubs_score(content):
    with open('clubs.json') as c:
         updated_clubs = json.dump(c)['clubs']
         return list_of_clubs

def return_smallest(club, competition):
    club_points = int(club["points"])
    available_places = int(competition["numberOfPlaces"])
    if club_points < available_places:
        max_selector = club_points
    else:
        max_selector = available_places

    return max_selector


app = Flask(__name__)
app.secret_key = 'something_special'

competitions = load_competitions()
clubs = load_clubs()


@app.route('/')
def index():
    """Shows the form whose data will inform show_summary()"""
    return render_template('index.html')

@app.route('/showSummary', methods=['POST'])
def show_summary():
    """Check whether the entered email exists.
    If so, store the user's email in a new cession (barring user ids).
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
            return render_template('welcome.html',club=club,competitions=competitions)

        flash(error)
        return redirect(url_for('index'))

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))


@app.route('/book/<competition>/<club>')
def book(competition,club):
    found_club = [c for c in clubs if c['name'] == club][0]
    found_competition = [c for c in competitions if c['name'] == competition][0]
    max_selector = MAX_CLUB_POINTS
    if int(found_club['points']) < MAX_CLUB_POINTS or int(found_competition['numberOfPlaces']) < MAX_CLUB_POINTS:
        max_selector = return_smallest(found_club, found_competition)

    try:
        if found_club and found_competition and session["user_id"] == found_club["email"]:
            return render_template('booking.html', club=found_club,
                                    competition=found_competition, max_selector=max_selector)

        else:
            flash("Something went wrong-please try again")
            return render_template('welcome.html', club=club, competitions=competitions)
    except:
        flash("You are not logged in.")
        return redirect(url_for('index'))


@app.route('/purchasePlaces',methods=['POST'])
def purchase_places():
    """Check that the user is logged in.
    Then, check that the places are still available.
    If so, deduce the club points and places involved and
    redirect user to the welcome template."""
    competition = [c for c in competitions if c['name'] == request.form['competition']][0]
    club = [c for c in clubs if c['name'] == request.form['club']][0]
    places_required = int(request.form['places'])

    try:
        if session["user_id"] == club["email"] and places_required < 0:
            #TODO: to change if there's a better way of checking
            double_check_comp = load_competitions()
            double_check_club = load_clubs()
            competition = [c for c in double_check_comp if c['name'] == request.form['competition']][0]
            club = [c for c in double_check_club if c['name'] == request.form['club']][0]
            double_check = return_smallest(club, competition)

            if places_required <= double_check and places_required <= MAX_CLUB_POINTS:
                competition['numberOfPlaces'] = int(competition['numberOfPlaces']) - places_required
                club['points'] = int(club['points']) - places_required
                clubs_to_json = json.dumps({"clubs": double_check_club})
                competitions_to_json = json.dumps({"competitions": double_check_comp})
                open('clubs.json','w').write(to_json)
                open('competitions.json','w').write(to_json)
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


# TODO: Add route for points display
