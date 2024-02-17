import pytest
from server import loadClubs

class TestServer(TestCase):

    def test_loadClubs(self):
        clubs = loadClubs()
        assert isinstance(clubs, list)
        assert len(clubs) > 0

# Pour exécuter les tests avec pytest
if __name__ == '__main__':
    pytest.main()