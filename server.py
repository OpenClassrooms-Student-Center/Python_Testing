import datetime
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
def showSummary():
    club = [club for club in clubs if club["email"] == request.form["email"]]
    if len(club) == 0:
        message = "Email not found. Please try again."
        return render_template("index.html", message=message)
    else:
        return render_template(
            "welcome.html",
            club=club[0],
            competitions=competitions,
            today=str(datetime.date.today()),
        )


@app.route("/book/<competition>/<club>")
def book(competition, club):
    foundClub = [c for c in clubs if c["name"] == club][0]
    foundCompetition = [c for c in competitions if c["name"] == competition][0]
    if foundClub and foundCompetition:
        return render_template(
            "booking.html", club=foundClub, competition=foundCompetition
        )
    else:
        flash("Something went wrong-please try again")
        return render_template("welcome.html", club=club, competitions=competitions)


@app.route("/purchasePlaces", methods=["POST"])
def purchasePlaces():
    competition_name = request.form["competition"]
    club_name = request.form["club"]
    places_required = int(request.form["places"])

    competition = next(c for c in competitions if c["name"] == competition_name)
    club = next(c for c in clubs if c["name"] == club_name)

    # Check if club has enough points
    if int(club["points"]) < places_required:
        flash("Cannot redeem more points than available!")
    elif int(competition["numberOfPlaces"]) < places_required:
        flash("Cannot book more places than available!")
    elif places_required > 12:
        flash("Cannot redeem more than 12 places!")
    else:
        # Update the competition's available places and club's points
        competition["numberOfPlaces"] = str(
            int(competition["numberOfPlaces"]) - places_required
        )
        club["points"] = str(int(club["points"]) - places_required)
        flash("Great-booking complete!")

        # Save the updated data back to the JSON files
        saveClubs()
        saveCompetitions()

    return render_template("welcome.html", club=club, competitions=competitions)


def saveClubs():
    data = {"clubs": clubs}
    with open("clubs.json", "w") as file:
        json.dump(data, file)


def saveCompetitions():
    data = {"competitions": competitions}
    with open("competitions.json", "w") as file:
        json.dump(data, file)


@app.route("/logout")
def logout():
    return redirect(url_for("index"))
