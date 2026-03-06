import json
from flask import Flask,render_template,request,redirect,flash,url_for,abort


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
    """
    Looks up club by email submitted via login form and displays club dashboard.

    Method: POST
    Expects: form data containing 'email' key from index.html login form
    Returns: welcome.html with club and competitions data if email is found
             index.html with error message if email is not found
    """
    club = next((club for club in clubs if club['email'] == request.form['email']), None)
    if club:
        return render_template('welcome.html',club=club,competitions=competitions)
    message = "Please enter a valid email address"
    return render_template('index.html', message=message)


@app.route('/book/<competition>/<club>')
def book(competition,club):
    """
    Loads the booking page for a specific club and competition.

    Method: GET
    Expects: Valid club name and competition name as URL parameters
    Returns: booking.html if both club and competition exist in database
             404 if either club or competition name does not match database
    """
    foundClub = next((c for c in clubs if c['name'] == club), None)
    foundCompetition = next((c for c in competitions if c['name'] == competition), None)
    if foundClub and foundCompetition:
        return render_template('booking.html',club=foundClub,competition=foundCompetition)
    else:
        abort(404)


@app.route('/purchasePlaces',methods=['POST'])
def purchasePlaces():
    competition = [c for c in competitions if c['name'] == request.form['competition']][0]
    club = [c for c in clubs if c['name'] == request.form['club']][0]
    placesRequired = int(request.form['places'])
    competition['numberOfPlaces'] = int(competition['numberOfPlaces'])-placesRequired
    flash('Great-booking complete!')
    return render_template('welcome.html', club=club, competitions=competitions)


# TODO: Add route for points display


@app.route('/logout')
def logout():
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)