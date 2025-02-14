import pytest

def test_booking_page_when_club_not_found(client, setup_data):
    """TEST: The booking page should load when credentials are correct"""
    response = client.get('/book/Competition 5/Club D', follow_redirects=True)

    assert response.status_code == 200
    assert b"Something went wrong - Please try again" in response.data
