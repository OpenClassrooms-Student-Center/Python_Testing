import os.path

import sys
import os

current = os.path.dirname(os.path.realpath(__file__))
test_dir = os.path.dirname(current)
root_dir = os.path.dirname(test_dir)
sys.path.append(test_dir)
sys.path.append(root_dir)

from server import load_clubs


def test_full_use(auth, client, purchase):
    """
    Describe a case use where the user buys two places,
    checks a correctly updated Full Display page and then logs out.
    """
    auth.login()

    response = client.get('/book/Frozen Drops/Simply Lift')
    assert response.status_code == 200
    assert b"Booking for Frozen Drops" in response.data

    response = purchase.purchase()
    db = load_clubs()

    assert response.status_code == 200
    assert b"Points available: 7" in response.data
    assert b"Number of Places: 3" in response.data
    assert db[0]['competitions'][2]['name'] == 'Frozen Drops'

    response = purchase.purchase()
    db = load_clubs()

    assert response.status_code == 200
    assert b"Points available: 1" in response.data
    assert b"Number of Places: 1" in response.data
    assert db[0]['competitions'][2]['places'] == '4'

    response = client.get('/fullDisplay')
    assert response.status_code == 200
    assert b"Simply Lift" in response.data
    assert b"Points: 1" in response.data

    db = load_clubs()

    response = client.get('/logout')
    assert response.status_code == 302
    assert "http://localhost/" == response.headers["Location"]
