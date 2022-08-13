def test_should_return_200_on_board(client):
    response = client.get('/displayBoard')
    assert response.status_code == 200
    assert 'GUDLFT Display Clubs Board !' in response.text