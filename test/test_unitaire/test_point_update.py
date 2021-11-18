import server
import pytest
import copy


@pytest.fixture
def client():
    server.app.config['TESTING'] = True
    clients = server.app.test_client()
    return clients

def test_club_point_update(client):
    club = server.clubs[1]
    print(club['name'])
    before_points = club["points"]
    competition = server.competitions[0]['name']
    response = client.post('/purchasePlaces',
                           data={
                               'club': club['name'],
                               'competition': competition,
                               'places': 3
                           })
    assert response.status_code == 200
    print(before_points != club['points'])
    assert before_points != club['points']
