def test_show_board_route(client, clubs):
    """
    Test if the show_board route renders the board.html template with the
    provided clubs.

    This test case simulates a GET request to the "/board" route,
    checks that the response status code is 200,
    and verifies that the rendered template is "board.html" with the expected
    clubs.

    Args:
    - client: Flask test client.
    - clubs: Fixture providing a list of clubs for testing.
    """
    response = client.get("/board")
    assert response.status_code == 200
    assert response.content_type == "text/html; charset=utf-8"
    assert b"<!DOCTYPE html>" in response.data
    assert b"Welcome to the GUDLFT Board" in response.data
    for club in clubs["clubs"]:
        assert bytes(club["name"], "utf-8") in response.data
