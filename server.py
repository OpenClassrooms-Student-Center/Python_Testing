import json
from functools import wraps

from flask import Flask, render_template, request, redirect, flash, url_for, session


def loadClubs():
    with open('clubs.json') as c:
         listOfClubs = json.load(c)['clubs']
         return listOfClubs


def loadCompetitions():
    with open('competitions.json') as comps:
         listOfCompetitions = json.load(comps)['competitions']
         return listOfCompetitions


def get_club_by_email(email):
    """Retourne le club correspondant à un email, ou None si inconnu."""
    matching_clubs = [club for club in clubs if club['email'] == email]
    return matching_clubs[0] if matching_clubs else None


def get_logged_in_club():
    """Lit la session Flask et retourne le club connecté, ou None."""
    email = session.get('club_email')
    if not email:
        return None
    return get_club_by_email(email)


def login_required(view_func):
    """
    Décorateur de protection des routes : vérifie qu'un secrétaire est connecté.
    Si la session est absente, redirige vers la page de connexion.
    Sinon, injecte logged_in_club dans la vue pour éviter de relire la session.
    """
    @wraps(view_func)
    def wrapped_view(*args, **kwargs):
        logged_in_club = get_logged_in_club()
        if not logged_in_club:
            flash('Please log in to access this page.')
            return redirect(url_for('index'))
        return view_func(*args, logged_in_club=logged_in_club, **kwargs)
    return wrapped_view


def require_own_club(club, logged_in_club):
    """
    Vérifie qu'un secrétaire ne réserve que pour son propre club.
    Retourne une redirection en cas d'échec, None sinon.
    """
    if logged_in_club['email'] != club['email']:
        flash('You can only book places for your own club.')
        return redirect(url_for('showSummary'))
    return None


app = Flask(__name__)
app.secret_key = 'something_special'

competitions = loadCompetitions()
clubs = loadClubs()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/showSummary', methods=['GET', 'POST'])
def showSummary():
    if request.method == 'POST':
        # Connexion : vérifie l'email puis enregistre le club en session
        matching_clubs = [club for club in clubs if club['email'] == request.form['email']]
        if not matching_clubs:
            flash('Email not found. Please use a registered secretary email.')
            return redirect(url_for('index'))
        session['club_email'] = matching_clubs[0]['email']
        # POST-redirect-GET : évite de re-soumettre le formulaire au retour arrière
        return redirect(url_for('showSummary'))
    return _render_summary()


@login_required
def _render_summary(logged_in_club):
    """Affiche le tableau de bord du club connecté (route GET /showSummary)."""
    return render_template('welcome.html', club=logged_in_club, competitions=competitions)


# Réservation : accès réservé aux secrétaires connectés (@login_required)
@app.route('/book/<competition>/<club>')
@login_required
def book(competition, club, logged_in_club):
    foundClub = [c for c in clubs if c['name'] == club][0]
    foundCompetition = [c for c in competitions if c['name'] == competition][0]

    redirect_response = require_own_club(foundClub, logged_in_club)
    if redirect_response:
        return redirect_response

    if foundClub and foundCompetition:
        return render_template('booking.html', club=foundClub, competition=foundCompetition)

    flash("Something went wrong-please try again")
    return redirect(url_for('showSummary'))


@app.route('/purchasePlaces', methods=['GET', 'POST'])
def purchasePlaces():
    if request.method == 'GET':
        # Accès direct à l'URL après une réservation (retour arrière / refresh)
        if get_logged_in_club():
            return redirect(url_for('showSummary'))
        flash('Please log in to access this page.')
        return redirect(url_for('index'))
    return _process_purchase()


@login_required
def _process_purchase(logged_in_club):
    """Traite la réservation (route POST /purchasePlaces)."""
    competition = [c for c in competitions if c['name'] == request.form['competition']][0]
    club = [c for c in clubs if c['name'] == request.form['club']][0]

    redirect_response = require_own_club(club, logged_in_club)
    if redirect_response:
        return redirect_response

    placesRequired = int(request.form['places'])
    competition['numberOfPlaces'] = int(competition['numberOfPlaces']) - placesRequired
    flash('Great-booking complete!')
    # POST-redirect-GET : l'URL ne reste plus bloquée sur /purchasePlaces
    return redirect(url_for('showSummary'))


# TODO: Add route for points display


@app.route('/logout')
def logout():
    # Invalide la session côté serveur pour bloquer l'accès aux routes protégées
    session.clear()
    return redirect(url_for('index'))
