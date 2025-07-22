from services.services import validate_places_request

def test_validate_places_request():
    assert validate_places_request(0) is False
    assert validate_places_request(1) is True
    assert validate_places_request(12) is True
    assert validate_places_request(13) is False