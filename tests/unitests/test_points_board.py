import pytest
import server


# Utilisez les fixtures définies dans conftest.py
@pytest.mark.usefixtures("client", "clubs")

def test_points_board(client, monkeypatch, clubs):
    
    # Mock the loadClubs function - Monkeypatching pour simuler les données de club
    def patch_loadClubs():
        """Mock loadClubs() function"""
        return clubs
    
    monkeypatch.setattr(server, "loadClubs", patch_loadClubs)

    # Effectuer une demande GET à l'URL /pointsBoard
    response = client.get('/pointsBoard')
   
    # Vérifier que la réponse est un succès (code de statut 200)
    assert response.status_code == 200
    
    # Vérifier que le contenu de la page contient le nom du club
    assert b"Simply Lift" in response.data
    assert b"Iron Temple" in response.data

    # Vérifier que le contenu de la page contient les points du club
    # assert b"13" in response.data
    # assert b"20" in response.data
    



    
