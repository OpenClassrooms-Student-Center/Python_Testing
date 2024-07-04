import pytest
from server import app
from server import loadClubs, loadCompetitions


def test_loadClubs():
    clubs = loadClubs()
    assert isinstance(clubs, list), "La fonction loadClubs doit renvoyer une liste"
    assert len(clubs) > 0, "La liste des clubs ne doit pas être vide"
    assert 'name' in clubs[0], "Chaque club doit avoir un nom"
    assert 'email' in clubs[0], "Chaque club doit avoir un email"

def test_loadCompetitions():
    competitions = loadCompetitions()
    assert isinstance(competitions, list), "La fonction loadCompetitions doit renvoyer une liste"
    assert len(competitions) > 0, "La liste des compétitions ne doit pas être vide"
    assert 'name' in competitions[0], "Chaque compétition doit avoir un nom"
    assert 'date' in competitions[0], "Chaque compétition doit avoir une date"


# Pour exécuter les tests avec pytest
if __name__ == '__main__':
    pytest.main()