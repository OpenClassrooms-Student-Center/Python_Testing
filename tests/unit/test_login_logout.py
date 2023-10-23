from flask_testing import TestCase
from server import app


class MyTest(TestCase):
    def create_app(self):
        app.config['TESTING'] = True
        return app

    def test_login_logout(self):
        # Test de la page d'accueil
        response = self.client.get('/')
        self.assert200(response)

        # Test de la page de résumé après la soumission du formulaire
        response = self.client.post('/showSummary', data={'email': 'john@simplylift.co'})
        self.assert200(response)

        # Test de la page de logout
        response = self.client.get('/logout')
        self.assertRedirects(response, '/')