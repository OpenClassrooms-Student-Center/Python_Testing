import json
import pathlib

import pytest

from server import app


@pytest.fixture
def client():
    with app.test_client() as client:
        yield client


@pytest.fixture
def valid_club():
    return {
        "name": "Iron Temple",
        "email": "admin@irontemple.com",
        "points": "4"
    }


@pytest.fixture
def invalid_club():
    return {
        "name": "Invalid club",
        "email": "club@mail.com",
        "points": "13"
    }


@pytest.fixture
def past_competition():
    return {
        "name": "Spring Festival",
        "date": "2020-03-27 10:00:00",
        "numberOfPlaces": "25"
    }


@pytest.fixture
def next_competition():
    return {
        "name": "Winter Tournament",
        "date": "2022-12-12 10:00:00",
        "numberOfPlaces": "24"
    }


@pytest.fixture
def clubs(request):
    file = pathlib.Path(request.node.fspath.strpath)
    config = file.parent.with_name('clubs.json')
    with config.open() as fp:
        return json.load(fp)
