import json
from flask import Flask,render_template,request,redirect,flash,url_for


class FlaskWrapper():
    app = Flask(__name__)
    app.secret_key = 'something_special'
    competitions = None
    clubs = None

    def __init__(self, competitions_path = "competitions.json", clubs_path = "clubs.json"):
        FlaskWrapper.competitions = FlaskWrapper.loadCompetitions(competitions_path)
        FlaskWrapper.clubs = FlaskWrapper.loadClubs(clubs_path)

    @staticmethod
    def loadClubs(path: str):
        with open(path) as c:
            listOfClubs = json.load(c)['clubs']
            return listOfClubs

    @staticmethod
    def loadCompetitions(path: str):
        with open(path) as comps:
            listOfCompetitions = json.load(comps)['competitions']
            return listOfCompetitions

    @app.route('/')
    def index():
        return render_template('login.html')

    @app.route('/showSummary',methods=['POST'])
    def showSummary():
        retrieved_clubs = [club for club in FlaskWrapper.clubs if club['email'] == request.form['email']]
        if len(retrieved_clubs) != 0:
            return render_template('welcome.html',club=retrieved_clubs[0],competitions=FlaskWrapper.competitions)
        else:
            return render_template('login.html', errors=["Email not found."])


    @app.route('/book/<competition>/<club>')
    def book(competition,club):
        foundClub = [c for c in FlaskWrapper.clubs if c['name'] == club]
        foundCompetition = [c for c in FlaskWrapper.competitions if c['name'] == competition]
        if len(foundClub) != 0 and len(foundCompetition) != 0:
            return render_template('booking.html',club=foundClub[0],competition=foundCompetition[0])
        else:
            # flash("Something went wrong-please try again")
            return render_template('welcome.html', club=club, competitions=FlaskWrapper.competitions, errors=["Club or competition not found."])


    @app.route('/purchasePlaces',methods=['POST'])
    def purchasePlaces():
        competition = [c for c in FlaskWrapper.competitions if c['name'] == request.form['competition']][0]
        club = [c for c in FlaskWrapper.clubs if c['name'] == request.form['club']][0]
        places_required = int(request.form['places'])
        if places_required > int(club["points"]):
            return render_template("booking.html", competition=competition, club=club, errors=["Club has not enough points."])
        if places_required > int(competition["numberOfPlaces"]):
            return render_template("booking.html", competition=competition, club=club, errors=["Competition has not enough places."])
        if places_required > 12:
            return render_template("booking.html", competition=competition, club=club, errors=["You can't reserve more than 12 places."])
        competition['numberOfPlaces'] = int(competition['numberOfPlaces']) - places_required
        club["points"] = int(club["points"]) - places_required
        flash('Great-booking complete!')
        return render_template('welcome.html', club=club, competitions=FlaskWrapper.competitions)


    # TODO: Add route for points display


    @app.route('/logout')
    def logout():
        return redirect(url_for('index'))


if __name__ != "__main__":
    flask_wrapper = FlaskWrapper()
    app = flask_wrapper.app
