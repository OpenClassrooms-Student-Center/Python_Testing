class TestPurchase:

    def test_should_return_error_message_on_past_competition(self, client, testing_data):
        NB_PLACES = 6
        club = testing_data['clubs'][3]
        competition = testing_data['competitions'][0]
        expected_value = [competition['numberOfPlaces'],
                          club['points'],
                          'You cannot book for a past competiton'
                          ]
        response = client.post('/purchasePlaces',
                               data={'places': NB_PLACES, 'club': club['name'], 'competition': competition[
                                   'name']})
        data = response.data.decode()
        assert competition['numberOfPlaces'] == expected_value[0]
        assert club['points'] == expected_value[1]
        assert expected_value[2] in data

    def test_should_update_points_and_places_left(self, client, testing_data):
        NB_PLACES = 6
        club = testing_data['clubs'][3]
        competition = testing_data['competitions'][2]
        expected_value = [int(competition['numberOfPlaces'])-NB_PLACES,
                          int(club['points'])-NB_PLACES,
                          'Great-booking complete!'
                          ]
        response = client.post('/purchasePlaces', data={'places': NB_PLACES, 'club': club['name'], 'competition': competition[
            'name']})
        data = response.data.decode()
        assert competition['numberOfPlaces'] == expected_value[0]
        assert club['points'] == expected_value[1]
        assert expected_value[2] in data

    def test_should_limit_purchase_to_places_available(self, client, testing_data):
        NB_PLACES = 6
        club = testing_data['clubs'][3]
        competition = testing_data['competitions'][1]
        expected_value = [int(competition['numberOfPlaces']),
                          int(club['points']),
                          'There is only %s places left' % competition['numberOfPlaces']]
        response = client.post('/purchasePlaces',
                               data={'places': NB_PLACES, 'club': club['name'], 'competition': competition[
                                   'name']})
        data = response.data.decode()
        assert response.status_code == 200
        assert expected_value[2] in data
        assert int(competition['numberOfPlaces']) == expected_value[0]
        assert int(club['points']) == expected_value[1]

    def test_should_limit_number_of_purchase_to_12(self, client, testing_data):
        NB_PLACES = 13
        club = testing_data['clubs'][3]
        competition = testing_data['competitions'][1]
        expected_value = [int(competition['numberOfPlaces']),
                          int(club['points']),
                          'Can book only to a maximum of 12 places']
        response = client.post('/purchasePlaces',
                               data={'places': NB_PLACES, 'club': club['name'], 'competition': competition[
                                   'name']})
        data = response.data.decode()
        assert response.status_code == 200
        assert expected_value[2] in data
        assert int(competition['numberOfPlaces']) == expected_value[0]
        assert int(club['points']) == expected_value[1]

    def test_should_limit_purchase_to_place_own(self, client, testing_data):
        NB_PLACES = 6
        club = testing_data['clubs'][1]
        competition = testing_data['competitions'][2]
        expected_value = [competition['numberOfPlaces'],
                          club['points'],
                          "Not enough place"
                          ]
        response = client.post('/purchasePlaces',
                               data={'places': NB_PLACES, 'club': club['name'], 'competition': competition[
                                   'name']})
        data = response.data.decode()
        assert competition['numberOfPlaces'] == expected_value[0]
        assert club['points'] == expected_value[1]
        assert expected_value[2] in data
