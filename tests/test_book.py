from server import app
from flask import url_for

competitions = [
    {
        "name": "Spring Festival",
        "date": "2020-03-27 10:00:00",
        "numberOfPlaces": "25"
    },
    {
        "name": "Fall Classic",
        "date": "2020-10-22 13:30:00",
        "numberOfPlaces": "13"
    }
]

clubs = [
    {
        "name": "Simply Lift",
        "email": "john@simplylift.co",
        "points": "13"
    },
    {
        "name": "Iron Temple",
        "email": "admin@irontemple.com",
        "points": "4"
    },
    {
        "name": "She Lifts",
        "email": "kate@shelifts.co.uk",
        "points": "12"
    }
]

def test_book():
    with app.test_request_context():
        with app.test_client() as client:
            # Connection
            login_response = client.post("/showSummary", data={"email": "john@simplylift.co"})
            assert login_response.status_code == 200
            assert b"Welcome, john@simplylift.co" in login_response.data

            # GET foreach competition and club
            for comp in competitions:
                for club in clubs:
                    book_places_url = url_for('book', competition=comp['name'], club=club['name'])
                    book_response = client.get(book_places_url)
                    assert book_response.status_code == 200

                    assert b"Book" in book_response.data

                    test_comp = competitions[0]
                    test_club = clubs[0]

                    num_places = 3
                    response = client.post("/purchasePlaces", data={
                        "club": test_club['name'],
                        "competition": test_comp['name'],
                        "places": num_places
                    })

                    assert response.status_code == 200
                    assert b"Great-booking complete!" in response.data

