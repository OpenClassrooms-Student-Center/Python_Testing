import pytest


@pytest.fixture
def client():
    app = create_app({"TESTING": True, "debug": True})
    with app.test_client() as client:
        yield client
