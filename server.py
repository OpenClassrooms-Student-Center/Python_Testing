import json
from flask import Flask,render_template,request,redirect,flash,url_for


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
    club = [club for club in clubs if club['email'] == request.form['email']][0]
    return render_template('welcome.html',club=club,competitions=competitions)


@app.route('/book/<competition>/<club>')
def book(competition,club):
    foundClub = [c for c in clubs if c['name'] == club][0]
    foundCompetition = [c for c in competitions if c['name'] == competition][0]
    if foundClub and foundCompetition:
        return render_template('booking.html', club=foundClub,competition=foundCompetition)
    else:
        flash("Something went wrong-please try again")
        return render_template('welcome.html', club=club, competitions=competitions)


@app.route('/purchasePlaces',methods=['POST'])
def purchasePlaces():
    try:
        competition_name = request.form['competition']
        club_name = request.form['club']
        places_required = int(request.form['places'])

        # Trouver la compétition et le club correspondants dans les listes
        competition = next((c for c in competitions if c['name'] == competition_name), None)
        club = next((c for c in clubs if c['name'] == club_name), None)

        if competition is None or club is None:
            flash("Club or competition not found.")
        elif competition['numberOfPlaces'] < places_required:
            flash("Not enough places available for booking.")
        else:
            # Vérifier si le club a suffisamment de points pour réserver
            if club['points'] >= places_required:
                # Déduire le nombre de places réservées de la compétition
                competition['numberOfPlaces'] -= places_required
                # Déduire les points du club
                club['points'] -= places_required
                flash(f"Booking complete! {places_required} places booked for {competition_name}")
            else:
                flash("Not enough points to make the booking.")

        return render_template('welcome.html', club=club, competitions=competitions)
    except Exception as e:
        flash("An error occurred. Please try again.")
        return redirect(url_for('index'))


# TODO: Add route for points display


@app.route('/logout')
def logout():
    return redirect(url_for('index'))