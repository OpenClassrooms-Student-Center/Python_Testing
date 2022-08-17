import json
import datetime

from flask import Flask, render_template, request, redirect, flash, url_for


def loadClubs(clubs):
    with open(clubs) as c:
        listOfClubs = json.load(c)["clubs"]
        return listOfClubs


def loadCompetitions(competitions):
    with open(competitions) as comps:
        listOfCompetitions = json.load(comps)["competitions"]
        return listOfCompetitions

def create_app(config={}):
    app = Flask(__name__)
    app.config.update(config)
    app.secret_key = "something_special"
    if app.config['TESTING'] == True:
        competitions = loadCompetitions("tests/competitions_test.json")
        clubs = loadClubs("tests/clubs_test.json")
    else:
        competitions = loadCompetitions("competitions.json")
        clubs = loadClubs("clubs.json")


    @app.route("/")
    def index():
        return render_template("index.html")


    @app.route("/showSummary", methods=["POST"])
    def showSummary():
        date = datetime.datetime.now()
        date_string = date.strftime("%Y-%m-%d %H:%M:%S")
        try:
            club = [club for club in clubs if club["email"] == request.form["email"]][0]
            return render_template("welcome.html", club=club, competitions=competitions, date_string=date_string)
        except IndexError:
            error = "Sorry, that email wasn't found."
            return render_template("index.html", error=error), 401


    @app.route("/book/<competition>/<club>")
    def book(competition, club):
        date = datetime.datetime.now()
        date_string = date.strftime("%Y-%m-%d %H:%M:%S")
        try:
            foundClub = [c for c in clubs if c["name"] == club][0]
            foundCompetition = [c for c in competitions if c["name"] == competition][0]
            return render_template(
                "booking.html", club=foundClub, competition=foundCompetition)
        except IndexError:
                flash("Something went wrong-please try again")
                return render_template("welcome.html", club=club, competitions=competitions, date_string=date_string)


    @app.route("/purchasePlaces", methods=["POST"])
    def purchasePlaces():
        date = datetime.datetime.now()
        date_string = date.strftime("%Y-%m-%d %H:%M:%S")
        competition = [c for c in competitions if c["name"] == request.form["competition"]][
            0
        ]
        club = [c for c in clubs if c["name"] == request.form["club"]][0]
        placesRequired = int(request.form["places"])
        if int(club["points"]) < placesRequired * 3:
            flash("You cannot use more points then you have !")
            render_template("booking.html", club=club, competition=competition)
        elif int(competition["numberOfPlaces"]) < placesRequired:
            flash("This competition does not have enough places")
            render_template("booking.html", club=club, competition=competition)
        elif int(request.form['places']) > 12:
            flash('You cannot take more than 12 places')
            render_template('booking.html', club=club, competition=competition)
        elif '-' in request.form['places']:
            flash('You cannot enter negative number')
            render_template('booking.html', club=club, competition=competition)
        else:
            competition["numberOfPlaces"] = (
                int(competition["numberOfPlaces"]) - placesRequired
            )
            club["points"] = int(club["points"]) - placesRequired * 3
            flash("Great-booking complete!")
        return render_template("welcome.html", club=club, competitions=competitions, date_string=date_string)


    @app.route('/displayBoard')
    def displayBoard():
        return render_template('board.html', clubs=clubs)


    @app.route("/logout")
    def logout():
        return redirect(url_for("index"))
    
    return app
