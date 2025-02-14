import json
from flask import Flask,render_template,request,redirect,flash,url_for

#load the clubs and competitions from the json files
def loadClubs():
    with open('clubs.json') as c:
         listOfClubs = json.load(c)['clubs']
         return listOfClubs

#load the clubs and competitions from the json files
def loadCompetitions():
    with open('competitions.json') as comps:
         listOfCompetitions = json.load(comps)['competitions']
         return listOfCompetitions


app = Flask(__name__) #create the Flask app
app.secret_key = 'something_special' #used to add a session flash

#load the clubs and competitions
competitions = loadCompetitions()
clubs = loadClubs()

@app.route('/')
def index():
    # user can connect from a form (by email)
    return render_template('index.html')

#display welcome page after connextion
@app.route('/show_summary',methods=['POST','GET'])
def show_summary():
    email = request.form.get("email") if request.method == "POST" else request.args.get("email")
    
    if not email:
        flash("Email is required. Please login.", "error")
        return redirect(url_for('index'))

    club = next((club for club in clubs if club['email'] == email), None)
    
    if club:
        return render_template('welcome.html', club=club, competitions=competitions)

    flash("Wrong credentials, please retry", "error")
    return redirect(url_for('index'))

#display the booking page
@app.route('/book/<competition>/<club>', methods=['GET', 'POST'])
def book(competition, club):
    found_club = next((c for c in clubs if c['name'] == club), None)
    found_competition = next((c for c in competitions if c['name'] == competition), None)

    if not found_club or not found_competition:
        flash("Something went wrong - Please try again", "error")
        return redirect(url_for('index'))

    return render_template("booking.html", club=found_club, competition=found_competition)


#purchase places
@app.route('/purchasePlaces', methods=['POST'])
def purchasePlaces():
    competition = next((c for c in competitions if c['name'] == request.form['competition']), None)
    club = next((c for c in clubs if c['name'] == request.form['club']), None)

    if not competition or not club:
        flash("Something went wrong - Please try again", "error")
        return redirect(url_for('index'))

    user_places_required = int(request.form['places'])
    
    if user_places_required <= 0:
        flash("You must book at least one place.", "error")
        return render_template('welcome.html', club=club, competitions=competitions), 400
    elif user_places_required > int(competition['numberOfPlaces']):
        flash("Not enough places available.", "error")
        return render_template('welcome.html', club=club, competitions=competitions), 400
    elif user_places_required > int(club["points"]):
        flash("Not enough points available.", "error")
        return render_template('welcome.html', club=club, competitions=competitions), 400
    elif user_places_required > 12:
        flash("You cannot book more than 12 places per competition.", "error")
        return render_template('welcome.html', club=club, competitions=competitions), 400
    else:
        competition['numberOfPlaces'] = int(competition['numberOfPlaces']) - user_places_required
        club['points'] = int(club['points']) - user_places_required
        flash(f"Great! Booking complete for {user_places_required} places!", "success")
        return redirect(url_for('show_summary', email=club['email']))

    return render_template('welcome.html', club=club, competitions=competitions)

@app.route('/display_points_club', methods=['POST','GET'])
def display_points_club():
    """Affiche les points des clubs et garde le contexte du club connecté"""
    email = request.form.get("email") if request.method == "POST" else request.args.get("email")
    club = next((club for club in clubs if club['email'] == email), None)

    return render_template('display_points_club.html', clubs=clubs, club=club)

@app.route('/logout')
def logout():
    return redirect(url_for('index'))
