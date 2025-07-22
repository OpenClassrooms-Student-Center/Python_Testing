def validate_places_request(places_requested):
    MAX_PLACES = 12
    if places_requested < 1 or places_requested > MAX_PLACES:
        return False
    return True