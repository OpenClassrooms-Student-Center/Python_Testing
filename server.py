import json
from datetime import datetime
from flask import (Flask,
                   render_template,
                   request,
                   redirect,
                   flash,
                   url_for,
                   get_flashed_messages)


MAXIMUM_POINTS_PER_COMP = 12


def load_json(file_name):
    """ Open the file database/file_name.json, extract and return a list of dicts
        This list is itself in a dict, inside the field {file_name} """
    with open(f'database/{file_name}.json') as file:
        return json.load(file)[file_name]


def save_json(file_name, data):
    """ Open/create the file database/file_name.json with the list of dicts 'data'
        This list will be saved in a dict, in the field {file_name} """
    with open(f'database/{file_name}.json', 'w') as file:
        json.dump({file_name: data}, file)


def update_json(file_name, data):
    """ Update an entry in the '/database/file_name.json
        If the file already contains an entry with the field 'name', the latter will be erase.
        Otherwise, it just adds 'data' and save the file. """
    tab = load_json(file_name)
    for entry in tab:
        if entry['name'] == data['name']:
            tab.remove(entry)
            break

    tab.insert(0, data)
    save_json(file_name, tab)


def maximum_points_allowed(competition, club):
    """ Return the maximum avaliable places for this club and this competition """

    nb_authorised_places = MAXIMUM_POINTS_PER_COMP
    if club['id'] in competition:
        nb_authorised_places -= int(competition[club['id']])

    return min(int(competition['numberOfPlaces']), int(club['points']), nb_authorised_places)


def is_competition_pass_the_deadline(comp):
    """ Return true if the competition datetime is inferior than the current datetime """

    return datetime.fromisoformat(comp['date']) < datetime.now()


def find_or_raise(json, name):
    """ load the mentioned json and return the first entry with the field 'name' equal to name
        Raise a NameError if not found """
    list_elem = [e for e in load_json(json) if e['name'] == name]

    if list_elem:
        return list_elem[0]
    else:
        raise NameError


def create_app(config):

    app = Flask(__name__)
    app.secret_key = 'something_special'
    app.jinja_env.globals['maximum_points_allowed'] = maximum_points_allowed
    app.jinja_env.globals['is_competition_pass_the_deadline'] = is_competition_pass_the_deadline

    @app.route('/')
    def index():
        return render_template('index.html')

    @app.route('/showSummary', methods=['POST'])
    def show_summary():

        clubs = [club for club in load_json('clubs') if club['email'] == request.form['email']]
        if clubs:
            return redirect(url_for('show_competitions', club=clubs[0]['name']))
        else:
            flash(f"Sorry, '{request.form['email']}' wasn't found", "flash_error")
            return render_template('index.html')

    @app.route('/showCompetitions/<club>')
    def show_competitions(club):

        try:
            found_club = find_or_raise('clubs', club)
            return render_template('welcome.html', club=found_club, competitions=load_json('competitions'))

        except NameError:
            flash(f"Sorry, '{club}' wasn't found", "flash_error")
            return redirect(url_for('index'))

    @app.route('/book/<competition>/<club>')
    def book(competition, club):

        try:
            found_competition = find_or_raise('competitions', competition)
            found_club = find_or_raise('clubs', club)

            maximum = maximum_points_allowed(found_competition, found_club)
            if maximum == 0:
                flash("You cannot book a new place", "flash_warning")

            return render_template('booking.html',
                                   club=found_club,
                                   competition=found_competition,
                                   maximum_allowed=maximum)

        except NameError:
            flash(f"Sorry, '{club}' or '{competition}' wasn't found", "flash_error")
            return redirect(url_for('index'))

    @app.route('/purchasePlaces', methods=['POST'])
    def purchase_places():

        try:
            found_comp = find_or_raise('competitions', request.form['competition'])
            found_club = find_or_raise('clubs', request.form['club'])

            try:
                placesRequired = int(request.form['places'])

                if is_competition_pass_the_deadline(found_comp):
                    flash(f"This competition is closed {found_comp['date']}", 'flash_warning')

                elif placesRequired <= 0:
                    raise ValueError

                elif placesRequired <= int(maximum_points_allowed(found_comp, found_club)):

                    # Remove used points from club and competition
                    found_comp['numberOfPlaces'] = int(found_comp['numberOfPlaces']) - placesRequired
                    found_club['points'] = int(found_club['points']) - placesRequired

                    # Also save the club id and its number of places to respect the limits (MAXIMUM_POINTS_PER_COMP)
                    if found_club['id'] in found_comp:
                        found_comp[found_club['id']] = int(found_comp[found_club['id']]) + placesRequired
                    else:
                        found_comp[found_club['id']] = placesRequired

                    # Save
                    update_json('competitions', found_comp)
                    update_json('clubs', found_club)

                    flash('Great-booking complete!', 'flash_info')
                    return render_template('welcome.html', club=found_club, competitions=load_json('competitions'))

                else:
                    flash(f"You are allowed to book {maximum_points_allowed(found_comp, found_club)} places maximum",
                          'flash_warning')

            except ValueError:
                flash('Invalid value', 'flash_error')

            return render_template('welcome.html', club=found_club, competitions=load_json('competitions'))

        except NameError:
            flash(f"Sorry, '{request.form['competition']}' or '{request.form['club']}' wasn't found", "flash_error")
            return redirect(url_for('index'))

    @app.route('/show_clubs/<club>')
    def show_clubs(club):

        try:
            # load clubs and sort them by name
            clubs = load_json('clubs')
            clubs.sort(key=lambda club: club['name'].lower())

            found_club = find_or_raise('clubs', club)
            return render_template('clubs.html', clubs=clubs, club=found_club)

        except NameError:
            flash(f"Sorry, '{club}' or wasn't found", "flash_error")
            return redirect(url_for('index'))

    @app.route('/logout')
    def logout():
        return redirect(url_for('index'))

    return app


# app = create_app({"TESTING": False})
app = create_app({"TESTING": True})


if __name__ == "__main__":
    app.run()
