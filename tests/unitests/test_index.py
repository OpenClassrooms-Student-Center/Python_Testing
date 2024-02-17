import pytest
from server import app
import json



def test_index(client):
    res = client.get('/')
    assert res.status_code == 200



# Pour exécuter les tests avec pytest
if __name__ == '__main__':
    pytest.main()