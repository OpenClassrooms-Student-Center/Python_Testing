import json
from datetime import datetime
from flask import Flask,render_template,request,redirect,flash,url_for


def loadClubs():
    with open('clubs.json') as c:
         listOfClubs = json.load(c)['clubs']
         return listOfClubs


def loadCompetitions():
    with open('competitions.json') as comps:
         listOfCompetitions = json.load(comps)['competitions']
         return listOfCompetitions


def create_app(config, json_competitions, json_clubs):

    app = Flask(__name__)
    app.secret_key = 'something_special'
    app.config.update(config)

    competitions = json_competitions
    clubs = json_clubs

    @app.route('/')
    def index():
        return render_template('index.html')

    @app.route('/showSummary',methods=['POST'])
    def showSummary():
        try:
            club = [club for club in clubs if club['email'] == request.form['email']][0]
            flash(f"You are connected as {request.form['email']}", "success")
            return render_template('welcome.html',club=club,competitions=competitions)
        except IndexError:
            flash("Please enter a recognized email", "error")
            return render_template('index.html'), 401

    @app.route('/book/<competition>/<club>')
    def book(competition,club):
        try:
            foundClub = [c for c in clubs if c['name'] == club][0]
            foundCompetition = [c for c in competitions if c['name'] == competition][0]
            if datetime.strptime(foundCompetition["date"], '%Y-%m-%d %H:%M:%S') < datetime.today():
                flash("Cannot access on detail, this book is obsolete, please select one that has not already passed", "error")
                return render_template('welcome.html', club=club, competitions=competitions), 400
            else:
                return render_template('booking.html', club=foundClub, competition=foundCompetition)

        except IndexError:
            flash("Something went wrong-please try again", "error")
            return render_template('welcome.html', club=club, competitions=competitions), 400

    @app.route('/purchasePlaces',methods=['POST'])
    def purchasePlaces():
        competition = [c for c in competitions if c['name'] == request.form['competition']][0]
        club = [c for c in clubs if c['name'] == request.form['club']][0]
        placesRequired = int(request.form['places'])

        if placesRequired < 0:
            flash("Please, enter an integer greater than 0 as value", "error")
            return render_template('booking.html', club=club, competition=competition), 400
        elif placesRequired > int(club["points"]):
            flash("Not enough points available for this purchase", "error")
            return render_template('booking.html', club=club, competition=competition), 400
        elif placesRequired > int(competition["numberOfPlaces"]):
            flash("Not enough places available for this purchase", "error")
            return render_template('booking.html', club=club, competition=competition), 400
        elif placesRequired > 12:
            flash("You cannot buy more than 12 tickets from the same competition", "error")
            return render_template('booking.html', club=club, competition=competition), 400
        elif datetime.strptime(competition["date"], '%Y-%m-%d %H:%M:%S') < datetime.today():
            flash("Cannot buy places, this book is obsolete, please select one that has not already passed", "error")
            return render_template('welcome.html', club=club, competition=competition), 400
        else:
            competition['numberOfPlaces'] = int(competition['numberOfPlaces']) - placesRequired
            club['points'] = int(club['points']) - placesRequired
            flash('Great-booking complete!', "success")
            return render_template('welcome.html', club=club, competitions=competitions)

    # TODO: Add route for points display

    @app.route('/logout')
    def logout():
        return redirect(url_for('index'))

    return app


app = create_app({"TESTING": False},
                 loadCompetitions(),
                 loadClubs())

if __name__ == "__main__":
    app.run()
