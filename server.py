import json
from flask import Flask, render_template, request, redirect, flash, url_for
from datetime import datetime, timedelta


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

competitions = loadCompetitions()
clubs = loadClubs()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/showSummary',methods=['POST'])
def showSummary():
    club_emails = [club['email'] for club in clubs]
    if request.form['email'] in club_emails:
        club = [club for club in clubs if request.form['email'] == club['email']][0]
        request_club_index = clubs.index(club)
        shadow_club_list = clubs.copy() # copies clubs'list
        shadow_club_list.pop(request_club_index) # extracts connected club to have a
        # list only with other clubs
        return render_template('welcome.html',
                               club=club,
                               competitions=competitions,
                               clubs=shadow_club_list)
    else:
        flash('Email not found - try again!')
        return render_template('index.html')


@app.route('/book/<competition>/<club>')
def book(competition,club):
    foundClub = [c for c in clubs if c['name'] == club][0]
    foundCompetition = [c for c in competitions if c['name'] == competition][0]
    if foundClub and foundCompetition:
        return render_template('booking.html',
                               club=foundClub,
                               competition=foundCompetition)
    else:
        flash("Something went wrong-please try again")
        return render_template('welcome.html',
                               club=club,
                               competitions=competitions)


@app.route('/purchasePlaces',methods=['POST'])
def purchasePlaces():
    competition = [c for c in competitions if c['name'] ==
                   request.form['competition']][0]
    club = [c for c in clubs if c['name'] == request.form['club']][0]
    placesRequired = int(request.form['places'])
    # Get today's date
    present_day = datetime.now()
    tomorrow = present_day + timedelta(1)
    competition_date = datetime.fromisoformat(competition['date'])
    if competition_date < tomorrow:
        flash('too late- booking is closed!')
        return render_template('welcome.html',
                               club=club,
                               competition=competition)
    else:
        if placesRequired <= int(club['points']):
            if placesRequired <= 12:
                competition['numberOfPlaces'] = \
                    int(competition['numberOfPlaces'])-placesRequired
                flash('Great-booking complete!')
                club['points'] = int(club['points'])-placesRequired
                return render_template('welcome.html',
                                       club=club,
                                       competitions=competitions)
            elif placesRequired > 12:
                flash('vous ne pouvez pas réserver plus de 12 places')
                return render_template('booking.html',
                                       club=club,
                                       competition=competition)
        elif placesRequired >= int(club['points']):
            flash('vous n\'avez pas assez de points')
            return render_template('booking.html',
                                   club=club,
                                   competition=competition)


# TODO: Add route for points display


@app.route('/logout')
def logout():
    return redirect(url_for('index'))


if __name__ == "__main__":
    app.run()