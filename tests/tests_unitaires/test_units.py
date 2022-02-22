from server import competition


class TestJson:

    def test_find_club(self, test_club):
        assert test_club[0]["name"] == "Simply Lift"
        assert test_club[0]["email"] == "john@simplylift.co"
        assert test_club[0]["points"] == "2"

    def test_find_competition(self, test_comp):
        assert test_comp[0]["name"] == "Spring Festival"
        assert test_comp[0]["date"] == "2023-03-27 10:00:00"
        assert test_comp[0]["numberOfPlaces"] == "45"


class TestAuth():

    def test_main_page(self, client):
        response = client.get("/")
        assert response.status_code == 200 and \
               b'Welcome to the GUDLFT Registration Portal!' \
               in response.data

    def test_valid_mail(self, client):
        response = client.post('/showSummary',
                               data={'email': 'kate@shelifts.co.uk'})
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
                "numberOfPlaces": "45"},
            {"name": "Test Festival",
             "date": "2023-03-27 10:00:00",
             "numberOfPlaces": "2"}
            ]
        futur = competition('tests/test_data_comp.json')
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


class TestPurchasesPlace():

    def test_registration_competition(self, client, test_valid_data):
        response = client.post('/purchasePlaces', data=test_valid_data)
        assert response.status_code == 200 and \
            b'Great-booking complete!' in response.data

    def test_registration_competition_place_limited(self,
                                                    client,
                                                    test_valid_data):
        test_valid_data['places'] = 13
        response = client.post('/purchasePlaces', data=test_valid_data)
        assert response.status_code == 200 and \
               b'you cannot book more than 12 places' in response.data

    def test_purchase_not_enought_points(self,
                                         client,
                                         test_not_enought_points):
        response = client.post('/purchasePlaces', data=test_not_enought_points)
        assert response.status_code == 200 and \
               b"you dont have enough points !" in response.data

    def test_purchase_not_enought_places(self,
                                         client,
                                         test_not_enought_places):
        response = client.post('/purchasePlaces', data=test_not_enought_places)
        assert response.status_code == 200 and \
               b'not enought places !' in response.data
