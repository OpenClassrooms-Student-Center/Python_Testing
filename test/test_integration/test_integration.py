import server
import pytest
import copy


@pytest.fixture
def client():
    server.app.config["TESTING"] = True
    clients = server.app.test_client()
    return clients


def test_purchase_place(client):
    competition_list = server.loadCompetitions()
    club_list = server.loadClubs()
    assert len(club_list) == 3
    assert len(competition_list) == 2

    result_login = client.post("/showSummary",
                               data={
                                   "email": "john@simplylift.co"
                               })
    assert result_login.status_code == 200

    club = server.clubs[0]
    competition = server.competitions[0]

    before_point = club["points"]
    result_purchase_place = client.post("/purchasePlaces",
                                        data={
                                            "club": club["name"],
                                            "competition": competition["name"],
                                            "places": 10
                                        })
    assert result_purchase_place.status_code == 200
    assert club["points"] != before_point

    result_logout = client.get('/logout')
    assert result_logout.status_code == 302
