from __future__ import annotations

import json
from datetime import datetime
from http import HTTPStatus

from flask import Flask, render_template, request, redirect, flash, url_for


def load_data(file_name):
    with open(file_name) as data_file:
        data = json.load(data_file)
        return data


def is_competition_over(competition):
    return datetime.strptime(competition["date"], "%Y-%m-%d %H:%M:%S") < datetime.now()


def find_club_by_name(club_name):
    return next((club for club in clubs if club["name"] == club_name), None)


def find_competition_by_name(competition_name):
    return next(
        (
            competition
            for competition in competitions
            if competition["name"] == competition_name
        ),
        None,
    )


app = Flask(__name__)
app.secret_key = "something_special"

clubs = load_data("clubs.json")["clubs"]
competitions = load_data("competitions.json")["competitions"]

# clubs = load_data(("tests/clubs.json")
# competitions = load_data("tests/competitions.json")


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
    found_club = find_club_by_name(club)
    found_competition = find_competition_by_name(competition)

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
    club_name = request.form.get("club", None)
    places_required = request.form.get("places", None)
    competition_name = request.form.get("competition", None)

    club = find_club_by_name(club_name)
    competition = find_competition_by_name(competition_name)

    if not club or not competition or is_competition_over(competition):
        flash("Something went wrong-please try again")
        return (
            render_template("welcome.html", club=club, competitions=competitions),
            HTTPStatus.BAD_REQUEST,
        )

    if places_required is None or not places_required.isdigit():
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

    competition_remaining_places = int(competition.get("numberOfPlaces", 0))
    club_remaining_point = int(club["points"]) - places_required

    if not competition_remaining_places > 0:
        flash("Sorry this competition is already full.")
        return (
            render_template("welcome.html", club=club, competitions=competitions),
            HTTPStatus.BAD_REQUEST,
        )

    elif club_remaining_point < 0:
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
