import json
from flask import Flask,render_template,request,redirect,flash,url_for
from .tests.utilities import loadClubs, loadCompetitions, loadClubs_test_data, loadCompetitions_test_data, search_club


MAX_INSCRIPTION = 12


def create_app(config):

    app = Flask(__name__)
    app.secret_key = 'something_special'
    app.config.update(config)

    competitions = loadCompetitions()
    clubs = loadClubs()

    if app.config['TESTING'] is True:
        competitions = loadCompetitions_test_data()
        clubs = loadClubs_test_data()

    @app.route('/')
    def index():
        return render_template('index.html')
    
    @app.route('/index')
    def hello():
        '''
        route test
        '''
        return 'Hello, World!'
    
    @app.route('/showSummary',methods=['POST'])
    def showSummary():
        club = search_club(request.form['email'], clubs)
        if club:
            return render_template('welcome.html', club=club, competitions=competitions)
        else:
            flash('invalide email')
            return redirect(url_for('index'))


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
        placesRequired = request.form['places']


        if placesRequired != '':
            placesRequired = int(request.form['places'])

        if placesRequired == '':
            flash("You haven't specified a number of places!")
            return render_template('welcome.html', club=club, competitions=competitions)
        
        elif placesRequired > 12:
            flash("Book less than 12 places!")
            return render_template('welcome.html', club=club, competitions=competitions)
        
        elif int(club['points']) - placesRequired < 0:
            flash("You don't have enough points!")
            return render_template('welcome.html', club=club, competitions=competitions)
        
        elif int(competition['numberOfPlaces']) - placesRequired < 0:
            flash("Not enough places in the competition!")
            return render_template('welcome.html', club=club, competitions=competitions)
        
        else:
            flash('Great-booking complete!')
            return render_template('welcome.html', club=club, competitions=competitions)

    # TODO: Add route for points display

    @app.route('/logout')
    def logout():
        return redirect(url_for('index'))
    
    return app

app = create_app({"TESTING": False})
    