from models import models

clubs_list = models.load_clubs()
competitions_list = models.load_competitions()
history_of_reservation = []


def get_number_of_place_reserved_for_competition(competition_name, club_name,
                                                 history_of_reservation):
    """Return the number of places reserved for a competition."""
    number_of_place_reserved = 0
    for reservation in history_of_reservation:
        if (reservation['competition'] == competition_name and
                reservation['club'] == club_name):
            number_of_place_reserved += reservation['number_of_places']
    return number_of_place_reserved


def email_found(request, clubs_list):
    """Return True if the email is found."""
    club_email = request.form['email']
    for club in clubs_list:
        if club['email'] == club_email:
            return club
    return False


def find_club(club_name, clubs_list):
    """Return the club if the club exists."""
    for club in clubs_list:
        if club['name'] == club_name:
            return club
    return False


def find_competition(competition_name, competitions_list):
    """Return the competition if the competition exists."""
    for competition in competitions_list:
        if competition['name'] == competition_name:
            return competition
    return False


def remove_points_from_competition(competition,
                                   competitions_list,
                                   points_to_remove):
    """Remove points from a competition."""
    index = competitions_list.index(competition)
    competition['numberOfPlaces'] = str(int(
        competition['numberOfPlaces'])-points_to_remove)
    competitions_list.pop(index)
    competitions_list.insert(index, competition)
    return competitions_list


def remove_points_from_club(club, clubs_list, points_to_remove):
    """Remove points from a club."""
    index = clubs_list.index(club)
    club['points'] = str(int(club['points'])-points_to_remove)
    clubs_list.pop(index)
    clubs_list.insert(index, club)
    return clubs_list


def verify_user_input(request, clubs_list, competitions_list):
    """Sanitize user post."""
    competition = find_competition(
            request.form['competition'], competitions_list)
    club = find_club(request.form['club'], clubs_list)
    try:
        places_required = int(request.form['places'])
        if places_required < 1:
            raise CannotBookLessThanOnePlace
    except ValueError:
        raise ValueError
    if not competition or not club or not places_required:
        raise ValueMissing
    else:
        return competition, club, places_required


def club_has_enough_points(club, places_required):
    """Verify the club has enough points to book."""
    if places_required > int(club['points']):
        return False
    else:
        return True


def club_wants_more_than_twelve_places(places_required, already_reserved):
    """Verify the club wants to book more than 12 places."""
    if (places_required + already_reserved) > 12:
        return True
    else:
        return False


def club_wants_more_than_available_places(places_required, competition):
    """Verify the club wants to book more than available places."""
    if places_required > int(competition['numberOfPlaces']):
        return True
    else:
        return False


class BookMoreThanTwelvePlaces(Exception):
    """Exception raised when a club wants to book more than 12 places."""
    pass


class BookMoreThanAvailablePlaces(Exception):
    """Exception raised when a club wants to book
    more than available places."""
    pass


class NotEnoughPoints(Exception):
    """Exception raised when a club has not enough points."""
    pass


class ValueMissing(Exception):
    """Exception raised when a value is missing."""
    pass


class CannotBookLessThanOnePlace(Exception):
    """Exception raised when a club wants to book less than 1 place."""
    pass


class CompetitionPassed(Exception):
    """Exception raised when a competition has passed."""
    pass


def verify_club_can_book(competition, club, places_required, already_reserved):
    """Verify the club can book."""
    if not club_has_enough_points(club, places_required):
        raise NotEnoughPoints

    elif club_wants_more_than_twelve_places(places_required, already_reserved):
        raise BookMoreThanTwelvePlaces

    elif club_wants_more_than_available_places(places_required, competition):
        raise BookMoreThanAvailablePlaces

    elif competition['passed']:
        raise CompetitionPassed

    else:
        return (True, 'Great-booking complete!', 'welcome.html')


def add_reservation_to_history(competition, club, places_required,
                               history_of_reservation):
    """Add reservation to history."""
    history_of_reservation.append({
        'competition': competition['name'],
        'club': club['name'],
        'number_of_places': places_required
    })


def handle_purchase(request, history_of_reservation, competitions_list,
                    clubs_list):
    """Handle the purchase process."""
    try:
        competition, club, places_required = verify_user_input(
                request, clubs_list, competitions_list)
    except CannotBookLessThanOnePlace:
        message = "You can't book less than 1 place."
        page = 'index.html'
        club = ''
        return message, page, club
    except ValueMissing:
        message = 'Please fill all the fields.'
        page = 'index.html'
        club = ''
        return message, page, club
    except ValueError:
        message = 'Please enter a number for the number of places.'
        page = 'index.html'
        club = ''
        return message, page, club

    alreadyReserved = get_number_of_place_reserved_for_competition(
            competition['name'], club['name'], history_of_reservation)

    try:
        verify_club_can_book(
            competition, club, places_required,
            alreadyReserved)

        remove_points_from_competition(
                competition, competitions_list, places_required)

        remove_points_from_club(club, clubs_list, places_required)

        add_reservation_to_history(competition, club, places_required,
                                   history_of_reservation)

        message = f'Congratulation for booking {places_required} places !'
        page = 'welcome.html'

    except NotEnoughPoints:
        message = ("You don't have enough points"
                   f" to book {places_required} places.")
        page = 'welcome.html'
        return message, page, club

    except BookMoreThanTwelvePlaces:
        message = ("You can only book 12 places per competition.")
        page = 'welcome.html'
        return message, page, club

    except BookMoreThanAvailablePlaces:
        message = ("Sorry, you can't book for this competition as there "
                   "are not enough places.")
        page = 'welcome.html'
        return message, page, club

    except CompetitionPassed:
        message = ("Sorry, you can't book for this competition "
                   "as the date has passed.")
        page = 'welcome.html'
        return message, page, club

    return message, page, club
