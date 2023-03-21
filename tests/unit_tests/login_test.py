from utilities import disp_log

CODE_200 = 200
CODE_302 = 302

PRINT_LOG = True

def test_right_login(client):
	data = {'email':'john@simplylift.co'}
	response = client.post('/showSummary', data=data)
	assert response.status_code == CODE_200

	if PRINT_LOG:
		disp_log(response.status_code,CODE_200)

def test_wrong_login(client):
	data = {'email':'wrongmail@gmail.com'}
	response = client.post('/showSummary', data=data)
	assert response.status_code == CODE_302

	if PRINT_LOG:
		disp_log(response.status_code,CODE_302)



