from app.server import app

def test_point_diplay():
    with app.test_request_context('/pointsDisplay'):

        response = app.test_client().get('/pointsDisplay')

    assert 'All clubs and their remaining points' in response.get_data(as_text=True)
