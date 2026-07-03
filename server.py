import json
from datetime import datetime
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


COMPETITION_DATE_FORMAT = '%Y-%m-%d %H:%M:%S'


def is_competition_upcoming(competition):
    """Retourne True si la compétition n'a pas encore eu lieu."""
    competition_date = datetime.strptime(competition['date'], COMPETITION_DATE_FORMAT)
    return competition_date > datetime.now()


def get_upcoming_competitions():
    """Retourne uniquement les compétitions à venir (Phase 1)."""
    return [competition for competition in competitions if is_competition_upcoming(competition)]


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


MAX_PLACES_PER_CLUB = 12

# Places déjà réservées par couple (club, compétition) — suivi cumulé en mémoire
club_competition_bookings = {}


def get_places_already_booked(club, competition):
    """Retourne le nombre de places déjà réservées par un club pour une compétition."""
    booking_key = (club['name'], competition['name'])
    return club_competition_bookings.get(booking_key, 0)


def record_purchase(club, competition, places):
    """Enregistre une réservation dans le compteur cumulé."""
    booking_key = (club['name'], competition['name'])
    club_competition_bookings[booking_key] = get_places_already_booked(club, competition) + places


def validate_purchase(club, competition, places_required):
    """
    Vérifie les règles métier avant une réservation.
    Retourne un message d'erreur, ou None si la réservation est valide.
    """
    if places_required <= 0:
        return 'Number of places must be at least 1.'

    if not is_competition_upcoming(competition):
        return 'This competition has already taken place.'

    if places_required > MAX_PLACES_PER_CLUB:
        return f'Cannot book more than {MAX_PLACES_PER_CLUB} places per competition.'

    already_booked = get_places_already_booked(club, competition)
    if already_booked + places_required > MAX_PLACES_PER_CLUB:
        remaining_allowed = MAX_PLACES_PER_CLUB - already_booked
        if remaining_allowed <= 0:
            return (
                f'Cannot book more than {MAX_PLACES_PER_CLUB} places per competition '
                f'for your club.'
            )
        return (
            f'Cannot book more than {MAX_PLACES_PER_CLUB} places per competition. '
            f'You already have {already_booked}, you can only book {remaining_allowed} more.'
        )

    available_places = int(competition['numberOfPlaces'])
    if available_places <= 0:
        return 'Competition is full.'
    if places_required > available_places:
        return f'Not enough places available. Only {available_places} remaining.'

    club_points = int(club['points'])
    if places_required > club_points:
        return 'Not enough points available.'

    return None


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
    return render_template(
        'welcome.html',
        club=logged_in_club,
        competitions=get_upcoming_competitions(),
    )


# Réservation : accès réservé aux secrétaires connectés (@login_required)
@app.route('/book/<competition>/<club>')
@login_required
def book(competition, club, logged_in_club):
    foundClub = [c for c in clubs if c['name'] == club][0]
    foundCompetition = [c for c in competitions if c['name'] == competition][0]

    redirect_response = require_own_club(foundClub, logged_in_club)
    if redirect_response:
        return redirect_response

    if not is_competition_upcoming(foundCompetition):
        flash('This competition has already taken place.')
        return redirect(url_for('showSummary'))

    if foundClub and foundCompetition:
        already_booked = get_places_already_booked(foundClub, foundCompetition)
        max_places = min(
            MAX_PLACES_PER_CLUB - already_booked,
            int(foundCompetition['numberOfPlaces']),
            int(foundClub['points']),
        )
        if max_places <= 0:
            flash(
                f'Cannot book more than {MAX_PLACES_PER_CLUB} places per competition '
                f'for your club.'
            )
            return redirect(url_for('showSummary'))
        return render_template(
            'booking.html',
            club=foundClub,
            competition=foundCompetition,
            max_places=max_places,
            already_booked=already_booked,
        )

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

    try:
        placesRequired = int(request.form['places'])
    except (ValueError, TypeError, KeyError):
        flash('Invalid number of places.')
        return redirect(url_for('showSummary'))

    error_message = validate_purchase(club, competition, placesRequired)
    if error_message:
        flash(error_message)
        return redirect(url_for('showSummary'))

    # Déduction des places et des points (1 point = 1 place)
    competition['numberOfPlaces'] = str(int(competition['numberOfPlaces']) - placesRequired)
    club['points'] = str(int(club['points']) - placesRequired)
    record_purchase(club, competition, placesRequired)
    flash(f'Great-booking complete! {placesRequired} places purchased.')
    # POST-redirect-GET : l'URL ne reste plus bloquée sur /purchasePlaces
    return redirect(url_for('showSummary'))


# TODO: Add route for points display


@app.route('/logout')
def logout():
    # Invalide la session côté serveur pour bloquer l'accès aux routes protégées
    session.clear()
    return redirect(url_for('index'))
