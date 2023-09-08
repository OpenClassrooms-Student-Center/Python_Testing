from http import HTTPStatus


def test_display_board(client):
    response = client.get("/displayBoard")
    assert response.status_code == HTTPStatus.OK
