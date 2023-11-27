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

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/showSummary',methods=['POST'])
def showSummary():
    club = [club for club in clubs if club['email'] == request.form['email']][0]
    return render_template('welcome.html',club=club,competitions=competitions)


@app.route('/book/<competition>/<club>')
def book(competition,club):
    foundClub = [c for c in clubs if c['name'] == club][0]
    foundCompetition = [c for c in competitions if c['name'] == competition][0]
    if foundClub and foundCompetition:
        return render_template('booking.html',club=foundClub,competition=foundCompetition)
    else:
        flash("Something went wrong-please try again")
        return render_template('welcome.html', club=club, competitions=competitions)


@app.route('/purchasePlaces',methods=['POST'])
def purchasePlaces():
    competition = [c for c in competitions if c['name'] == request.form['competition']][0]
    club = [c for c in clubs if c['name'] == request.form['club']][0]
    placesRequired = int(request.form['places'])
    competition['numberOfPlaces'] = int(competition['numberOfPlaces'])-placesRequired
    flash('Great-booking complete!')
    return render_template('welcome.html', club=club, competitions=competitions)


# TODO: Add route for points display


@app.route('/logout')
def logout():
    return redirect(url_for('index'))