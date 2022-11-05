import json
from flask import Flask, render_template, request, redirect, flash, url_for


def load_json(file_name):
    with open(f'database/{file_name}.json') as file:
        return json.load(file)[file_name]


def save_json(file_name, data):
    with open(f'database/{file_name}.json', 'w') as file:
        json.dump({file_name: data}, file)


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
            return render_template('booking.html', club=foundClub, competition=foundCompetition)
        else:
            flash("Something went wrong-please try again")
            return render_template('welcome.html', club=club, competitions=load_json('competitions'))

    @app.route('/purchasePlaces', methods=['POST'])
    def purchasePlaces():
        competition = [c for c in load_json('competitions') if c['name'] == request.form['competition']][0]
        club = [c for c in load_json('clubs') if c['name'] == request.form['club']][0]
        placesRequired = int(request.form['places'])
        competition['numberOfPlaces'] = int(competition['numberOfPlaces']) - placesRequired
        flash('Great-booking complete!')
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
