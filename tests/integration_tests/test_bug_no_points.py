from unittest.mock import patch
from app.server import app

def test_not_allowed_use_more_points():
    with app.test_request_context('/purchasePlaces'):

        with patch('app.server.clubs', [{'name': 'Simply Lift', 'points': '0'}]):

            with patch('app.server.request') as mock_request:
                mock_request.form = {'points': '0', 'competition': 'Spring Festival', 'club': 'Simply Lift',
                                     'places': '25'}

                response = app.test_client().post('/purchasePlaces', data={'points': mock_request.form['points'],
                                                                           'competition': mock_request.form[
                                                                               'competition'],
                                                                           'club': mock_request.form['club'],
                                                                           'places': mock_request.form['places']})

    assert "You can&#39;t book more places than you have!" in response.get_data(as_text=True)
