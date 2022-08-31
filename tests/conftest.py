import pytest

from server import app


@pytest.fixture
def client():
    with app.test_client() as client:
        yield client


@pytest.fixture
def valid_club():
    return {
        "name": "Iron Temple",
        "email": "admin@irontemple.com",
        "points": "4"
    }


@pytest.fixture
def invalid_club():
    return {
        "name": "Invalid club",
        "email": "club@mail.com",
        "points": "13"
    }


@pytest.fixture
def valid_competition():
    return {
        "name": "Spring Festival",
        "date": "2020-03-27 10:00:00",
        "numberOfPlaces": "25"
    }

# def list_competitions():
#     return [
#         {
#             "name": "Spring Festival",
#             "date": "2020-03-27 10:00:00",
#             "numberOfPlaces": "25"
#         },
#         {
#             "name": "Fall Classic",
#             "date": "2020-10-22 13:30:00",
#             "numberOfPlaces": "13"
#         }
#     ]


# @pytest.fixture
# def invalid_competition():
#     return [
#         {
#             "name": "Invalid competition",
#             "date": "2021-11-11 11:11:11",
#             "numberOfPlaces": "10"
#         },
#     ]
