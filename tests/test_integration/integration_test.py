import urllib.parse
import pytest
import html

CODE_200 = 200

# login


@pytest.mark.integtest
def test_right_login(client):
    data = {'email': 'john@simplylift.co'}
    response = client.post('/showSummary', data=data)

    assert response.status_code == CODE_200

# book


@pytest.mark.integtest
def test_booking_right(client, purchaseBase):
    comp_conv = urllib.parse.quote(purchaseBase['competition'])
    club_conv = urllib.parse.quote(purchaseBase['club'])

    response = client.get(f"/book/{comp_conv}/{club_conv}")
    message = html.unescape(response.data.decode())

    assert response.status_code == CODE_200
    assert f'<input type="hidden" name="club" value="{purchaseBase["club"]}">'\
        in message

# purchase


@pytest.mark.integtest
def test_validation_booking(client, purchaseBase):
    """
    Classic test to book places that runs if no contrary condition is raised.
    """
    response = client.post('/purchasePlaces', data=purchaseBase)
    message = html.unescape(response.data.decode())

    assert response.status_code == CODE_200
    assert 'Great-booking complete!' in message

# logout


@pytest.mark.integtest
def test_logout_ok(client):
    response = client.get('/logout')
    message = html.unescape(response.data.decode())

    assert 'Redirecting...' in message
    assert response.status_code == 302
