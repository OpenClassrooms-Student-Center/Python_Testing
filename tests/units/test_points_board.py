from conftest import get


def test_display_points_board(client, fixture):
    """
        GIVEN any user,
        WHEN he/she goes to '/board',
        THEN a board will display with all clubs and their points.
    """
    clubs = get(fixture, "board")
    response = client.get('/board')
    for club in clubs:
        assert club['name'] in response.data.decode()
        assert str(club["points"]) in response.data.decode()


def test_board_with_empty_data(client, fixture):
    """
        GIVEN any user,
        WHEN he/she goes to '/board' with GET method & no data return,
        THEN an error message will display.
    """
    get(fixture, "empty_board")
    response = client.get('/board')
    assert b'Sorry, this section has no clubs to display' in response.data
