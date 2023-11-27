import pytest
import json
from unittest.mock import mock_open, patch

from server import load_competitions


def test_load_competitions_exists():
    """
    Test if the load_competitions function exists.

    This test checks if the load_competitions function is defined and callable.
    """
    assert callable(load_competitions), "load_competitions function not found"


def test_load_competitions_list(competitions):
    """
    Test if the load_competitions function returns a list.

    This test checks if the load_competitions function, when provided with
    mock data, returns a list.

    Args:
    - competitions: Mock data for competitions.
    """
    with patch("builtins.open", mock_open(read_data=json.dumps(competitions))):
        assert isinstance(load_competitions(), list)


def test_load_competitions_returns_expected_data(
    competitions,
):
    """
    Test if the load_competitions function returns the expected data.

    This test checks if the load_competitions function, when provided with
    mock data, returns the expected list of competitions.

    Args:
    - competitions: Mock data for competitions.
    """
    with patch("builtins.open", mock_open(read_data=json.dumps(competitions))):
        competitions_loading = load_competitions()
        assert competitions_loading == [
            {
                "name": "Spring Festival",
                "date": "2024-03-27 10:00:00",
                "numberOfPlaces": "25",
            },
            {
                "name": "Fall Classic",
                "date": "2023-10-22 13:30:00",
                "numberOfPlaces": "13",
            },
        ]


def test_load_competition_raises_exception_if_invalid_json():
    """
    Test if the load_competitions function raises an exception when provided
    with invalid JSON.

    This test checks if the load_competitions function raises an exception
    with a specific error message when it encounters invalid JSON data while
    attempting to load competitions.
    """
    with patch("builtins.open", mock_open(read_data="{invalid_json}")):
        with pytest.raises(
            Exception,
            match="Expecting property name enclosed in double quotes",
        ):
            load_competitions()


def test_load_competitions_raises_exception_if_invalid_competitions_key():
    """
    Test if the load_competitions function raises an exception when the
    'competitions' key is missing.

    This test checks if the load_competitions function raises an exception
    with a specific error message when the loaded JSON data does not contain
    the expected 'competitions' key.
    """
    invalid_content = (
        '{"invalid_key": [{"name": "Competitions1", "numberOfPlaces": "10"}]}'
    )
    with patch("builtins.open", mock_open(read_data=invalid_content)):
        with pytest.raises(Exception, match="'competitions'"):
            load_competitions()


def test_load_competitions_raises_exception_if_missing_competitions_key():
    """
    Test if the load_competitions function raises an exception when the
    'competitions' key is missing.

    This test checks if the load_competitions function raises an exception
    with a specific error message when the loaded JSON data is empty or does
    not contain the expected 'competitions' key.
    """
    missing_content = "{}"
    with patch("builtins.open", mock_open(read_data=missing_content)):
        with pytest.raises(Exception, match="'competitions'"):
            load_competitions()
