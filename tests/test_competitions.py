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


def test_check_club_can_afford_place(clubs, competitions):
    response = client.post("/purchasePlaces", data={
        'places' : '3',
        'club': clubs[1]['name'],
        'competition': competitions[0]['name'],
    })
    assert response.status_code == 200
    assert b"Great-booking complete!"

def test_check_club_cant_reserve_this_place_amount(clubs, competitions):
    response = client.post("/purchasePlaces", data={
        'places' : '5',
        'club': clubs[1]['name'],
        'competition': competitions[0]['name'],
    })
    assert response.status_code == 200
    assert b"your club does not have enough points to affords this."


def test_check_club_cant_afford_more_than_12_place(clubs, competitions):
    response = client.post("/purchasePlaces", data={
        'places': '13',
        'club': clubs[1]['name'],
        'competition': competitions[0]['name'],
    })
    assert response.status_code == 200
    assert b"You cannot reserve more than 12 places"


