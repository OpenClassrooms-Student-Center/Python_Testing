from server import app

def test_logout(test_client):
    with app.test_client() as client:
        # Se connecter en tant qu'utilisateur
        login_response = client.post("/showSummary", data={"email": "john@simplylift.co"})
        assert login_response.status_code == 200
        assert f"Welcome, john@simplylift.co" in str(login_response.data)

        # Effectuer la requête de déconnexion
        logout_response = client.get("/logout", follow_redirects=True)
        assert logout_response.status_code == 200
