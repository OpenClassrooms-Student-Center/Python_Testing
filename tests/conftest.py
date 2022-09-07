import pytest


import server


@pytest.fixture
def client():
    app = server.create_app({"TESTING": True})
    with app.test_client() as client:
        yield client