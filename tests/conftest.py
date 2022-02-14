import pytest
from server import create_app, loadClubs, loadCompetitions


@pytest.fixture
def client():
    app = create_app({"TESTING": True})
    with app.test_client() as client:
        yield client


@pytest.fixture
def test_club():
    return loadClubs('test_data_clubs.json')


@pytest.fixture
def test_club_with_enought_points(test_club):
    return test_club[2]


@pytest.fixture
def test_club_with_not_enought_points(test_club):
    return test_club[0]


@pytest.fixture
def test_comp():
    return loadCompetitions('test_data_comp.json')


@pytest.fixture
def past_competition(test_comp):
    return test_comp[1]

@pytest.fixture
def futur_competition():
    return test_comp[0]