import html

CODE_200 = 200
CODE_302 = 302


def test_logout_ok(client):
    # authentication
    data = {'email': 'john@simplylift.co'}
    response = client.post('/showSummary', data=data)

    assert response.status_code == 200

    # logout
    response = client.get('/logout')
    message = html.unescape(response.data.decode())

    assert 'Redirecting...' in message
    assert response.status_code == 302
