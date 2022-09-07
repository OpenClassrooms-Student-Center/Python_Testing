from random import choice
from uuid import uuid4


# ------- FUNCTIONAL TESTS ------------------
def test_unknown_email_login(client):
    """Function that tests login of an unknown email"""

    # GIVEN
    # an unknown_email
    unknown_email = str(uuid4()) + "@domain.com"

    # WHEN
    # login
    response = client.post('/showSummary', data={'email': unknown_email})

    # THEN
    assert response.status_code == 404
    assert "that email wasn't found" in str(response.data)


def test_known_email_login(client, valid_club):
    """Function that tests login of a valid email"""

    # GIVEN
    # an email in club
    known_email = valid_club['email']

    # WHEN
    # login
    response = client.post('/showSummary', data={'email': known_email})

    # THEN
    assert response.status_code == 200
