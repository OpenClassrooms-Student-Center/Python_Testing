from datetime import timedelta, datetime
from unittest.mock import patch
from app.server import app


def test_book_in_a_past_competition():
    past_date = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d %H:%M:%S')

    with app.test_request_context('/showSummary', data={'email': 'john@simplylift.co'}):

        with patch('app.server.competitions', [{"name": "Spring Festival", "date": past_date,
                                                "numberOfPlaces": "25"}]):

            with patch('app.server.request') as mock_request:
                mock_request.form = {'email': 'john@simplylift.co'}

                response = app.test_client().post('/showSummary', data={'email': mock_request.form['email']})

    assert "Book Places" not in response.get_data(as_text=True)