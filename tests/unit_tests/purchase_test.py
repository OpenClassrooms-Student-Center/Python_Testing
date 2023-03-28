from datetime import datetime
from ..utilities import retrieveDateCompetition, loadCompetitions_test_data, loadClubs_test_data
import jsondiff
import html

CODE_200 = 200
CODE_302 = 302

NOW = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def test_validation_booking(client, purchaseBase):
	"""
	Classic test to book places that runs if no contrary condition is raised.
	"""
	response = client.post('/purchasePlaces', data=purchaseBase)
	message = html.unescape(response.data.decode())

	assert response.status_code == CODE_200
	assert 'Great-booking complete!' in message

def test_no_points_specified(client, purchaseEmpty):
	"""
	Test if no value is entered in the field
	"""
	response = client.post('/purchasePlaces', data=purchaseEmpty)
	message = html.unescape(response.data.decode())

	assert response.status_code == CODE_200
	assert "You haven't specified a number of places!" in message

def test_less_than_12_points(client, purchase12points):
	"""
	Test if the booked places are over 12
	"""
	response = client.post('/purchasePlaces', data=purchase12points)
	message = html.unescape(response.data.decode())

	assert response.status_code == CODE_200
	assert "Book less than 12 places!" in message

def test_club_not_enough_points(client, purchaseNotEnoughPointsClub):
	"""
	Test if the club have enough points for booking places
	"""
	response = client.post('/purchasePlaces', data=purchaseNotEnoughPointsClub)
	message = html.unescape(response.data.decode())

	assert response.status_code == CODE_200
	assert "You don't have enough points!" in message


def test_competition_not_enough_points(client, purchaseNotEnoughPointsCompetition):
	"""
	Test if the competition have enough points for booking
	"""
	response = client.post('/purchasePlaces', data=purchaseNotEnoughPointsCompetition)
	message = html.unescape(response.data.decode())

	assert response.status_code == CODE_200
	assert "Not enough places in the competition!" in message

def test_competition_not_over(client, purchaseBase):
	"""
	Test if the competition is not finish
	"""
	response = client.post('/purchasePlaces', data=purchaseBase)
	message = html.unescape(response.data.decode())

	assert response.status_code == 200
	assert 'Great-booking complete!' in message
	assert NOW < retrieveDateCompetition(purchaseBase['competition'])

def test_competition_is_over(client, dateIsOver):
	"""
	Test if the competition is finish
	"""
	response = client.post('/purchasePlaces', data=dateIsOver)
	message = html.unescape(response.data.decode())

	assert response.status_code == 200
	assert "That competition is over!" in message
	assert NOW > retrieveDateCompetition(dateIsOver['competition'])

def test_json_club_points_removal(client, purchaseBase):
	"""
	Test if the points have change in the json file 'clubs_test'
	"""
	data_clubs_before_request = loadClubs_test_data()

	response = client.post('/purchasePlaces', data=purchaseBase)
	message = html.unescape(response.data.decode())

	data_clubs_after_request = loadClubs_test_data()

	diff = jsondiff.diff(data_clubs_before_request, data_clubs_after_request)

	assert response.status_code == CODE_200
	assert 'Great-booking complete!' in message
	assert diff == {0: {'points': '2'}}

def test_json_competition_points_removal(client, purchaseBase):
	"""
	Test if the points have change in the json file 'competitions_test'
	"""
	data_comp_before_request = loadCompetitions_test_data()
	
	response = client.post('/purchasePlaces', data=purchaseBase)
	message = html.unescape(response.data.decode())

	data_comp_after_request = loadCompetitions_test_data()

	diff = jsondiff.diff(data_comp_before_request, data_comp_after_request)

	assert response.status_code == CODE_200
	assert 'Great-booking complete!' in message
	assert diff == {0: {'numberOfPlaces': '13'}}

def test_fixtures(client):
	response = client.get('/index')
	assert response.status_code == CODE_200
