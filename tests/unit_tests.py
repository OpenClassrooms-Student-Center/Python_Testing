from services.services import validate_places_request, is_competition_in_future
from datetime import datetime, timedelta

def test_validate_places_request():
    assert validate_places_request(0) is False
    assert validate_places_request(1) is True
    assert validate_places_request(12) is True
    assert validate_places_request(13) is False


def test_is_competition_in_future_with_future_date():
    future_date = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d %H:%M:%S")
    competition = {"date": future_date}
    assert is_competition_in_future(competition) is True

def test_is_competition_in_future_with_past_date():
    past_date = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d %H:%M:%S")
    competition = {"date": past_date}
    assert is_competition_in_future(competition) is False