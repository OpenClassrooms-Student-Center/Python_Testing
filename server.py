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
    try:
        club = [club for club in clubs if club["email"] == request.form["email"]][0]
    except IndexError:
        flash("Email does not exist")
        return redirect(url_for("index"))
    return render_template("welcome.html", club=club, competitions=competitions)


@app.route("/book/<competition>/<club>")
def book(competition, club):
    foundClub = [c for c in clubs if c["name"] == club][0]
    foundCompetition = [c for c in competitions if c["name"] == competition][0]
    if foundClub and foundCompetition:
        return render_template("booking.html", club=foundClub, competition=foundCompetition)
    else:
        flash("Something went wrong-please try again")
        return render_template("welcome.html", club=club, competitions=competitions)


@app.route("/purchasePlaces", methods=["POST"])
def purchasePlaces():
    competition = [c for c in competitions if c["name"] == request.form["competition"]][0]
    club = [c for c in clubs if c["name"] == request.form["club"]][0]
    if request.form["places"]:
        placesRequired = int(request.form["places"])
        if (int(competition["numberOfPlaces"]) - placesRequired) < 0:
            flash("You cannot reserve this places amount. places are limited")
        elif placesRequired > 12:
            flash("You cannot reserve more than 12 places")
        elif placesRequired > int(club["points"]):
            flash("your club does not have enough points to affords this.")
        else:
            competition["numberOfPlaces"] = int(competition["numberOfPlaces"]) - placesRequired
            club["points"] = str(int(club["points"]) - placesRequired)
            flash("Great-booking complete!")
    else:
        flash("You have to set place amount.")

    return render_template("welcome.html", club=club, competitions=competitions)


# TODO: Add route for points display
@app.route("/clubs_overview")
def displayPoints():
    clubs = [club for club in loadClubs()]
    if clubs:
        return render_template("clubs_overview.html", clubs=clubs)
    flash("Something went wrong !")
    return redirect(url_for("index"))


@app.route("/logout/", methods=['GET'])
def logout():
    return redirect(url_for("index"))



if __name__ == '__main__':
    import os
    # guaranteed to not be run on a production server
    assert os.path.exists('.env')  # for other environment variables...
    os.environ['FLASK_ENV'] = 'development'  # HARD CODE since default is production
    app.run(debug=True)