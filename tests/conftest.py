import pytest
from server import app

# Création d'une fixture 'client' pour les tests Flask
@pytest.fixture
def client():
    # Utilisation d'un contexte 'with' pour gérer automatiquement la fermeture du client après utilisation
    with app.test_client() as client:
        # Fournit le client de test aux tests qui l'utilisent
        yield client
        # nettoyage apres exe (contrairement à return)