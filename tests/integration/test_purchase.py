import server


def test_purchase_deducts_points_from_club(client):
    """Bug #6 : les points utilises doivent etre deduits du solde du club."""
    # On choisit un club et une competition connus
    club = next(c for c in server.clubs if c['name'] == "Simply Lift")
    competition = next(
        c for c in server.competitions if c['name'] == "Spring Festival"
    )

    points_avant = int(club['points'])
    places_reservees = 3

    client.post(
        "/purchasePlaces",
        data={
            "competition": competition['name'],
            "club": club['name'],
            "places": str(places_reservees),
        },
    )

    points_apres = int(club['points'])
    assert points_apres == points_avant - places_reservees

def test_purchase_more_than_points_is_blocked(client):
    """Bug #2 : un club ne peut pas reserver plus de places qu'il n'a de points."""
    club = next(c for c in server.clubs if c['name'] == "Iron Temple")  # 4 points
    competition = next(
        c for c in server.competitions if c['name'] == "Spring Festival"
    )

    points_avant = int(club['points'])
    places_demandees = points_avant + 5  # plus que le solde : impossible

    response = client.post(
        "/purchasePlaces",
        data={
            "competition": competition['name'],
            "club": club['name'],
            "places": str(places_demandees),
        },
        follow_redirects=True,
    )

    # Les points ne doivent pas avoir changé (rien n'a ete reserve)
    assert int(club['points']) == points_avant
    # Un message d'erreur doit apparaitre
    assert b"do not have enough points" in response.data

def test_purchase_more_than_12_places_is_blocked(client):
    """Bug #3 : un club ne peut reserver plus de 12 places par competition"""
    # On choisit un club et une competition connus
    club = next(c for c in server.clubs if c['name'] == "Simply Lift")
    competition = next(
        c for c in server.competitions if c['name'] == "Spring Festival"
    )

    points_avant = int(club['points'])
    places_demandees = 13 # au dessus de la limite de 12

    response = client.post(

        "/purchasePlaces",
        data={
            "competition": competition['name'],
            "club": club['name'],
            "places": str(places_demandees),
        },
        follow_redirects=True,
    )

    # Rien ne doit avoir ete debite
    assert int(club["points"]) == points_avant
    # Un message erreur doit apparaitre
    assert b"cannot book more than 12 places" in response.data

def test_purchase_more_than_available_places_is_blocked(client):
    """Bug #4 : un club ne peut pas reserver plus de places qu'il n'en reste"""
    club = next(c for c in server.clubs if c['name'] == "Simply Lift")
    competition = next(
        c for c in server.competitions if c['name'] == "Spring Festival"
    )

    # Force une competition presque pleine
    competition['numberOfPlaces'] = "5"

    points_avant = int(club['points'])
    places_demandees = 10 # Sous la limite de 12 mais plus que les 5 restants

    response = client.post(
        "/purchasePlaces",
        data={
            "competition": competition['name'],
            "club": club['name'],
            "places": str(places_demandees),
        },
        follow_redirects=True,
    )

    # Rien ne doit avoir change
    assert int(club['points']) == points_avant
    assert int (competition['numberOfPlaces']) == 5
    # Un message d'erreur doit apparaitre
    assert b"not enough places available" in response.data