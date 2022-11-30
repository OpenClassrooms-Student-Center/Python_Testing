import json
from datetime import datetime
from flask import (Flask,
                   render_template,
                   request,
                   redirect,
                   flash,
                   url_for,
                   session)


def load_json(file_name):
    """ Open the file database/file_name.json, extract and return a list of dicts
        This list is itself in a dict, inside the field {file_name} """
    with open(f'database/{file_name}.json') as file:
        return json.load(file)[file_name]


def save_json(file_name, data):
    """ Open/create the file database/file_name.json with the list of dicts 'data'
        This list will be saved in a dict, in the field {file_name} """
    with open(f'database/{file_name}.json', 'w') as file:
        json.dump({file_name: data}, file, indent=True)


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


def maximum_points_allowed(competition, club, maxi_club_per_competition=12):
    """ Return the maximum avaliable places for this club and this competition """

    nb_authorised_places = maxi_club_per_competition
    if club['id'] in competition:
        nb_authorised_places -= int(competition[club['id']])

    return min(int(competition['numberOfPlaces']), int(club['points']), nb_authorised_places)


def is_competition_pass_the_deadline(comp):
    """ Return true if the competition datetime is inferior than the current datetime """

    return datetime.fromisoformat(comp['date']) < datetime.now()


def find_or_raise(json, name):
    """ load the mentioned json and return the first entry with the field 'name' equal to name
        Raise a NameError if not found
        Raise a json.JSONDecodeError if load_json fails
    """
    list_elem = [e for e in load_json(json) if e['name'] == name]

    if list_elem:
        return list_elem[0]
    else:
        raise NameError


def create_app(config):

    _MAX_POINTS_PER_COMP = 100000 if 'LOCUST' in config else 12

    app = Flask(__name__)
    app.debug = True if 'DEBUG' in config else False
    app.secret_key = 'something_special'

    app.jinja_env.globals['maximum_points_allowed'] = maximum_points_allowed
    app.jinja_env.globals['is_competition_pass_the_deadline'] = is_competition_pass_the_deadline

    @app.route('/')
    def index():
        return render_template('index.html')

    @app.route('/login', methods=['POST'])
    def login():

        try:
            clubs = [club for club in load_json('clubs') if club['email'] == request.form['email']]
            if clubs:
                session['logged_club'] = clubs[0]
                return redirect(url_for('show_competitions'))

            else:
                flash(f"Sorry, '{request.form['email']}' wasn't found", "flash_error")
                return redirect(url_for('index'))

        except json.JSONDecodeError:
            flash("Database access failed, please retry", "flash_error")
            return redirect(url_for('index'))

    @app.route('/showCompetitions')
    def show_competitions():

        if 'logged_club' in session:

            try:
                competitions = load_json('competitions')
                competitions.sort(key=lambda club: club['date'], reverse=True)  # Sort competitions by date

                return render_template('competitions.html', club=session['logged_club'], competitions=competitions)

            except json.JSONDecodeError:
                flash("Database access failed, please retry", "flash_error")
                return redirect(url_for('index'))

        else:
            flash("This action needs to be logged", "flash_warning")
            return redirect(url_for('index'))

    @app.route('/book/<competition>')
    def book(competition):

        if 'logged_club' in session:

            try:
                found_competition = find_or_raise('competitions', competition)
                found_club = find_or_raise('clubs', session['logged_club']['name'])

                maximum = maximum_points_allowed(found_competition, found_club, _MAX_POINTS_PER_COMP)
                if maximum == 0:
                    flash("You cannot book a new place", "flash_warning")

                return render_template('booking.html',
                                       club=found_club,
                                       competition=found_competition,
                                       maximum_allowed=maximum)

            except json.JSONDecodeError:
                flash("Database access failed, please retry", "flash_error")
                return redirect(url_for('show_competitions'))

            except NameError:
                flash(f"Sorry, '{session['logged_club']['name']}' or '{competition}' wasn't found", "flash_error")
                return redirect(url_for('show_competitions'))

        else:
            flash("This action needs to be logged", "flash_warning")
            return redirect(url_for('index'))

    @app.route('/purchasePlaces', methods=['POST'])
    def purchase_places():

        if 'logged_club' in session:

            try:
                try:
                    found_comp = find_or_raise('competitions', request.form['competition'])
                    found_club = find_or_raise('clubs', session['logged_club']['name'])

                    placesRequired = int(request.form['places'])

                    if is_competition_pass_the_deadline(found_comp):
                        flash(f"This competition is closed {found_comp['date']}", 'flash_warning')

                    elif placesRequired <= 0:
                        raise ValueError

                    elif placesRequired <= int(maximum_points_allowed(found_comp, found_club, _MAX_POINTS_PER_COMP)):

                        # Remove used points from club and competition
                        found_comp['numberOfPlaces'] = int(found_comp['numberOfPlaces']) - placesRequired
                        found_club['points'] = int(found_club['points']) - placesRequired

                        # Also save the club id and its number of places to respect the limits
                        if found_club['id'] in found_comp:
                            found_comp[found_club['id']] = int(found_comp[found_club['id']]) + placesRequired
                        else:
                            found_comp[found_club['id']] = placesRequired

                        # Save
                        update_json('competitions', found_comp)
                        update_json('clubs', found_club)

                        # Update the logged club (To avoid a json load in showCompetitions)
                        session['logged_club'] = found_club

                        flash('Great-booking complete!', 'flash_info')

                    else:
                        flash(f"You are allowed to book "
                              f"{maximum_points_allowed(found_comp, found_club, _MAX_POINTS_PER_COMP)} "
                              "places maximum",
                              'flash_warning')

                except ValueError:
                    flash('Invalid value', 'flash_error')

                except NameError:
                    flash(f"Sorry, '{request.form['competition']}' or "
                          f"'{session['logged_club']['name']}' wasn't found",
                          "flash_error")

                return render_template('competitions.html',
                                       club=session['logged_club'],
                                       competitions=load_json('competitions'))

            except json.JSONDecodeError:
                flash("Database access failed, please retry", "flash_error")
                return redirect(url_for('show_competitions'))

        else:
            flash("This action needs to be logged", "flash_warning")
            return redirect(url_for('index'))

    @app.route('/showClubs')
    def show_clubs():

        try:
            clubs = load_json('clubs')
            clubs.sort(key=lambda club: club['name'].lower())  # Sort by name

            if 'logged_club' in session:
                return render_template('clubs.html', clubs=clubs, club=session['logged_club'])
            else:
                return render_template('clubs.html', clubs=clubs)

        except json.JSONDecodeError:
            flash("Database access failed, please retry", "flash_error")

            if 'logged_club' in session:
                return redirect(url_for('show_competitions'))
            else:
                return redirect(url_for('index'))

    @app.route('/logout')
    def logout():
        session.clear()
        return redirect(url_for('index'))

    return app


if __name__ == "__main__":
    app = create_app({"DEBUG": True})
    app.run()
