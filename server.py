import json
from datetime import datetime
from flask import Flask, render_template, request, redirect, flash, url_for

MAX_PLACES = 12


def load_clubs():
    """
    Load the list of clubs from the 'clubs.json' file.

    Returns:
    - list: A list of dictionaries representing the clubs.
    """
    with open("clubs.json") as clubs_file:
        return json.load(clubs_file)["clubs"]


def load_competitions():
    """
    Load the list of competitions from the 'competitions.json' file.

    Returns:
    - list: A list of dictionaries representing the competitions.
    """
    with open("competitions.json") as competitions_file:
        return json.load(competitions_file)["competitions"]


def check_if_the_date_has_passed(date):
    """
    Check if the given date has already passed.

    Args:
    - date (str): The date to be checked in the format '%Y-%m-%d %H:%M:%S'.

    Returns:
    - bool: True if the date is in the future, False if it has passed.
    """
    format_str = "%Y-%m-%d %H:%M:%S"
    date = datetime.strptime(date, format_str)
    return date > datetime.now()


def write_on_json_file(json_file, key, value):
    """
    Write a key-value pair to a JSON file.

    Args:
    - json_file (str): The path to the JSON file.
    - key (str): The key to be written.
    - value: The value associated with the key.
    """
    with open(json_file, "w") as f:
        json.dump({key: value}, f, indent=4)


def cart_initialization():
    """
    Initialize an empty cart based on available competitions and clubs.

    Returns:
    - dict: A nested dictionary representing the cart with competitions as
    outer keys and clubs as inner keys, all initialized to zero.
    """
    cart = {
        competition["name"]: {club["name"]: 0 for club in clubs}
        for competition in competitions
    }
    return cart


def find_first_item_by_key(items_list, key, value):
    """
    Find the first item in a list of dictionaries based on a specified
    key-value pair.

    Args:
    - items_list (list): List of dictionaries.
    - key (str): Key to search for.
    - value (str): Value to match.

    Returns:
    - dict or None: The first dictionary in the list that contains the
    specified key-value pair, or None if no match is found.
    """
    matching_items = [item for item in items_list if item.get(key) == value]
    return matching_items[0] if matching_items else None


def find_items_by_key(items_list, key, value):
    """
    Find all items in a list of dictionaries based on a specified key-value
    pair.

    Args:
    - items_list (list): List of dictionaries.
    - key (str): Key to search for.
    - value (str): Value to match.

    Returns:
    - list or None: List of dictionaries that contain the specified
    key-value pair, or None if no match is found.
    """
    matching_items = [item for item in items_list if item.get(key) == value]
    return matching_items if matching_items else None


def check_booking_conditions(
    places_required,
    points,
    MAX_PLACES,
    current_cart,
    current_places_available,
    club,
    competition,
    flash_function=None,
):
    """
    Check the booking conditions before purchasing places for a competition.

    Args:
    - places_required (int): Number of places requested.
    - points (int): Points available for the club.
    - MAX_PLACES (int): Maximum allowed places for booking.
    - current_cart (int): Current number of places booked in the cart.
    - current_places_available (int): Current available places for the
    competition.
    - club (dict): Club information.
    - competition (dict): Competition information.
    - flash_function (function, optional): Flash message function.
    Defaults to None.

    Returns:
    - bool: True if booking conditions are met, False otherwise.
    """
    if places_required > points:
        if flash_function:
            flash_function("Sorry, your club doesn't have enough points!")
    elif places_required > MAX_PLACES:
        if flash_function:
            flash_function(
                f"Sorry, you can't book more than {MAX_PLACES} places!"
            )
    elif places_required + current_cart > MAX_PLACES:
        if flash_function:
            flash_function("Sorry, you have exceeded the booking limit!")
    elif places_required > current_places_available:
        if flash_function:
            flash_function("Sorry, you booked more places than available!")
    else:
        return True
    return False


app = Flask(__name__)
app.secret_key = "something_special"

clubs = load_clubs()
competitions = load_competitions()


@app.route("/")
def index():
    """
    Render the index page.

    Returns:
    - str: Rendered HTML content for the index page.
    """
    return render_template("index.html", clubs=clubs)


@app.route("/showSummary", methods=["POST"])
def show_summary():
    """
    Show the summary for a club based on the provided email.

    Returns:
    - str: Rendered HTML content for the welcome page or a redirection to the
    index page.
    """
    email = request.form.get("email")
    club = find_items_by_key(items_list=clubs, key="email", value=email)
    if not club:
        flash("Sorry, that email wasn't found.")
        return redirect(url_for("index"))
    club = club[0]
    return render_template(
        "welcome.html", club=club, competitions=competitions
    )


@app.route("/book/<competition>/<club>")
def book(competition, club):
    """
    Render the booking page for a specific competition and club.

    Args:
    - competition (str): The name of the competition.
    - club (str): The name of the club.

    Returns:
    - str: Rendered HTML content for the booking page or a redirection to
    the welcome page with a flash message.
    """
    found_club = find_first_item_by_key(
        items_list=clubs, key="name", value=club
    )
    found_competition = find_first_item_by_key(
        items_list=competitions, key="name", value=competition
    )
    if found_club and found_competition:
        return render_template(
            "booking.html", club=found_club, competition=found_competition
        )
    else:
        flash("Something went wrong - please try again")
    return render_template(
        "welcome.html", club=found_club, competition=found_competition
    )


@app.route("/purchasePlaces", methods=["POST"])
def purchase_places():
    """
    Process the purchase of places for a competition and club.

    This function handles the POST request to "/purchasePlaces", initializes
    the cart, and updates club and competition data based on the purchase.

    Returns:
    - str: Rendered HTML content for the welcome page with flash messages
    indicating the result of the purchase.
    """
    cart = cart_initialization()

    competition_name = request.form["competition"]
    club_name = request.form["club"]
    places_required = int(request.form["places"])

    competition = find_first_item_by_key(
        items_list=competitions, key="name", value=competition_name
    )
    club = find_first_item_by_key(
        items_list=clubs, key="name", value=club_name
    )
    current_cart = cart[competition["name"]][club["name"]]
    current_places_available = int(competition["numberOfPlaces"])
    points = int(club["points"])

    if check_if_the_date_has_passed(competition["date"]) is False:
        flash("Sorry, this competition is over!")
        return render_template(
            "booking.html", club=club, competition=competition
        )

    if check_booking_conditions(
        places_required=places_required,
        points=points,
        MAX_PLACES=MAX_PLACES,
        current_cart=current_cart,
        current_places_available=current_places_available,
        club=club,
        competition=competition,
    ):
        # Deduct points from the club
        for c in clubs:
            if c["name"] == club_name:
                c["points"] = str(int(c["points"]) - places_required)

        # Update the number of places available for the competition
        for c in competitions:
            if c["name"] == competition_name:
                c["numberOfPlaces"] = str(
                    int(c["numberOfPlaces"]) - places_required
                )

        # Save the updated data to JSON files
        write_on_json_file("clubs.json", "clubs", clubs)
        write_on_json_file("competitions.json", "competitions", competitions)

        cart[competition_name][club_name] += places_required

        flash(
            f"You have booked {places_required} places for {competition_name}!"
        )

    return render_template(
        "welcome.html",
        club=club,
        competitions=competitions,
        add_to_cart=cart[competition_name][club_name],
    )


@app.route("/board", methods=["GET"])
def show_board():
    """
    Render the board.html template displaying information about all clubs.

    This function handles the GET request to "/board" and renders the
    "board.html" template.

    Returns:
    - str: Rendered HTML content for the board page.
    """
    return render_template("board.html", all_clubs=clubs)


@app.route("/logout")
def logout():
    """
    Log out the user by redirecting to the index page.

    This function handles the GET request to "/logout" and redirects the
    user to the index page.

    Returns:
    - Redirect: Redirect to the index page.
    """
    return redirect(url_for("index"))
