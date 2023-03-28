import html

CODE_200 = 200
CODE_302 = 302

def test_informations_for_table_construct(client):
    response = client.get('/publicBoard')
    message = html.unescape(response.data.decode())

    assert response.status_code == CODE_200
    assert 'club test base' in message
    assert '6' in message