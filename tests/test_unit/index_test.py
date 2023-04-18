import html

CODE_200 = 200


def test_index_return_200(client):
    response = client.get('/')
    message = html.unescape(response.data.decode())

    assert response.status_code == CODE_200
    assert 'Welcome to the GUDLFT Registration Portal!' in message
