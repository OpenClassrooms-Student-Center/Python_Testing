from app.server import app

def test_logout():
    with app.test_request_context('/logout'):

        response = app.test_client().get('/logout')

    assert '<a href="/">/</a>' in response.get_data(as_text=True)