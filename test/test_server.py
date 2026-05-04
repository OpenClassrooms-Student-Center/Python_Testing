
def test_show_summary_with_valid_email(client):
    response = client.post("/showSummary", data={
        "email": "admin@irontemple.com"
    })

    assert response.status_code == 200
    assert b"Welcome" in response.data

def test_show_summary_with_unknown_email(client):
    response = client.post("/showSummary", data={
        "email": "unknown@test.com"
    }, follow_redirects=True)

    assert response.status_code == 200
    assert b"Sorry, that email was not found" in response.data



def test_purchase_places_with_valid_number_of_places(client):
    response = client.post("/purchasePlaces", data={
        "competition": "Spring Festival",
        "club": "Iron Temple",
        "places": "2"
    }, follow_redirects=True)
    
    assert response.status_code == 200
    assert b"Great-booking complete!" in response.data
    
def test_purchase_places_with_too_many_places(client):
    response = client.post("/purchasePlaces", data={
        "competition": "Spring Festival",
        "club": "Iron Temple",
        "places": "5", 
    })
    
    assert response.status_code == 200
    assert b"You are not authorized to book this number of places" in response.data
    


