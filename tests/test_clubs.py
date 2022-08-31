def test_show_clubs_template(client):
    response = client.get('/clubs')
    assert response.status_code == 200


def test_display_clubs(client, clubs):
    names = [club["name"] for club in clubs]
    points = [club["points"] for club in clubs]

    response = client.get('/clubs')
    message = response.data.decode()
    assert response.status_code == 200
    for name in names:
        assert name in message
    for point in points:
        assert f"Points: {point}" in message
