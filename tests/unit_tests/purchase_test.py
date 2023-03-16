"""
Tester que les points d'un club ne descende jamais en dessous de zero
Tester que les points des compétitions ne descende jamais en dessous de zero
Tester que lke club a assez de points
tester que la compet a assez de points
Tester que chaques requetes me renvoi un code 200
"""
import os
import json
import html

CODE_200 = 200
CODE_302 = 302

def test_validation_booking(client, purchaseRequest):
	response = client.post('/purchasePlaces', data=purchaseRequest)
	message = response.data.decode()

	assert response.status_code == CODE_200
	assert 'Great-booking complete!' in message

def test_no_points_specified(client, purchaseNoPointSpecified):
	response = client.post('/purchasePlaces', data=purchaseNoPointSpecified)
	message = html.unescape(response.data.decode())

	assert response.status_code == CODE_200
	assert "You haven't specified a number of places!" in message

def test_club_not_enough_points(client, purchaseMorePointThanClub):
	response = client.post('/purchasePlaces', data=purchaseMorePointThanClub)
	message = html.unescape(response.data.decode())

	assert response.status_code == CODE_200
	assert "You don't have enough points!" in message


def test_competition_not_enough_points(client, purchaseMorePointThanCompetition):
	response = client.post('/purchasePlaces', data=purchaseMorePointThanCompetition)
	message = html.unescape(response.data.decode())

	assert response.status_code == CODE_200
	assert "Not enough places in the competition!" in message


def test_fixtures(client, patch_clubs):
	response = client.get('/index')
	assert response.status_code == CODE_200
	
	club_lst = json.loads(patch_clubs)
	
