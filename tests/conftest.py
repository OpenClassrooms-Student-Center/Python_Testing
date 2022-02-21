import pytest
from server import create_app, loadClubs, loadCompetitions


@pytest.fixture
def client():
    app = create_app({"TESTING": True})
    with app.test_client() as client:
        yield client


@pytest.fixture
def test_club():
    return loadClubs('tests/test_data_clubs.json')


@pytest.fixture
def test_comp():
    return loadCompetitions('tests/test_data_comp.json')


@pytest.fixture
def test_valid_data():
    data = {
        'competition': 'Spring Festival',
        'club': 'She Lifts',
        'places': 2,
    }
    return data


@pytest.fixture
def test_not_enought_points():
    data = {
        'competition': 'Spring Festival',
        'club': 'Simply Lift',
        'places': 2,
    }
    return data


@pytest.fixture
def test_not_enought_places():
    data = {
        'competition': 'Test Festival',
        'club': 'She Lifts',
        'places': 5,
    }
    return data
