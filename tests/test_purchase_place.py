import pytest

def test_purchase_places_success(client, setup_data):
    #TEST can purchase places
    competitions, _ = setup_data
    response = client.post('/purchasePlaces', data={
        'competition': 'Competition 1',
        'club': 'Club A',
        'places': '5'
    })
    
    assert response.status_code == 302
    assert int(competitions[0]['numberOfPlaces']) == 15

def test_cant_purchase_places_not_enough_places(client, setup_data):
    #TEST cant buy if not enough places
    competitions, _ = setup_data
    response = client.post('/purchasePlaces', data={
        'competition': 'Competition 2',
        'club': 'Club A',
        'places': '10'
    })
    
    assert response.status_code == 400
    assert b"Not enough places available." in response.data
    assert int(competitions[1]['numberOfPlaces']) == 5

def test_cant_purchase_places_more_than_12(client, setup_data):
    #TEST cant buy more than 12 places
    competitions, _ = setup_data
    response = client.post('/purchasePlaces', data={
        'competition': 'Competition 1',
        'club': 'Club C',
        'places': '15'
    })
    
    assert response.status_code == 400
    assert int(competitions[0]['numberOfPlaces']) == 20
    assert b"You cannot book more than 12 places per competition." in response.data


def test_cant_purchase_places_not_enough_points(client, setup_data):
    # TEST cant buy if not enough points
    _, clubs = setup_data
    response = client.post('/purchasePlaces', data={
        'competition': 'Competition 1',
        'club': 'Club B',
        'places': '5'
    })
        
    assert response.status_code == 400
    assert int(clubs[1]['points']) == 3
    assert b"Not enough points available." in response.data
