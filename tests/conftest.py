import pytest
import server

# ============================================= FIXTURES CLIENT TESTING


@pytest.fixture
def client():
    with server.app.test_client() as client:
        yield client


# ================================================== FIXTURE FOR CLUBS TESTING


@pytest.fixture
def clubs_fixture():
    return [
        {
            "name": "Basic lift",
            "email": "john@basiclift.co",
            "points": "15"
        },
        {
            "name": "BeastMaster",
            "email": "admin@beastmaster.com",
            "points": "20"
        },
        {
            "name": "Urban fit",
            "email": "Tom@urbanfit.co.uk",
            "points": "6"
        }
    ]


# ================================================== FIXTURE FOR COMPETITIONS TESTING


@pytest.fixture
def competitions_fixture():
    return [
        {
            "name": "Aka League",
            "date": "2023-02-05 10:00:00",
            "numberOfPlaces": "20"
        },
        {
            "name": "Pink Race",
            "date": "2021-05-12 09:00:00",
            "numberOfPlaces": "4"
        },
        {
            "name": "Champion Road",
            "date": "2023-02-13 13:00:00",
            "numberOfPlaces": "8"
        },
        {
            "name": "Ice Race",
            "date": "2022-12-01 14:00:00",
            "numberOfPlaces": "10"
        }
    ]


# ================================================== FIXTURE TO AVOID BOOKING MORE THAN 12 PLACES


@pytest.fixture
def cart_fixture(competitions_fixture, clubs_fixture):
    return {
        competition["name"]: {club["name"]: 0 for club in clubs_fixture}
        for competition in competitions_fixture
    }


# ================================================== FIXTURE TO AVOID REPETITIONS OF CALLING FIXTURE IN PARAMETERS


@pytest.fixture
def fixture(mocker, clubs_fixture, competitions_fixture, cart_fixture):
    return [mocker, clubs_fixture, competitions_fixture, cart_fixture]


# ================================================== FIXTURE TO AVOID REPETITIONS IN FUNCTIONS TESTING


def get(fixture, case, places=0):
    fixture[0].patch.object(server, 'clubs', fixture[1])
    fixture[0].patch.object(server, 'competitions', fixture[2])
    fixture[0].patch.object(server, 'cart', fixture[3])

    valid_club = fixture[1][0]['name']
    valid_competition = fixture[2][0]['name']

    if case == "email":
        email = fixture[1][0]['email']
        data_email = {'email': email}
        return data_email

    elif case == "wrong_email":
        return {"email": "unknown_email@gmail.com"}

    elif case == "valid_club_competition":
        data_book = {'competition': valid_competition, 'club': valid_club}
        return data_book

    elif case == "club_unknown_competition":
        return {'competition': "Black Race", 'club': valid_club}

    elif case == "club_competition_places":
        data_purchase_places = {'competition': valid_competition, 'club': valid_club, 'places': places}
        return data_purchase_places

    elif case == "small_competition_places":
        small_competition = fixture[2][2]['name']
        data_purchase_places = {'competition': small_competition, 'club': valid_club, 'places': places}
        return data_purchase_places

    elif case == "small_club_places":
        small_club = fixture[1][2]['name']
        data_purchase_places = {'competition': valid_competition, 'club': small_club, 'places': places}
        return data_purchase_places

    elif case == "past_competition_places":
        past_competition = fixture[2][1]['name']
        data_purchase_places = {'competition': past_competition, 'club': valid_club, 'places': places}
        return data_purchase_places

    elif case == "board":
        return fixture[1]

    elif case == "empty_board":
        return fixture[0].patch.object(server, 'clubs', '')


# ================================================== FIXTURE FOR JSON TESTING


EMPTY_JSON_PATH = 'tests/functional/empty.json'
FAKE_PATH_JSON_CLUBS = 'fake_club.json'
FAKE_PATH_JSON_COMPETITIONS = 'fake_comp.json'


def get_empty_json(mocker):
    return mocker.patch.object(
        server, 'PATH_JSON_CLUBS', EMPTY_JSON_PATH), mocker.patch.object(
            server, 'PATH_JSON_COMPETITIONS', EMPTY_JSON_PATH)


def get_wrong_json_path(mocker):
    return mocker.patch.object(server, 'PATH_JSON_CLUBS',
                               FAKE_PATH_JSON_CLUBS), mocker.patch.object(
            server, 'PATH_JSON_COMPETITIONS', FAKE_PATH_JSON_COMPETITIONS)
