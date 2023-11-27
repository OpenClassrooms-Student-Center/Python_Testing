import pytest
import json
from unittest.mock import mock_open, patch

from server import load_clubs


def test_load_clubs_exists():
    """
    Test the existence of the load_clubs function.

    This test checks if the load_clubs function is defined and callable in
    the current scope.
    """
    assert callable(load_clubs), "load_clubs function not found"


def test_load_clubs_returns_list(clubs):
    """
    Test if the load_clubs function returns a list.

    This test uses a mock_open to simulate reading JSON data from a file
    containing club information.
    It checks if the load_clubs function returns a list when reading and
    parsing the mocked data.

    Args:
    - clubs (fixture): A fixture providing sample club data.
    """
    with patch("builtins.open", mock_open(read_data=json.dumps(clubs))):
        assert isinstance(load_clubs(), list)


def test_load_clubs_returns_expected_data(clubs):
    """
    Test if the load_clubs function returns the expected club data.

    This test uses a mock_open to simulate reading JSON data from a file
    containing club information.
    It checks if the load_clubs function returns the expected list of club
    dictionaries.

    Args:
    - clubs (fixture): A fixture providing sample club data.
    """
    with patch("builtins.open", mock_open(read_data=json.dumps(clubs))):
        assert load_clubs() == [
            {
                "name": "Simply Lift",
                "email": "john@simplylift.co",
                "points": "13",
            },
            {
                "name": "Iron Temple",
                "email": "admin@irontemple.com",
                "points": "4",
            },
            {
                "name": "She Lifts",
                "email": "kate@shelifts.co.uk",
                "points": "12",
            },
        ]


def test_load_clubs_raises_exception_if_invalid_json():
    """
    Test if load_clubs raises an exception when attempting to load invalid
    JSON data.

    This test uses a mock_open to simulate reading invalid JSON data from a
    file.
    It checks if attempting to load clubs with invalid JSON raises an exception
    with the expected error message.
    """
    with patch("builtins.open", mock_open(read_data="{invalid_json}")):
        with pytest.raises(
            Exception,
            match="Expecting property name enclosed in double quotes",
        ):
            load_clubs()


def test_load_clubs_raises_exception_if_invalid_clubs_key(clubs):
    """
    Test if load_clubs raises an exception when attempting to load JSON data
    with an invalid key (expecting 'clubs').

    This test uses a mock_open to simulate reading JSON data with an invalid
    key from a file.
    It checks if attempting to load clubs with JSON data containing an invalid
    key raises an exception with the expected error message.

    Args:
    - clubs: A fixture providing fake clubs data.
    """
    invalid_content = '{"invalid_key": [{"name": "Club1", "points": "10"}]}'

    with patch("builtins.open", mock_open(read_data=invalid_content)):
        with pytest.raises(Exception, match="'clubs'"):
            load_clubs()


def test_load_clubs_raises_exception_if_missing_clubs_key(clubs):
    """
    Test if load_clubs raises an exception when attempting to load JSON data
    with a missing 'clubs' key.

    This test uses a mock_open to simulate reading JSON data with a missing key
    from a file.
    It checks if attempting to load clubs with JSON data containing a missing
    key raises an exception with the expected error message.

    Args:
    - clubs: A fixture providing fake clubs data.
    """
    missing_content = '{"": [{"name": "", "points": ""}]}'

    with patch("builtins.open", mock_open(read_data=missing_content)):
        with pytest.raises(Exception, match="'clubs'"):
            load_clubs()
