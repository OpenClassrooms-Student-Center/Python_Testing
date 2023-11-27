import pytest
from datetime import datetime, timedelta
from server import check_if_the_date_has_passed


def test_future_date():
    """
    Test the check_if_the_date_has_passed function for a future date.

    This test checks the behavior of the check_if_the_date_has_passed function
    when provided with a future date (i.e., a date that has not passed yet).

    The expected result is True, indicating that the date is in the future.

    Parameters:
    - date (str): A date string in the format "YYYY-MM-DD HH:MM:SS".
    """
    assert check_if_the_date_has_passed("2025-12-01 12:00:00") is True


def test_near_future_date():
    """
    Test the check_if_the_date_has_passed function for a date in the near
    future.

    This test checks the behavior of the check_if_the_date_has_passed function
    when provided with a date that is in the near future
    (within the next 30 minutes).

    The expected result is True, indicating that the date is in the future.

    Parameters:
    - date (str): A date string in the format "YYYY-MM-DD HH:MM:SS".
    """
    future_date = (datetime.now() + timedelta(minutes=30)).strftime(
        "%Y-%m-%d %H:%M:%S"
    )
    assert check_if_the_date_has_passed(future_date) is True


def test_current_date():
    """
    Test the check_if_the_date_has_passed function for the current date.

    This test checks the behavior of the check_if_the_date_has_passed function
    when provided with the current date and time.

    The expected result is False, indicating that the provided date is not in
    the past.
    """
    current_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    assert check_if_the_date_has_passed(current_date) is False


def test_past_date():
    """
    Test the check_if_the_date_has_passed function for a past date.

    This test checks the behavior of the check_if_the_date_has_passed
    function when provided with a date in the past.

    The expected result is False, indicating that the provided date is not
    in the past.
    """
    past_date = "2020-01-01 00:00:00"
    assert check_if_the_date_has_passed(past_date) is False


def test_near_past_date():
    """
    Test the check_if_the_date_has_passed function for a near past date.

    This test checks the behavior of the check_if_the_date_has_passed function
    when provided with a date in the near past.

    The expected result is False, indicating that the provided date is not in
    the past.
    """
    near_past_date = (datetime.now() - timedelta(minutes=30)).strftime(
        "%Y-%m-%d %H:%M:%S"
    )
    assert check_if_the_date_has_passed(near_past_date) is False


def test_invalid_date_format():
    """
    Test the check_if_the_date_has_passed function with an invalid date format.

    This test checks the behavior of the check_if_the_date_has_passed function
    when provided with an invalid date format.

    The expected result is a ValueError, indicating that the provided date
    format is invalid.
    """
    with pytest.raises(ValueError):
        check_if_the_date_has_passed("invalid date format")
