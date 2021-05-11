import json
from datetime import datetime
from flask import Flask,render_template,request,redirect,flash,url_for
from flask.globals import session


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
        for c in FlaskWrapper.competitions:
            c["is_passed"] = datetime.fromisoformat(c["date"]) < datetime.now() if True else False
        if retrieved_clubs:
            return render_template('welcome.html',club=retrieved_clubs[0],competitions=FlaskWrapper.competitions)
        else:
            return render_template('login.html', errors=["Email not found."])


    @app.route('/book/<competition>/<club>')
    def book(competition,club):
        foundClubs = [c for c in FlaskWrapper.clubs if c['name'] == club]
        foundCompetitions = [c for c in FlaskWrapper.competitions if c['name'] == competition]
        if foundClubs and foundCompetitions:
            if datetime.fromisoformat(foundCompetitions[0]["date"]) < datetime.now():
                flash("Competitions already passed.")
                return render_template("welcome.html", club=foundClubs[0], competitions=FlaskWrapper.competitions)
            else:
                return render_template('booking.html',club=foundClubs[0],competition=foundCompetitions[0])
        else:
            flash("Something went wrong-please try again")
            return render_template('welcome.html', club=club, competitions=FlaskWrapper.competitions, errors=["Club or competition not found."])


    @app.route('/purchasePlaces',methods=['POST'])
    def purchasePlaces():
        competitions = [c for c in FlaskWrapper.competitions if c['name'] == request.form['competition']]
        clubs = [c for c in FlaskWrapper.clubs if c['name'] == request.form['club']]
        if not competitions and not clubs:
            return redirect(url_for("logout"))
        else:
            competition = competitions[0]
            club = clubs[0]
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


    @app.route("/displayboard", methods=["GET"])
    def displayBoard():
        clubs = FlaskWrapper.clubs
        return render_template("display_board.html", clubs=clubs)


    @app.route('/logout', methods=["GET"])
    def logout():
        session.pop("user_email", None)
        return redirect(url_for('index'))


if __name__ != "__main__":
    flask_wrapper = FlaskWrapper()
    app = flask_wrapper.app
