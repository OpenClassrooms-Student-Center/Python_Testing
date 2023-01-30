from flask import (
        Flask,
        render_template,
        request,
        redirect,
        flash,
        url_for,
        )

from controllers import controllers

app = Flask(__name__)
app.secret_key = 'something_special'


@app.route('/')
def index():
    return render_template('index.html', clubs=controllers.clubs_list)


@app.route('/showSummary', methods=['POST'])
def showSummary():
    email = controllers.email_found(request, controllers.clubs_list)
    if not email:
        return render_template('index.html',
                               error="Sorry, that email wasn't found.",
                               clubs=controllers.clubs_list)
    club = controllers.email_found(request, controllers.clubs_list)
    return render_template('welcome.html',
                           club=club,
                           competitions=controllers.competitions_list,
                           clubs=controllers.clubs_list)


@app.route('/book/<competition>/<club>')
def book(competition, club):
    club_found = controllers.find_club(club, controllers.clubs_list)
    competition_found = controllers.find_competition(
            competition, controllers.competitions_list)
    if not club_found:
        return render_template('index.html',
                               error="Sorry, that club wasn't found.",
                               clubs=controllers.clubs_list)
    if not competition_found:
        return render_template('index.html',
                               error="Sorry, that competition wasn't found.",
                               clubs=controllers.clubs_list)
    if club_found and competition_found:
        if competition_found['numberOfPlaces'] == '0':
            flash("Sorry, there are no places left for this competition.")
            return render_template('welcome.html',
                                   club=club_found,
                                   clubs=controllers.clubs_list,
                                   competitions=controllers.competitions_list)
        elif competition_found['passed']:
            flash("Sorry, you can't book for this competition as " +
                  "the date has passed.")
            return render_template('welcome.html',
                                   club=club_found,
                                   clubs=controllers.clubs_list,
                                   competitions=controllers.competitions_list)
        elif not competition_found['passed']:
            return render_template('booking.html',
                                   club=club_found,
                                   competition=competition_found)
    else:
        flash("Something went wrong-please try again")
        return render_template('welcome.html',
                               club=club_found,
                               competitions=controllers.competitions_list,
                               clubs=controllers.clubs_list)


@app.route('/purchasePlaces', methods=['POST'])
def purchasePlaces():

    message, page, club = controllers.handle_purchase(
            request, controllers.history_of_reservation,
            controllers.competitions_list, controllers.clubs_list)
    flash(message)
    return render_template(page,
                           club=club,
                           competitions=controllers.competitions_list,
                           clubs=controllers.clubs_list)


@app.route('/logout')
def logout():
    return redirect(url_for('index'))
