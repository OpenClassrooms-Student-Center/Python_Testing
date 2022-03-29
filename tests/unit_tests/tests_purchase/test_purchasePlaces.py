class TestPurchase:

    def test_should_limit_purchase_to_points_own(self, client, testing_data):
        NB_PLACES = 6
        club = testing_data['clubs'][1]
        competition = testing_data['competitions'][2]
        expected_value = [competition['numberOfPlaces'],
                          club['points'],
                          "Not enough points"
                          ]
        response = client.post('/purchasePlaces',
                               data={'places': NB_PLACES, 'club': club['name'], 'competition': competition[
                                   'name']})
        data = response.data.decode()
        assert competition['numberOfPlaces'] == expected_value[0]
        assert club['points'] == expected_value[1]
        assert expected_value[2] in data
