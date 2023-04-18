import urllib.parse
import jsondiff
import html

from ...config import CLUBS_TEST_PATH, COMPETITIONS_TEST_PATH
from ..utilities import loadClubs, loadCompetitions

CODE_200 = 200
CODE_302 = 302


def test_bookPlaces(client, purchaseBase):
    # login
    data = {'email': 'john@simplylift.co'}
    response = client.post('/showSummary', data=data)

    assert response.status_code == 200

    comp_conv = urllib.parse.quote(purchaseBase['competition'])
    club_conv = urllib.parse.quote(purchaseBase['club'])

    # go booking
    response = client.get(f"/book/{comp_conv}/{club_conv}")
    message = html.unescape(response.data.decode())

    assert response.status_code == CODE_200
    assert f'<input type="hidden" name="club" value="{purchaseBase["club"]}">'\
        in message

    # book places
    data_comp_before_request = loadClubs(CLUBS_TEST_PATH)

    response = client.post('/purchasePlaces', data=purchaseBase)
    message = html.unescape(response.data.decode())

    data_comp_after_request = loadClubs(CLUBS_TEST_PATH)

    diff = jsondiff.diff(data_comp_before_request, data_comp_after_request)

    assert response.status_code == CODE_200
    assert 'Great-booking complete!' in message
    assert diff == {0: {'points': '11'}}

    # logout
    response = client.get('/logout')
    message = html.unescape(response.data.decode())

    assert 'Redirecting...' in message
    assert response.status_code == 302
