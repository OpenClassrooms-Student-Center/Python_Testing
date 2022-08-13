import pytest


def test_should_not_take_more_than_12_places(client):
    
    response = client.post('/purchasePlaces', data = {
        "competition": "Spring Festival",
        "club": "Simply Lift",
        "places": 13
        })
    
    assert response.status_code == 200
    assert 'You cannot take more than 12 places' in response.text


def test_should_not_accept_negative_numbers(client):

    response = client.post('/purchasePlaces', data = {
        "competition": "Spring Festival",
        "club": "Simply Lift",
        "places": -2
        })
    
    assert response.status_code == 200
    assert 'You cannot enter negative number' in response.text


def test_should_raise_error(client):

    response = client.get('book/Futur Competition/Simply Bug')
    assert 'Something went wrong-please try again' in response.text


def test_should_return_200_on_booking(client):

    response = client.get('book/Test Competition/Simply Lift')
    assert response.status_code == 200
    assert 'Test Competition' in response.text
    