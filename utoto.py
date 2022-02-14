import pytest



from flask import Flask

def create_app(config):
    app = Flask(__name__)
    app.config.from_object(config)
    @app.route('/index')
    def index():
        return 'Hello, World!'
    return app


@pytest.fixture
def client():
    app = create_app({"TESTING": True})
    with app.test_client() as client:
        yield client


def test_should_status_code_ok(client):
    response = client.get('/index')
    assert response.status_code == 200
