from server import competition


class TestJson:

    def test_find_club(self, test_club):
        assert test_club[0]["name"] == "Simply Lift"
        assert test_club[0]["email"] == "john@simplylift.co"
        assert test_club[0]["points"] == "2"

    def test_find_competition(self, test_comp):
        assert test_comp[0]["name"] == "Spring Festival"
        assert test_comp[0]["date"] == "2023-03-27 10:00:00"
        assert test_comp[0]["numberOfPlaces"] == "25"


class TestAuth():

    def test_main_page(self, client):
        response = client.get("/")
        assert response.status_code == 200 and \
               b'Welcome to the GUDLFT Registration Portal!' \
               in response.data

    def test_valid_mail(self, client):
        response = client.post('/showSummary', data={'email': 'kate@shelifts.co.uk'})
        assert response.status_code == 200 and \
               b'Summary | GUDLFT Registration' in response.data

    def test_wrong_mail(self, client):
        response = client.post('/showSummary', data={'email': 'jojo@jo.com'})
        assert response.status_code == 200

    def test_logout(self, client):
        response = client.get('/logout', follow_redirects=True)
        assert response.status_code == 200


class TestBook:

    def test_find_only_futur_competition(self):
        expected = [
            {"name": "Spring Festival",
                "date": "2023-03-27 10:00:00",
                "numberOfPlaces": "25"}
            ]
        futur = competition('test_data_comp.json')
        assert futur == expected

    def test_valid__endpoint(self, client):

        endpoint = '/book/Spring Festival/Simply Lift'
        response = client.get(endpoint)
        assert response.status_code == 200 and \
               b'Spring Festival' \
               in response.data

    def test_wrong_endpoint(self, client):
        endpoint = '/book/Fake Competition/Fake Club'
        response = client.get(endpoint)
        assert response.status_code == 200 and \
            b'Something went wrong-please try again' in response.data