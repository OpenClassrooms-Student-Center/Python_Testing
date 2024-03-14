from server import app

def test_summary_page(test_client):
    with app.test_client() as client:
        response = client.post("/showSummary", data={"email": "john@simplylift.co"})
        assert response.status_code == 200
        assert f"Welcome, john@simplylift.co" in str(response.data)
        assert b"<title>Summary | GUDLFT Registration</title>" in response.data
        assert b"Welcome, john@simplylift.co" in response.data

        assert b'<a href="/logout">Logout</a>' in response.data

        assert b"Points available:" in response.data

        assert b"<h3>Competitions:</h3>" in response.data

        assert b"Date:" in response.data
        assert b"Number of Places:" in response.data
        assert b"Book Places" in response.data
