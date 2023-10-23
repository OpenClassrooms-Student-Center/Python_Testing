import json
from config import DEBUG
from flask import Flask, render_template, request, redirect, flash, url_for


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

if DEBUG:
    app.debug = True

competitions = loadCompetitions()
clubs = loadClubs()

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/showSummary', methods=['POST'])
def showSummary():
    # Récupérer l'adresse e-mail depuis le formulaire, en supprimant les espaces inutiles
    email = request.form.get('email', '').strip()
    
    # Vérification de l'adresse e-mail
    if not email:
        # Si l'adresse e-mail est vide, affichez un message flash et renvoyez un statut HTTP 400 (Mauvaise Requête)
        flash('Veuillez fournir une adresse e-mail.')
        return redirect(url_for('index'), code=400)

    # Recherche du club correspondant à l'adresse e-mail
    club = [club for club in clubs if club['email'] == email]

    if not club:
        # Si le club n'est pas trouvé, affichez un message flash et renvoyez un statut HTTP 400 (Mauvaise Requête)
        flash('Adresse e-mail inconnue. Veuillez vous inscrire.')
        return redirect(url_for('index'), code=400)

    # Si tout est correct, affichez la page de résumé avec les détails du club et des compétitions
    return render_template('welcome.html', club=club[0], competitions=competitions)



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