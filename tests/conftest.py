import pytest
import logging

from ..server import create_app

def pytest_configure(config):
    logging.basicConfig(level=logging.INFO)

@pytest.fixture
def client():
    app = create_app({"TESTING": True})
    with app.test_client() as client:
        yield client