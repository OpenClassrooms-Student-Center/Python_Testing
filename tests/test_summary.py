from server import app

def test_summary_page(test_client):
    with app.test_client() as client:
        response = client.post("/showSummary", data={"email": "john@simplylift.co"})
        assert response.status_code == 200
        assert f"Welcome, john@simplylift.co" in str(response.data)
        # Assurez-vous que le titre de la page est correct.
        assert b"<title>Summary | GUDLFT Registration</title>" in response.data

        # Assurez-vous que le message de bienvenue affiche l'email du club.
        assert b"Welcome, john@simplylift.co" in response.data

        assert b'<a href="/logout">Logout</a>' in response.data

        # Assurez-vous que les points disponibles du club sont affichés.
        assert b"Points available: 13" in response.data

        # Assurez-vous que la liste des compétitions est correctement affichée.
        assert b"<h3>Competitions:</h3>" in response.data

        # Assurez-vous que chaque compétition est correctement affichée.
        assert b"Date:" in response.data
        assert b"Number of Places:" in response.data
        assert b"Book Places" in response.data
