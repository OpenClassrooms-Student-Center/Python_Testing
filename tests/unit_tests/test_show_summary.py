from tests.unit_tests.conftest import client

from tests.unit_tests.conftest import client


class TestShowSummary:

    def test_valid_email_should_return_welcome_page(self, client):
        """
        As we dont have means to assert used templates, we check if our posted email is in response
        """
        valid_email = 'john@simplylift.co'
        response = client.post('/showSummary', data={'email': valid_email})
        assert response.status_code == 200
        assert valid_email in response.data.decode()

    def test_invalid_email_should_return_index_html_with_errorMail(self, client):
        invalid_email = 'errorMail@club.com'
        response = client.post('/showSummary', data={"email": invalid_email})
        assert response.data.decode()
        assert 'message' in response.data.decode()


