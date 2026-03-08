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
    """
    Updates competition places and club points after a successful reservation.

    Method: POST
    Expects: form data containing:
        - 'club': club name from booking form
        - 'competition': competition name from booking form
        - 'places': number of places requested
    Returns: welcome.html with success message if reservation is valid
             welcome.html with error message if competition not found
             redirect to index if club not found
    """
    competition = next((c for c in competitions if c['name'] == request.form['competition']), None)
    club = next((c for c in clubs if c['name'] == request.form['club']), None)

    if not club:
        flash("Something went wrong - please try again.")
        return redirect(url_for('index'))

    if not competition:
        flash("A problem occurred. Please try again.")
        return render_template('welcome.html', club=club, competitions=competitions)

    placesRequired = int(request.form['places'])

    # Validation step for attempts to reserve over 12 places
    if placesRequired > 12:
        flash("The limit for reservations is 12 maximum. Please try again.")
        return render_template('booking.html', club=club, competition=competition)

    # Validation step for reserving more places than points allow
    if placesRequired > int(club['points']):
        flash("You don't have enough points to reserve this many places. Please try again.")
        return render_template('booking.html', club=club, competition=competition)

    competition['numberOfPlaces'] = int(competition['numberOfPlaces'])-placesRequired

    # Update club points in database
    club["points"] = int(club['points'])-placesRequired
    flash('Great-booking complete!')
    return render_template('welcome.html', club=club, competitions=competitions)


# TODO: Add route for points display


@app.route('/logout')
def logout():
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)