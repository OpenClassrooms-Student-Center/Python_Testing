import pytest

import server
@pytest.fixture
def app():
    app = server.app
    app.config["TESTING"] = True
    app.secret_key = "testing_secret_key"
    return app
