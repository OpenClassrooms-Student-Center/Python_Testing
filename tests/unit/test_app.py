from server import app
from server import clubs

def test_showSummary():
    """
        WHEN a secretary logs into the app
        THEN They should be able to see the list of clubs and their associated current points balance
    """

    # Create a test client using the Flask application configured for testing
    with app.test_client() as test_client:
        response = test_client.post('/showSummary', data=dict(email='john@simplylift.co'),follow_redirects=True)
        other_clubs = [other_club for other_club in clubs if not other_club['email'] == 'john@simplylift.co']
        print(response.data.decode('utf8'))
        assert response.status_code == 200
        assert all([club for club in other_clubs if club['points'] in response.data.decode('utf8')])
        assert all([club for club in other_clubs if club['name'] in response.data.decode('utf8')])