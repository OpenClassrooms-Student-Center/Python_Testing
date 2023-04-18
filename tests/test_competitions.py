import pytest
import server


server.app.config["TESTING"] = True
client = server.app.test_client()


@pytest.fixture
def clubs():
    yield server.clubs

@pytest.fixture
def competitions():
    yield server.competitions


def test_check_club_can_afford_slots(clubs, competitions):
    response = client.post("/purchasePlaces", data={
        'places' : '3',
        'club': clubs[1]['name'],
        'competition': competitions[0]['name'],
    })
    assert response.status_code == 200


def test_check_club_can_buy_too_much_slots(clubs, competitions):
    response = client.post("/purchasePlaces", data={
        'places' : '5',
        'club': clubs[1]['name'],
        'competition': competitions[0]['name'],
    })
    assert response.status_code == 200

def test_check_club_can_afford_more_than_12_slots(clubs, competitions):
    response = client.post("/purchasePlaces", data={
        'places': '13',
        'club': clubs[1]['name'],
        'competition': competitions[0]['name'],
    })
    assert response.status_code == 200


