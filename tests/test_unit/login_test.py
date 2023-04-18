import html

from ...config import COMPETITIONS_TEST_PATH
from ..utilities import loadCompetitions

CODE_200 = 200
CODE_302 = 302


def test_right_login(client):
    data = {'email': 'john@simplylift.co'}
    response = client.post('/showSummary', data=data)
    message = html.unescape(response.data.decode())
    comps = loadCompetitions(COMPETITIONS_TEST_PATH)

    assert response.status_code == CODE_200

    for i in comps:
        assert i['name'] in message


def test_wrong_login(client):
    data = {'email': 'wrongadmin@irontemple.com'}
    response = client.post('/showSummary', data=data)

    assert response.status_code == CODE_302
