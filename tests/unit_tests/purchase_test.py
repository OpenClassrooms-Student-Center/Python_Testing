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

def test_validation_booking(client, purchaseBase):
	response = client.post('/purchasePlaces', data=purchaseBase)
	message = response.data.decode()
	print("COUCOUUU : ", message)

	assert response.status_code == CODE_200
	assert 'Great-booking complete!' in message

def test_no_points_specified(client, purchaseEmpty):
	response = client.post('/purchasePlaces', data=purchaseEmpty)
	message = html.unescape(response.data.decode())

	assert response.status_code == CODE_200
	assert "You haven't specified a number of places!" in message

def test_less_than_12_points(client, purchaseMore12points):
	response = client.post('/purchasePlaces', data=purchaseMore12points)
	message = html.unescape(response.data.decode())

	assert response.status_code == CODE_200
	assert "Book less than 12 places!" in message

def test_club_not_enough_points(client, purchaseNotEnoughPointsClub):
	response = client.post('/purchasePlaces', data=purchaseNotEnoughPointsClub)
	message = html.unescape(response.data.decode())

	assert response.status_code == CODE_200
	assert "You don't have enough points!" in message


def test_competition_not_enough_points(client, purchaseNotEnoughPointsCompetition):
	response = client.post('/purchasePlaces', data=purchaseNotEnoughPointsCompetition)
	message = html.unescape(response.data.decode())

	print("YESSSS: ", purchaseNotEnoughPointsCompetition)

	assert response.status_code == CODE_200
	assert "Not enough places in the competition!" in message


def test_fixtures(client, patch_clubs):
	response = client.get('/index')
	assert response.status_code == CODE_200
	
	club_lst = json.loads(patch_clubs)
	
