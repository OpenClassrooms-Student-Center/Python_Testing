from app.server import app

def test_logout():
    with app.test_request_context('/'):

        response = app.test_client().get('/')

    assert '<h1>Welcome to the GUDLFT Registration Portal!</h1>' in response.get_data(as_text=True)