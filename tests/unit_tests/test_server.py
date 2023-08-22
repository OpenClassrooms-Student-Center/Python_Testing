from server import (clubs,
                    competitions)

club_name = clubs[1]["name"]
club_email = clubs[1]["email"]
club_points = int(clubs[1]["points"])
competition_name = competitions[1]["name"]


# Email tests
def test_valid_email(client):
    response = client.post("/showSummary", data={"email": club_email})
    data = response.data.decode()
    assert "Welcome" in data


def test_invalid_email(client):
    response = client.post("/showSummary", data={"email": "invalid@email.com"})
    data = response.data.decode()
    assert "Invalid email !" in data
