import pytest
from conftest import get


def test_login_with_known_email(client, fixture):
    """
        GIVEN a user not connected
        WHEN a user types in an email found in the system
        THEN this user is successfully connected
    """
    email = get(fixture, "email")
    response = client.post('/showSummary', data=email)
    assert response.status_code == 200


def test_login_with_unknown_email(client, fixture):
    """
        GIVEN a not connected user
        WHEN a user types in an email which is not found in the system
        THEN the error is caught and handled with error message
    """
    email = get(fixture, "wrong_email")
    response = client.post('/showSummary', data=email)
    assert response.status_code == 302
    with pytest.raises(Exception) as exc_info:
        assert str(exc_info.value) == "Sorry, this email wasn't found. Please try again with a correct email !!"
