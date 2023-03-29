import html

from ...config import CLUBS_TEST_PATH
from ..utilities import loadClubs

CODE_200 = 200
CODE_302 = 302


def test_informations_for_table_construct(client):
    response = client.get('/publicBoard')
    message = html.unescape(response.data.decode())
    clubs = loadClubs(CLUBS_TEST_PATH)

    assert response.status_code == CODE_200
    for i in clubs:
        assert i['name'] in message
