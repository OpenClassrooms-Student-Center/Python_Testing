import pytest
import server



def test_booking_process(client):
    """
    Test the booking process for a competition.
    """
    # Étape 1: Connexion de l'utilisateur
    response = client.post('/showSummary', data={'email': 'john@simplylift.co'})
    assert response.status_code == 200
    assert b'Welcome, john@simplylift.co' in response.data  # Vérifiez que l'utilisateur est connecté

    # Étape 2: Sélection de la compétition "Winter Showdown" et vérification de la redirection vers la page de réservation
    response = client.get('/book/Winter Showdown/Simply Lift')
    assert response.status_code == 200
    assert b'Winter Showdown' in response.data  # Assurez-vous que le nom de la compétition est correct dans la réponse

    # Étape 3: Réalisation d'une réservation pour "Winter Showdown"
    response = client.post('/purchasePlaces', data={
        'competition': 'Winter Showdown',
        'club': 'Simply Lift',
        'places': 1
    })
    assert response.status_code == 200
    assert b'Great-booking complete!' in response.data  # Vérification que la réservation a été réussie

    # Étape 4: Vérification que les points du club ont été déduits correctement
    response = client.post('/showSummary', data={'email': 'john@simplylift.co'})
    assert b'Points available: 12' in response.data  


    # Étape 5: Vérification de la mise à jour du nombre de places disponibles
    assert b'Number of Places: 29' in response.data  
    assert b'Number of Places: 30' not in response.data  


    # Tenter de réserver plus de places que le club n'a de points
    response = client.post('/purchasePlaces', data={
        'competition': 'Winter Showdown',
        'club': 'Simply Lift',
        'places': 100  # Un nombre délibérément élevé pour dépasser les points disponibles
    })
    print(response.data.decode('utf-8'))
    #assert b"You don't have enough points." in response.data
    assert b"You don&#39;t have enough points."


    # Tenter de réserver plus de places que disponibles
    response = client.post('/purchasePlaces', data={
        'competition': 'Winter Invitational',
        'club': 'Simply Lift',
        'places': 12  # Un nombre délibérément élevé pour dépasser les places disponibles
    })
    assert b"Not enough places available" in response.data


    # rajouter le logout