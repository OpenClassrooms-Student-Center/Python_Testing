import json
from datetime import datetime
from flask import Flask, render_template, request, redirect, flash, url_for


def loadClubs():
    """
    Loads the list of clubs from the 'clubs.json' file.

    Returns:
        list: The list of clubs.
    """
    with open("clubs.json") as c:
        listOfClubs = json.load(c)["clubs"]
        return listOfClubs


def loadCompetitions():
    """
    Loads the list of competitions from the 'competitions.json' file.

    Returns:
        list: The list of competitions.
    """
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


def get_club(email):
    """Retourne le club correspondant à l'email donné, ou None si non trouvé."""
    for club in clubs:
        if club["email"] == email:
            return club
    return None


@app.route("/showSummary", methods=["POST"])
def showSummary():
    email = request.form["email"]
    club = get_club(email)
    if club is not None:
        return render_template("welcome.html", club=club, competitions=competitions)
    else:
        flash(f"Error: email {email} not found")
        return redirect(url_for("index"))


@app.route("/book/<competition>/<club>")
def book(competition, club):
    """
    Book a place for a competition at a specific club.

    Returns:
    - tuple: A tuple containing the rendered template, HTTP status code.
    """
    try:
        foundClub = [c for c in clubs if c["name"] == club][0]
        foundCompetition = [c for c in competitions if c["name"] == competition][0]
    except IndexError:
        flash("Something went wrong-please try again")
        return (
            render_template(
                "welcome.html", club=club, competitions=competitions, clubs=clubs
            ),
            400,
        )

    if foundClub and foundCompetition:
        competition_date = datetime.strptime(
            foundCompetition["date"], "%Y-%m-%d %H:%M:%S"
        )
        if competition_date < datetime.now():
            flash("Error: can not purchase a place for past competitions")
            return (
                render_template(
                    "welcome.html",
                    club=foundClub,
                    competitions=competitions,
                    clubs=clubs,
                ),
                200,
            )

        return render_template(
            "booking.html", club=foundClub, competition=foundCompetition
        )
    else:
        flash("Something went wrong-please try again")
        return (
            render_template(
                "welcome.html", club=foundClub, competitions=competitions, clubs=clubs
            ),
            400,
        )


@app.route("/purchasePlaces", methods=["POST"])
def purchasePlaces():
    """
    Purchase places for a competition.
    Returns:
        A rendered template for the booking page with the updated club and competition information.
    """
    global competitions

    # Get the data from the form.
    competition_name = request.form.get("competition")
    club_name = request.form.get("club")

    # Search for the corresponding competition and club.
    competition = [c for c in competitions if c["name"] == competition_name][0]
    club = next((c for c in clubs if c["name"] == club_name), None)

    try:
        placesRequired = int(request.form["places"])
    except ValueError:
        flash("Please enter a number between 0 and 12.", "error")
        return render_template("booking.html", club=club, competition=competition), 400

    placesRemaining = int(competition["numberOfPlaces"])

    # Check if the club has enough points. - points fix here
    if placesRequired > int(club["points"]):
        flash("You don't have enough points.", "error")
        return render_template("booking.html", club=club, competition=competition), 400

    # Check if there are enough places remaining in the competition.
    elif placesRequired > placesRemaining:
        flash(
            "Not enough places available, you are trying to book more than the remaining places.",
            "error",
        )
        return render_template("booking.html", club=club, competition=competition), 400

    # Check if the number of places exceeds the limit. - point fix here
    elif placesRequired > 12:
        # Max_places = club['points'] # faire une condition pour vérifa
        flash("You can't book more than 12 places in a competition.", "error")
        return render_template("booking.html", club=club, competition=competition), 400

    else:
        # Booking is successful.
        flash("Great-booking complete!")
        # flash(f'Great, succesfully booked {placesRequired} place(s)!')
        # Update club points and competition places. - points fix here
        club["points"] = int(club["points"]) - placesRequired
        competition["numberOfPlaces"] = (
            int(competition["numberOfPlaces"]) - placesRequired
        )

    # Render the welcome template with updated club and competition information.
    return render_template("welcome.html", club=club, competitions=competitions)


@app.route("/pointsBoard")
def pointsBoard():
    """
    Display the points board.

    Returns:
        A rendered template for the points board.
    """
    # Sort the clubs alphabetically by name
    # club_list = sorted(clubs, key=lambda club: club["name"])

    # Sort the clubs by points in descending order
    club_list = sorted(clubs, key=lambda club: int(club["points"]), reverse=True)

    # Render the template with the sorted list of clubs
    return render_template("points_board.html", clubs=club_list)


@app.route("/logout")
def logout():
    """
    Redirects the user to the index page.

    Returns:
        A redirect response to the index page.
    """
    return redirect(url_for("index"))
