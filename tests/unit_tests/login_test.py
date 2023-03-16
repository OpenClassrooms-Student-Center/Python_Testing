CODE_200 = 200
CODE_302 = 302

def test_right_login(client):
	data = {'email':'john@simplylift.co'}
	response = client.post('/showSummary', data=data)
	assert response.status_code == CODE_200

def test_wrong_login(client):
	data = {'email':'wrongmail@gmail.com'}
	response = client.post('/showSummary', data=data)
	assert response.status_code == CODE_302



