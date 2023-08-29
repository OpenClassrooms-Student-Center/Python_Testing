from datetime import datetime
import json
from flask import Flask, render_template, request, redirect, flash, url_for


def loadClubs():
    with open("clubs.json") as c:
        listOfClubs = json.load(c)["clubs"]
        return listOfClubs


def loadCompetitions():
    with open("competitions.json") as comps:
        listOfCompetitions = json.load(comps)["competitions"]
        return listOfCompetitions


app = Flask(__name__)
app.secret_key = "something_special"

competitions = loadCompetitions()
clubs = loadClubs()


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/showSummary", methods=["POST"])
def show_summary():
    email = request.form["email"]
    club = next((club for club in clubs if club["email"] == email), False)
    if club:
        return render_template("welcome.html", club=club, competitions=competitions)
    else:
        flash("Sorry, that email wasn't found.")
        return redirect(url_for("index"))


@app.route("/book/<competition>/<club>")
def book(competition, club):
    foundClub = [c for c in clubs if c["name"] == club][0]
    foundCompetition = [c for c in competitions if c["name"] == competition][0]
    if foundClub and foundCompetition:
        over = datetime.strptime(foundCompetition['date'], '%Y-%m-%d %H:%M:%S') < datetime.now()
        return render_template(
            "booking.html", club=foundClub, competition=foundCompetition, over=over
        )
    else:
        flash("Something went wrong-please try again")
        return render_template("welcome.html", club=club, competitions=competitions)


@app.route("/purchasePlaces", methods=["POST"])
def purchase_places():
    club_name = request.form["club"]
    club = next((club for club in clubs if club["name"] == club_name), False)

    placesRequired = int(request.form["places"])
    club_remaining_point = int(club["points"]) - placesRequired

    if club_remaining_point <= 0:
        flash(
            f"Sorry you can't book more than {club_remaining_point + placesRequired} places."
        )
        return render_template("welcome.html", club=club, competitions=competitions)

    competition_name = request.form["competition"]

    competition = next(
        (
            competition
            for competition in competitions
            if competition["name"] == competition_name
        ),
        False,
    )

    club["points"] = club_remaining_point
    competition["numberOfPlaces"] = int(competition["numberOfPlaces"]) - placesRequired
    flash("Great-booking complete!")
    return render_template("welcome.html", club=club, competitions=competitions)


# TODO: Add route for points display


@app.route("/logout")
def logout():
    return redirect(url_for("index"))
