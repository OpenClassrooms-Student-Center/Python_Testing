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