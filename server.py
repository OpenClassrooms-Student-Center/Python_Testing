import json
from flask import (Flask,
                   render_template,
                   request,
                   redirect,
                   flash,
                   url_for,
                   get_flashed_messages)


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
    """ Return the maximum avaliable places for this club """

    if int(competition['numberOfPlaces']) <= int(club['points']):
        return competition['numberOfPlaces']
    else:
        return club['points']


def create_app(config):
    app = Flask(__name__)
    app.secret_key = 'something_special'

    @app.route('/')
    def index():
        return render_template('index.html')

    @app.route('/showSummary', methods=['POST'])
    def showSummary():
        club = [club for club in load_json('clubs') if club['email'] == request.form['email']][0]
        return render_template('welcome.html', club=club, competitions=load_json('competitions'))

    @app.route('/book/<competition>/<club>')
    def book(competition, club):
        foundClub = [c for c in load_json('clubs') if c['name'] == club][0]
        foundCompetition = [c for c in load_json('competitions') if c['name'] == competition][0]
        if foundClub and foundCompetition:

            return render_template('booking.html',
                                   club=foundClub,
                                   competition=foundCompetition,
                                   maximum_allowed=maximum_points_allowed(foundCompetition, foundClub))
        else:
            flash("Something went wrong-please try again")
            return render_template('welcome.html', club=club, competitions=load_json('competitions'))

    @app.route('/purchasePlaces', methods=['POST'])
    def purchasePlaces():
        competition = [c for c in load_json('competitions') if c['name'] == request.form['competition']][0]
        club = [c for c in load_json('clubs') if c['name'] == request.form['club']][0]

        # Remove used points for competition and club
        placesRequired = int(request.form['places'])

        if placesRequired <= int(maximum_points_allowed(competition, club)) and placesRequired > 0:

            competition['numberOfPlaces'] = int(competition['numberOfPlaces']) - placesRequired
            club['points'] = int(club['points']) - placesRequired

            # Save
            update_json('competitions', competition)
            update_json('clubs', club)

            flash('Great-booking complete!')
            return render_template('welcome.html', club=club, competitions=load_json('competitions'))

        else:
            flash(f"You are allowed to book {maximum_points_allowed(competition, club)} places maximum")
            return render_template('welcome.html', club=club, competitions=load_json('competitions'))

    # TODO: Add route for points display

    @app.route('/logout')
    def logout():
        return redirect(url_for('index'))

    return app


# app = create_app({"TESTING": False})
app = create_app({"TESTING": True})


if __name__ == "__main__":
    app.run()
