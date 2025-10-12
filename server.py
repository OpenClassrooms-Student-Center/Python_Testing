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
    # Le rajout de .get évite une erreur si 'email' absent et renvoie None
    email = request.form.get('email')
    if email:
        # si un email est présent, retrait des espaces
        email = email.strip()
    # Si pas d'email fourni, afficher un message et rester sur la page index
    if not email:
        flash("Sorry, that email wasn't found, please try again.")
        return render_template('index.html')
    # Liste en compréhension pour trouver la valeur associée à l'email. Et .get pour éviter une erreur si 'email' absent dans un club dans clubs.json
    email_found = [c for c in clubs if c.get('email', '').strip() == email]
    # print("Email recherché : ", email)
    # print("Résultat de la recherche : ", email_found)
    if not email_found:
        flash("Sorry, that email wasn't found, please try again.")
        return render_template('index.html')
    club = email_found[0]
    # print("Club trouvé : ", club)
    return render_template('welcome.html',club=club,competitions=competitions)


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
    placesRequired = int(request.form['places'])
    competition['numberOfPlaces'] = int(competition['numberOfPlaces'])-placesRequired
    flash('Great-booking complete!')
    return render_template('welcome.html', club=club, competitions=competitions)


# TODO: Add route for points display


@app.route('/logout')
def logout():
    return redirect(url_for('index'))