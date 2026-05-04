import pytest
from server import app


@pytest.fixture
def client():
    # active le mode test de Flask
    app.config["TESTING"] = True
    # crée un faux navigateur
    with app.test_client() as client:
        # donne ce navigateur aux tests
        yield client