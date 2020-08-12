import pytest
from flask_testing import TestCase
from server import app

class TestLogin(TestCase):
    def create_app(self):
        app.config['TESTING'] = True
        return app

    def test_valid_email_login(self):
        # Test de la page de résumé après la soumission d'une adresse e-mail valide
        response = self.client.post('/showSummary', data={'email': 'john@simplylift.co'})
        self.assert200(response)

    def test_invalid_email_login(self):
        # Test de la page de résumé après la soumission d'une adresse e-mail invalide
        response = self.client.post('/showSummary', data={'email': 'invalid-email'})
        self.assert400(response)

    def test_empty_email_login(self):
        # Test de la page de résumé après la soumission d'une adresse e-mail vide
        response = self.client.post('/showSummary', data={'email': ''})
        self.assert400(response)