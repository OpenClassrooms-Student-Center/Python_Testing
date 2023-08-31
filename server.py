from __future__ import annotations

import json
from datetime import datetime
from http import HTTPStatus

from flask import Flask, render_template, request, redirect, flash, url_for


def load_clubs(file_name):
    with open(file_name) as c:
        listOfClubs = json.load(c)["clubs"]
        return listOfClubs


def load_competitions(file_name):
    with open(file_name) as comps:
        listOfCompetitions = json.load(comps)["competitions"]
        return listOfCompetitions


def is_competition_over(competition):
    return datetime.strptime(competition["date"], "%Y-%m-%d %H:%M:%S") < datetime.now()


app = Flask(__name__)
app.secret_key = "something_special"

clubs = load_clubs("clubs.json")
competitions = load_competitions("competitions.json")

# clubs = load_clubs("tests/clubs.json")
# competitions = load_competitions("tests/competitions.json")


@app.route("/")
def index():
    return render_template("index.html"), HTTPStatus.OK


@app.route("/showSummary", methods=["POST"])
def show_summary():
    email = request.form.get("email", None)
    club = next((club for club in clubs if club["email"] == email), False)
    if club:
        return (
            render_template("welcome.html", club=club, competitions=competitions),
            HTTPStatus.OK,
        )
    else:
        flash("Sorry, that email wasn't found.")
        return render_template("index.html"), HTTPStatus.BAD_REQUEST


@app.route("/book/<competition>/<club>")
def book(competition, club):
    found_club = next(
        (found_club for found_club in clubs if found_club["name"] == club), False
    )

    found_competition = next(
        (
            found_competition
            for found_competition in competitions
            if found_competition["name"] == competition
        ),
        False,
    )

    if found_competition and is_competition_over(found_competition):
        flash("Sorry, this competition is over, places are not available anymore.")
        return (
            render_template("welcome.html", club=found_club, competitions=competitions),
            HTTPStatus.BAD_REQUEST,
        )

    if found_club and found_competition:
        return (
            render_template(
                "booking.html",
                club=found_club,
                competition=found_competition,
            ),
            HTTPStatus.OK,
        )
    else:
        flash("Something went wrong-please try again")
        return (
            render_template("welcome.html", club=found_club, competitions=competitions),
            HTTPStatus.BAD_REQUEST,
        )


@app.route("/purchasePlaces", methods=["POST"])
def purchase_places():
    club_name = request.form.get("club", False)
    club = next((club for club in clubs if club["name"] == club_name), False)

    if not club:
        flash("Something went wrong-please try again")
        return (
            render_template("welcome.html", club=club, competitions=competitions),
            HTTPStatus.BAD_REQUEST,
        )

    places_required = request.form.get("places", "%")
    if not places_required.isdigit():
        flash("Please provide a valid rounded number")
        return (
            render_template("welcome.html", club=club, competitions=competitions),
            HTTPStatus.BAD_REQUEST,
        )

    places_required = int(places_required)
    if places_required > 12:
        flash("Sorry you can't book more than 12 places")
        return (
            render_template("welcome.html", club=club, competitions=competitions),
            HTTPStatus.BAD_REQUEST,
        )

    competition_name = request.form.get("competition", False)

    competition = next(
        (
            competition
            for competition in competitions
            if competition["name"] == competition_name
        ),
        False,
    )

    if not competition or is_competition_over(competition):
        flash("Something went wrong-please try again")
        return (
            render_template("welcome.html", club=club, competitions=competitions),
            HTTPStatus.BAD_REQUEST,
        )

    competition_remaining_places = int(competition.get("numberOfPlaces", 0))

    if not competition_remaining_places > 0:
        flash("Sorry this competition is already full.")
        return (
            render_template("welcome.html", club=club, competitions=competitions),
            HTTPStatus.BAD_REQUEST,
        )

    club_remaining_point = int(club["points"]) - places_required
    if club_remaining_point < 0:
        flash(
            f"Sorry you can't book more than {club_remaining_point + places_required} places."
        )
        return (
            render_template("welcome.html", club=club, competitions=competitions),
            HTTPStatus.BAD_REQUEST,
        )

    club["points"] = club_remaining_point
    competition["numberOfPlaces"] = competition_remaining_places - places_required
    flash("Great-booking complete!")
    return (
        render_template("welcome.html", club=club, competitions=competitions),
        HTTPStatus.OK,
    )


# TODO: Add route for points display


@app.route("/logout")
def logout():
    return redirect(url_for("index"), HTTPStatus.FOUND)
