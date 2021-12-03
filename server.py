import datetime
import json

from flask import Flask, render_template, request, redirect, flash, url_for, session

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
    """Shows the form whose data will inform show_summary()"""
    return render_template('index.html')

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

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))


@app.route('/book/<competition>/<club>')
def book(competition, club):
    found_club = [c for c in clubs if c['name'] == club][0]
    found_competition = [c for c in competitions if c['name'] == competition][0]

    try:
        if found_club and found_competition and session["user_id"] == found_club["email"]:
            if datetime.datetime.fromisoformat(found_competition['date']) < datetime.datetime.now():
                flash("You cannot book places for a past event.")
                return render_template('welcome.html', club=club, competitions=competitions)
            else:
                return render_template('booking.html',club=found_club, competition=found_competition)

        else:
            flash("Something went wrong - please try again")
            return redirect(url_for('index'))

    except:
        flash("You are not logged in.")
        return redirect(url_for('index'))


@app.route('/purchasePlaces',methods=['POST'])
def purchase_places():
    competition = [c for c in competitions if c['name'] == request.form['competition']][0]
    club = [c for c in clubs if c['name'] == request.form['club']][0]
    places_required = int(request.form['places'])
    competition['numberOfPlaces'] = int(competition['numberOfPlaces']) - places_required
    flash('Great - booking complete!')
    return render_template('welcome.html', club=club, competitions=competitions)


# TODO: Add route for points display
