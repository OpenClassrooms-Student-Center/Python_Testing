import pytest
# from server import app
from server import *

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


def test_showSummary(client):
    response = client.post('/showSummary', data=dict(email='john@simplylift.co'))
    assert b'<title>Summary | GUDLFT Registration</title>' in response.data


def test_showSummary_unknown_email(client):
    response = client.post('/showSummary', data=dict(email='test@example.com'))
    assert b'<title>GUDLFT Registration</title>' in response.data

def test_purchase_places_exceeding_points(client):
    # load the clubs and competitions data
    clubs = loadClubs()
    competitions = loadCompetitions()

    # find a club and a competition for testing
    club = next(c for c in clubs if c['name'] == 'Simply Lift')
    competition = next(c for c in competitions if c['name'] == 'Spring Festival')

    # count the initial number of points
    initial_points = int(club['points'])

    # try to purchase more places than the club has points
    places_required = initial_points + 10
    response = client.post(
        '/purchasePlaces', 
        data=dict(
            competition=competition['name'],
            club=club['name'],
            places=places_required
        ), 
        follow_redirects=True
    )

    # response should indicate that the purchase was not possible
    assert b'Cannot redeem more points than available' in response.data

    # club's points should not have changed
    assert int(club['points']) == initial_points
