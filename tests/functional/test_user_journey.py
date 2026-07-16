"""
Test fonctionnel : parcours complet d'un secrétaire de club.

Reproduit le scénario décrit dans les spécifications :
consultation publique du tableau des points, connexion, réservation avec
déduction des points, puis déconnexion et blocage de l'accès.
"""


class TestFullSecretaryJourney:
    def test_complete_booking_journey(self, client):
        # 1. Le tableau public des points est consultable sans connexion
        board = client.get("/clubsPoints")
        assert board.status_code == 200
        assert b"Test Club A" in board.data

        # 2. Connexion avec un email de secrétaire valide
        client.post("/showSummary", data={"email": "a@test.com"})
        summary = client.get("/showSummary")
        assert summary.status_code == 200
        assert b"Points available: 15" in summary.data

        # 3. Ouverture de la page de réservation d'une compétition à venir
        booking_page = client.get("/book/Future Comp/Test Club A")
        assert booking_page.status_code == 200

        # 4. Réservation de 4 places : confirmation + points déduits (15 -> 11)
        purchase = client.post(
            "/purchasePlaces",
            data={"club": "Test Club A", "competition": "Future Comp", "places": "4"},
            follow_redirects=True,
        )
        html = purchase.get_data(as_text=True)
        assert "4 places purchased" in html
        assert "Points available: 11" in html

        # 5. Déconnexion
        client.get("/logout")
        with client.session_transaction() as sess:
            assert "club_email" not in sess

        # 6. Après déconnexion, la réservation n'est plus accessible
        blocked = client.get("/book/Future Comp/Test Club A")
        assert blocked.status_code == 302
