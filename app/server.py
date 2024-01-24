import json
from datetime import datetime
from flask import Flask,render_template,request,redirect,flash,url_for
from jinja2 import Environment, FileSystemLoader, select_autoescape


def loadClubs():
    with open('clubs.json') as c:
         listOfClubs = json.load(c)['clubs']
         return listOfClubs


def loadCompetitions():
    with open('competitions.json') as comps:
         listOfCompetitions = json.load(comps)['competitions']
         return listOfCompetitions


app = Flask(__name__)
app.secret_key = 'something_special'
app.template_folder = '/home/edward/Documents/Repos/OpenClassRooms/Python_Testing/templates'


competitions = loadCompetitions()
clubs = loadClubs()


env = Environment(
    loader=FileSystemLoader(app.template_folder),
    autoescape=select_autoescape(['html', 'xml'])
)
env.globals['datetime'] = datetime
env.filters['strftime'] = lambda dt, fmt: dt.strftime(fmt) if dt else ''


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/showSummary',methods=['POST'])
def showSummary():
    club_found = [club for club in clubs if club['email'] == request.form['email']]
    if club_found:
        current_time = datetime.now()
        club = [club for club in clubs if club['email'] == request.form['email']][0]
        return render_template('welcome.html', club=club, competitions=competitions, current_time=current_time)
    else:
        flash('No club associated with this email, please try again.')
        return render_template('index.html')


@app.route('/book/<competition>/<club>')
def book(competition,club):
    foundClub = [c for c in clubs if c['name'] == club][0]
    foundCompetition = [c for c in competitions if c['name'] == competition][0]
    if foundClub and foundCompetition:
        return render_template('booking.html', club=foundClub, competition=foundCompetition)
    else:
        flash("Something went wrong-please try again")
        return render_template('welcome.html', club=club, competitions=competitions)


@app.route('/purchasePlaces',methods=['POST'])
def purchasePlaces():
    competition = [c for c in competitions if c['name'] == request.form['competition']][0]
    club = [c for c in clubs if c['name'] == request.form['club']][0]
    places_required = int(request.form['places'])
    club_name = request.form['club']
    current_time = datetime.now()

    if int(club['points']) - places_required < 0:
        flash("You can't book more places than you have!")
        return render_template('welcome.html', club=club, competitions=competitions, current_time=current_time)
    else:
        if competition:
            club_booking = competition.get(club_name, None)

            if club_booking:
                if (competition[club_name] + places_required) <= 12:
                    competition[club_name] += places_required
                    competition['numberOfPlaces'] = int(competition['numberOfPlaces']) - places_required
                    club['points'] = int(club['points']) - places_required
                    flash('Great-booking complete!')
                    return render_template('welcome.html', club=club, competitions=competitions, current_time=current_time)
                else:
                    flash("You can't book more than 12 places by competition")
                    return render_template('welcome.html', club=club, competitions=competitions, current_time=current_time)
            else:
                if places_required <= 12:
                    competition[club_name] = places_required
                    competition['numberOfPlaces'] = int(competition['numberOfPlaces']) - places_required
                    club['points'] = int(club['points']) - places_required
                    flash('Great-booking complete!')
                    return render_template('welcome.html', club=club, competitions=competitions, current_time=current_time)
                else:
                    flash("You can't book more than 12 places by competition")
                    return render_template('welcome.html', club=club, competitions=competitions, current_time=current_time)

        competition['numberOfPlaces'] = int(competition['numberOfPlaces']) - places_required
        club['points'] = int(club['points']) - places_required
        flash('Great-booking complete!')
        return render_template('welcome.html', club=club, competitions=competitions, current_time=current_time)


# TODO: Add route for points display
@app.route('/pointsDisplay')
def pointsDisplay():
    return render_template('points.html', clubs=clubs)


@app.route('/logout')
def logout():
    return redirect(url_for('index'))
