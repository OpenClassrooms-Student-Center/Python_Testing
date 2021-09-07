import server
import pytest


@pytest.fixture()
def client():
    with server.app.test_client() as client:
        yield client