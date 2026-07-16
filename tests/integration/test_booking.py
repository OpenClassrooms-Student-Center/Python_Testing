"""Tests d'intégration des routes de réservation (/book et /purchasePlaces)."""


class TestBookRoute:
    def test_book_requires_login(self, client):
        response = client.get("/book/Future Comp/Test Club A")
        assert response.status_code == 302

    def test_book_page_shown_for_own_club(self, logged_in_client):
        response = logged_in_client.get("/book/Future Comp/Test Club A")
        assert response.status_code == 200
        assert b"Future Comp" in response.data

    def test_book_other_club_is_rejected(self, logged_in_client):
        response = logged_in_client.get(
            "/book/Future Comp/Test Club B", follow_redirects=True
        )
        assert b"only book places for your own club" in response.data

    def test_book_past_competition_is_rejected(self, logged_in_client):
        response = logged_in_client.get(
            "/book/Past Comp/Test Club A", follow_redirects=True
        )
        assert b"already taken place" in response.data

    def test_book_rejected_when_club_limit_reached(self, logged_in_client):
        # Réserve déjà 12 places, puis rouvre la page : plus rien de réservable
        logged_in_client.post(
            "/purchasePlaces",
            data={"club": "Test Club A", "competition": "Future Comp", "places": "12"},
        )
        response = logged_in_client.get(
            "/book/Future Comp/Test Club A", follow_redirects=True
        )
        assert b"Cannot book more than 12" in response.data


class TestPurchaseGet:
    def test_get_purchase_without_login_redirects_to_index(self, client):
        response = client.get("/purchasePlaces")
        assert response.status_code == 302
        assert response.headers["Location"].endswith("/")

    def test_get_purchase_with_login_redirects_to_summary(self, logged_in_client):
        response = logged_in_client.get("/purchasePlaces")
        assert response.status_code == 302


class TestPurchasePost:
    def _purchase(self, client, competition, places, club="Test Club A"):
        return client.post(
            "/purchasePlaces",
            data={"club": club, "competition": competition, "places": str(places)},
            follow_redirects=True,
        )

    def test_valid_purchase_confirms_and_deducts(self, logged_in_client):
        response = self._purchase(logged_in_client, "Future Comp", 3)
        html = response.get_data(as_text=True)
        assert "3 places purchased" in html
        assert "Points available: 12" in html  # 15 - 3

    def test_purchase_with_invalid_number_is_rejected(self, logged_in_client):
        response = self._purchase(logged_in_client, "Future Comp", "abc")
        assert b"Invalid number of places" in response.data

    def test_purchase_over_points_is_rejected(self, client):
        client.post("/showSummary", data={"email": "b@test.com"})  # 4 points
        response = self._purchase(client, "Future Comp", 6, club="Test Club B")
        assert b"Not enough points available" in response.data

    def test_purchase_over_twelve_is_rejected(self, logged_in_client):
        response = self._purchase(logged_in_client, "Future Comp", 13)
        assert b"Cannot book more than 12" in response.data

    def test_purchase_for_other_club_is_rejected(self, logged_in_client):
        # Connecté en tant que Club A, tentative de réserver pour Club B
        response = self._purchase(logged_in_client, "Future Comp", 2, club="Test Club B")
        assert b"only book places for your own club" in response.data


class TestClubsPointsBoard:
    def test_board_is_public(self, client):
        response = client.get("/clubsPoints")
        assert response.status_code == 200

    def test_board_lists_all_clubs(self, client):
        response = client.get("/clubsPoints")
        html = response.get_data(as_text=True)
        assert "Test Club A" in html
        assert "Test Club B" in html
