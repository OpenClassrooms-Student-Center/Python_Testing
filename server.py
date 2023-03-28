from datetime import datetime
from flask import Flask,render_template,request,redirect,flash,url_for
from .tests.utilities import loadClubs, loadCompetitions, loadClubs_test_data, loadCompetitions_test_data, search_club, writerJson, init_db_clubs, init_db_competitions


MAX_INSCRIPTION = 12
NOW = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
NOW_GABARIT = datetime.now().strftime("%Y-%m-%d")

def create_app(config):

    app = Flask(__name__)
    app.secret_key = 'something_special'
    app.config.update(config)

    if app.config['TESTING'] is True:
        init_db_competitions()
        init_db_clubs()
        competitions = loadCompetitions_test_data()
        clubs = loadClubs_test_data()
        test = 'data/'
    else:
        competitions = loadCompetitions()
        clubs = loadClubs()
        test = ''
        

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
            return render_template('welcome.html', club=club, competitions=competitions, date=NOW_GABARIT)
        else:
            flash('invalide email')
            return redirect(url_for('index'))


    @app.route('/book/<competition>/<club>')
    def book(competition,club):
        foundClub = [c for c in clubs if c['name'] == club][0]
        foundCompetition = [c for c in competitions if c['name'] == competition][0]
        if foundClub and foundCompetition:
            return render_template('booking.html',club=foundClub,competition=foundCompetition, date=NOW_GABARIT)
        else:
            flash("Something went wrong-please try again")
            return render_template('welcome.html', club=club, competitions=competitions, date=NOW_GABARIT)


    @app.route('/purchasePlaces',methods=['POST'])
    def purchasePlaces():
    
        competition = [c for c in competitions if c['name'] == request.form['competition']][0]
        club = [c for c in clubs if c['name'] == request.form['club']][0]
        placesRequired = request.form['places']

        if placesRequired != '':
            placesRequired = int(request.form['places'])

        if placesRequired == '':
            flash("You haven't specified a number of places!")
            return render_template('welcome.html', club=club, competitions=competitions, date=NOW_GABARIT)
        
        elif NOW > competition['date']:
            flash("That competition is over!")
            return render_template('welcome.html', club=club, competitions=competitions, date=NOW_GABARIT)
        
        elif placesRequired > 12:
            flash("Book less than 12 places!")
            return render_template('welcome.html', club=club, competitions=competitions, date=NOW_GABARIT)
        
        elif int(club['points']) - placesRequired < 0:
            flash("You don't have enough points!")
            return render_template('welcome.html', club=club, competitions=competitions, date=NOW_GABARIT)
        
        elif int(competition['numberOfPlaces']) - placesRequired < 0:
            flash("Not enough places in the competition!")
            return render_template('welcome.html', club=club, competitions=competitions, date=NOW_GABARIT)
        
        else:

            # update competition points
            competition['numberOfPlaces'] = str(int(competition['numberOfPlaces'])-placesRequired)
            writerJson(competitions, competition, f'{test}competitions_test.json')
            # update club points
            club['points'] = str(int(club['points']) - placesRequired)
            writerJson(clubs, club, f'{test}clubs_test.json')

            flash('Great-booking complete!')
            return render_template('welcome.html', club=club, competitions=competitions, date=NOW_GABARIT)

    @app.route('/publicBoard')
    def board():

        clubs_name = [c['name'] for c in clubs]
        clubs_points = [p['points'] for p in clubs]

        return render_template('publicBoard.html', clubs_name=clubs_name, clubs_points=clubs_points)

    @app.route('/logout')
    def logout():
        return redirect(url_for('index'))
    
    return app

app = create_app({"TESTING": False})
    