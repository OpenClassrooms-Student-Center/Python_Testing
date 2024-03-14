from server import app

def test_logout(test_client):
    with app.test_client() as client:
        login_response = client.post("/showSummary", data={"email": "john@simplylift.co"})
        assert login_response.status_code == 200
        assert b"Welcome, john@simplylift.co" in login_response.data

        logout_response = client.get("/logout")
        assert logout_response.status_code == 302
