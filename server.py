import json
from flask import Flask,render_template,request,redirect,flash,url_for


def loadClubs():
    """
    Loads the list of clubs from the 'clubs.json' file.

    Returns:
        list: The list of clubs.
    """
    with open('clubs.json') as c:
         listOfClubs = json.load(c)['clubs']
         return listOfClubs


def loadCompetitions():
    """
    Loads the list of competitions from the 'competitions.json' file.

    Returns:
        list: The list of competitions.
    """
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


def getClub(email):
    """Retourne le club correspondant à l'email donné, ou None si non trouvé."""
    for club in clubs:
        if club['email'] == email:
            return club
    return None


@app.route('/showSummary',methods=['POST'])
def showSummary():
    try:
        email = request.form['email']
        club = getClub(email)
        if club:
            return render_template('welcome.html', club=club, competitions=competitions)
        else:
            flash(f"Error: email {email} not found")
            return redirect(url_for('index'))
    except:
        flash(f"Error: email does not exist in the database")
        return redirect(url_for('index'))



# tester qu'est ce qui ce passe quand on passe un club ou une competition qui n'existe pas
@app.route('/book/<competition>/<club>')
def book(competition,club):
    foundClub = [c for c in clubs if c['name'] == club][0]
    foundCompetition = [c for c in competitions if c['name'] == competition][0]
    if foundClub and foundCompetition:
        return render_template('booking.html',club=foundClub,competition=foundCompetition)
    else:
        flash("Something went wrong-please try again")
        return render_template('welcome.html', club=club, competitions=competitions)


# Lorsqu'il achete avec succes que ses points soite bien deduit
# scenario alternative, s'il veut acheter plus de 12 places
    # prevoir une constante globale max à 12 et le renvoyé dans le html via le render template
@app.route('/purchasePlaces',methods=['POST'])
def purchasePlaces():
    competition = [c for c in competitions if c['name'] == request.form['competition']][0]
    club = [c for c in clubs if c['name'] == request.form['club']][0]
    placesRequired = int(request.form['places'])
    competition['numberOfPlaces'] = int(competition['numberOfPlaces'])-placesRequired
    flash('Great-booking complete!')
    return render_template('welcome.html', club=club, competitions=competitions)


# TODO: Add route for points display
# il faut que le tableau de points (bord) soit public par exemple sur la home page
# faire une render template (charger les clubs et les afficher) pour afficher les points
# faire des tests sur cette fonction

@app.route('/logout')
def logout():
    return redirect(url_for('index'))