import json
from flask import Flask, render_template, request, redirect, flash, url_for
from datetime import datetime


def load_clubs():
    with open("clubs.json") as c:
        listOfClubs = json.load(c)["clubs"]
        return listOfClubs


def load_competitions():
    with open("competitions.json") as comps:
        listOfCompetitions = json.load(comps)["competitions"]
        return listOfCompetitions


app = Flask(__name__)
app.secret_key = "something_special"
competitions = load_competitions()
clubs = load_clubs()
booked_places = []


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/showSummary", methods=["POST"])
def show_summary():
    try:
        club = [club for club in clubs if club["email"] == request.form["email"]][0]
    except IndexError:
        flash("Sorry, that email wasn't found")
        return render_template("index.html")
    else:
        return render_template("welcome.html", club=club, competitions=competitions)


@app.route("/book/<competition>/<club>")
def book(competition, club):
    found_club = [c for c in clubs if c["name"] == club][0]
    found_competition = [c for c in competitions if c["name"] == competition][0]
    competition_date = datetime.strptime(found_competition["date"], "%Y-%m-%d %H:%M:%S")
    if found_club and found_competition:
        if competition_date > datetime.today():
            return render_template(
                "booking.html", club=found_club, competition=found_competition
            )
        else:
            flash("You can't book places if the competition already started")
            return render_template(
                "welcome.html", club=found_club, competitions=competitions
            )
    else:
        flash("Something went wrong-please try again")
        return render_template("welcome.html", club=club, competitions=competitions)


@app.route("/purchasePlaces", methods=["POST"])
def purchase_places():
    competition = [c for c in competitions if c["name"] == request.form["competition"]][
        0
    ]
    club = [c for c in clubs if c["name"] == request.form["club"]][0]
    available_points = int(club["points"])
    i = 2  # i is the coefficient of placeRequired/available_points
    places_required = int(request.form["places"])
    if available_points < places_required * i:
        flash("You don't have enough points to purchase this amount of places !")
        return render_template("welcome.html", club=club, competitions=competitions)
    elif int(competition["numberOfPlaces"]) - places_required < 0:
        flash("There isn't enough places left for this competitions !")
        return render_template("welcome.html", club=club, competitions=competitions)
    else:
        booked_places.append(places_required)
        if sum(booked_places) > 12:
            flash("You can't purchase more than 12 places !")
            booked_places.remove(places_required)
            return render_template("welcome.html", club=club, competitions=competitions)
        else:
            competition["numberOfPlaces"] = (
                int(competition["numberOfPlaces"]) - places_required
            )
            club["points"] = available_points - places_required * i
            flash("Great-booking complete !")
            return render_template("welcome.html", club=club, competitions=competitions)


@app.route("/points")
def list_of_points():
    return render_template("list_of_points.html", clubs=clubs)


@app.route("/logout")
def logout():
    return redirect(url_for("index"))
