import pytest

@pytest.mark.integration
class TestEmailValidation:
    """Tests d'intégration pour la validation des emails (Issue #1)"""
    
    def test_empty_email_redirects_with_flash(self, client):
        """Test: Email vide affiche message d'erreur"""
        response = client.post('/showSummary', 
                              data={'email': ''}, 
                              follow_redirects=True)
        assert response.status_code == 200
        assert b"Veuillez entrer une adresse e-mail" in response.data
    
    def test_unknown_email_redirects_with_flash(self, client):
        """Test: Email inconnu affiche message d'erreur"""
        response = client.post('/showSummary', 
                              data={'email': 'unknown@test.com'}, 
                              follow_redirects=True)
        assert response.status_code == 200
        assert b"cette adresse e-mail est introuvable" in response.data
    
    def test_valid_email_shows_welcome(self, client):
        """Test: Email valide affiche page welcome"""
        response = client.post('/showSummary', 
                              data={'email': 'john@simplylift.co'})
        assert response.status_code == 200
        assert b"Welcome, john@simplylift.co" in response.data