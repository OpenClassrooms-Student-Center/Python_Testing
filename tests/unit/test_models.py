from models import models


def test_add_date_information_on_competition(competitions):
    """Test the function add_date_information_on_competition."""
    competitions = models.add_date_information_on_competition(competitions)
    assert competitions[0]['date'] == '2023-03-27 10:00:00'
    assert not competitions[0]['passed']
    assert competitions[1]['date'] == '2020-10-22 13:30:00'
    assert competitions[1]['passed']
    assert competitions[2]['date'] == '2023-12-31 10:00:00'
    assert not competitions[2]['passed']
    assert competitions[3]['date'] == '2023-06-30 10:00:00'
    assert not competitions[3]['passed']
