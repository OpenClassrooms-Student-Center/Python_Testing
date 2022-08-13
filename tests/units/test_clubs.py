def test_should_buy_actual_competition(client):
    """test for taking places in actual competition"""
    response = client.post('/showSummary', data = {"email": "john@simplylift.co"})
    assert response.status_code == 200
    assert 'The competition Future Competition is already passed' not in response.text


def test_should_not_buy_past_competition(client):
    """test for taking places in past competition"""
    response = client.post('/showSummary', data = {"email": "john@simplylift.co"})
    assert response.status_code == 200
    assert 'The competition Past Competition is already passed' in response.text

