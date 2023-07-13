from tests.config import client, existent_club, existent_competition, \
    non_existent_club, non_existent_competition
from datetime import datetime


def test_get_detail_book_200(client, existent_competition, existent_club):
    # Success access to book detail (retrieve)
    rv = client.get(
        f"/book/{existent_competition[0]['name']}"
        f"/{existent_club[0]['name']}")
    assert rv.status_code == 200
    data = rv.data.decode()
    assert existent_competition[0]['name'] in data
    assert existent_club[0]['name'] in data


def test_get_detail_book_wrong_club_400(client, existent_competition, non_existent_club):
    # Try to access book detail with wrong club name
    rv = client.get(
        f"/book/{existent_competition[0]['name']}"
        f"/{non_existent_club[0]['name']}")
    assert rv.status_code == 400
    data = rv.data.decode()
    assert "Something went wrong-please try again" in data


def test_get_detail_book_wrong_competition_400(client, non_existent_competition, existent_club):
    # Try to access book detail with wrong competition name
    rv = client.get(
        f"/book/{non_existent_competition[0]['name']}"
        f"/{existent_club[0]['name']}")
    assert rv.status_code == 400
    data = rv.data.decode()
    assert "Something went wrong-please try again" in data


def test_get_detail_book_outdated_400(client, existent_competition, existent_club):
    # Try to access to an outdated book
    rv = client.get(
        f"/book/{existent_competition[2]['name']}"
        f"/{existent_club[0]['name']}")
    assert rv.status_code == 400
    data = rv.data.decode()
    assert "Cannot access on detail, this book is obsolete, please select one that has not already passed" in data