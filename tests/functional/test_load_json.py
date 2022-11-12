import pytest
import server
from server import loadClubs, loadCompetitions
from conftest import get_empty_json, get_wrong_json_path


def test_valid_load_json():
    """
        GIVEN a valid json files as database for flask app
        WHEN loadClubs() and loadCompetitions() are called
        THEN all the data is correctly loaded from json files.
    """
    clubs = loadClubs()

    assert clubs is not None
    assert isinstance(clubs, list)
    assert len(clubs) > 0

    competitions = loadCompetitions()

    assert competitions is not None
    assert isinstance(competitions, list)
    assert len(competitions) > 0


def test_with_empty_json(mocker):
    """
        BACK END TESTING :
        GIVEN empty json files as database for flask app
        WHEN loadClubs() and loadCompetitions() are called
        THEN the json file is not found python raise an exception.
    """
    get_empty_json(mocker)

    assert pytest.raises(Exception)
    assert loadClubs() == "This file is empty, or key not found"
    assert loadCompetitions() == "This file is empty, or key not found"


def test_with_wrong_json_path(mocker):
    """
        BACK END TESTING :
        GIVEN wrong path for json files as database for flask app
        WHEN loadClubs() and loadCompetitions() are called
        THEN the json file is not found python raise an exception.
    """
    get_wrong_json_path(mocker)

    assert pytest.raises(Exception)
    assert loadClubs() == "[Errno 2] No such file or directory: 'fake_club.json'"
    assert loadCompetitions() == "[Errno 2] No such file or directory: 'fake_comp.json'"


def test_index_with_empty_data(client, mocker):
    """
        FRONT END TESTING :
        GIVEN JSON files used as database are not loaded
        WHEN connected user go to /index (route of the home page)
        THEN the template 500.html will be rendered with 500 status code.
    """

    mocker.patch.object(server, 'clubs', ''),
    mocker.patch.object(server, 'competitions', '')

    response = client.get('/')
    print(f'{response.status_code}, data reponse = {response.data.decode()}')

    assert response.status_code == 500
    assert b'500 page' in response.data
