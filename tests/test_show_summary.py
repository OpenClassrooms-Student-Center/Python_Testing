import pytest

def test_welcome_page_when_loading_accepted(client, setup_data):
    """TEST: The welcome page should load when credentials are correct"""
    response = client.post('/show_summary', data={'email': 'clubA@example.com'})

    assert response.status_code == 200
    assert b"Welcome" in response.data
    assert b"Competition 1" in response.data

def test_error_when_wrong_credentials(client, setup_data):
    """TEST: Wrong credentials should redirect to index with an error message"""
    response = client.post('/show_summary', data={'email': 'fake@example.com'}, follow_redirects=True)

    assert response.status_code == 200
    assert b"Wrong credentials, please retry" in response.data

def test_error_when_no_email(client, setup_data):
    """TEST: No email inputed should redirect to index with an error message"""
    response = client.post('/show_summary', data={'email': ''}, follow_redirects=True)

    assert response.status_code == 200
    assert b"Email is required. Please login." in response.data
