from tests.config import client, existent_club, existent_competition


def test_get_board_page_200(client, existent_club):
    # Try and success access to club points board
    rv = client.get("/clubsPointsBoard")
    assert rv.status_code == 200
    data = rv.data.decode()
    for i in range(len(existent_club)):
        assert existent_club[i]["name"], existent_club[i]["points"] in data
