import json
from flask import Flask,render_template,request,redirect,flash,url_for

def search_club(club_email):
    club = [club for club in clubs if club['email'] == club_email]
    if len(club) == 1:
        return club[0]
    else:
        return None


def loadClubs():
    with open('clubs.json') as c:
         listOfClubs = json.load(c)['clubs']
         return listOfClubs


def loadCompetitions():
    with open('competitions.json') as comps:
         listOfCompetitions = json.load(comps)['competitions']
         return listOfCompetitions


competitions = loadCompetitions()
clubs = loadClubs()
MAX_INSCRIPTION = 12


def create_app(config):

    app = Flask(__name__)
    app.secret_key = 'something_special'

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
        club = search_club(request.form['email'])
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
        print('REQUEST server: ', request.form)
        competition = [c for c in competitions if c['name'] == request.form['competition']][0]
        club = [c for c in clubs if c['name'] == request.form['club']][0]

        placesRequired = request.form['places']

        if placesRequired != '':
            placesRequired = int(request.form['places'])

        if placesRequired == '':
            flash("You haven't specified a number of places!")
            return render_template('welcome.html', club=club, competitions=competitions)
        
        elif int(club['points']) - placesRequired < 0:
            flash("You don't have enough points!")
            return render_template('welcome.html', club=club, competitions=competitions)
        
        elif int(competition['numberOfPlaces']) - placesRequired < 0:
            flash("Not enough places in the competition!")
            return render_template('welcome.html', club=club, competitions=competitions)
        
        else:
            # update competition points
            competition['numberOfPlaces'] = int(competition['numberOfPlaces'])-placesRequired
            # update club points
            club['points'] = str(int(club['points']) - placesRequired)

            flash('Great-booking complete!')
            return render_template('welcome.html', club=club, competitions=competitions)


    # TODO: Add route for points display


    @app.route('/logout')
    def logout():
        return redirect(url_for('index'))
    
    return app

app = create_app({"TESTING": False})
    