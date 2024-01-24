from unittest.mock import patch
from app.server import app

def test_show_summary_with_incorrect_email():
    with app.test_request_context('/showSummary', data={'email': 'incorrect@example.com'}):

        with patch('app.server.request') as mock_request:
            mock_request.form = {'email': 'incorrect@example.com'}

            response = app.test_client().post('/showSummary', data={'email': mock_request.form['email']})

    assert 'No club associated with this email, please try again.' in response.get_data(as_text=True)
