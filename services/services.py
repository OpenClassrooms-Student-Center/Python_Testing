from datetime import datetime


def validate_places_request(places_requested):
    MAX_PLACES = 12
    if places_requested < 1 or places_requested > MAX_PLACES:
        return False
    return True

def is_competition_in_future(competition):
    competition_date_str = competition.get('date')
    competition_date = datetime.strptime(competition_date_str, "%Y-%m-%d %H:%M:%S")
    return competition_date > datetime.now()