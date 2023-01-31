from bs4 import BeautifulSoup


def test_first_page(client):
    """Test the login page."""
    response = client.get('/')
    assert b'Simply Lift' in response.data
    assert response.status_code == 200


def test_user_can_login(client):
    """Test the login page."""
    payload = {
        "email": "kate@shelifts.co.uk"
        }
    response = client.post("/showSummary", data=payload)
    assert response.status_code == 200
    assert b'Welcome, kate@shelifts.co.uk' in response.data


def test_user_cannot_login(client):
    """Test the login page."""
    payload = {
        "email": "unknown@mail.com",
        }
    response = client.post("/showSummary", data=payload)
    assert b'Sorry, that email wasn' in response.data
    assert b'Simply Lift' in response.data


def test_user_enter_empty_email(client):
    """Test the login page."""
    payload = {
        "email": "",
        }
    response = client.post("/showSummary", data=payload)
    assert b'Please enter your secretary' in response.data
    assert b'Simply Lift' in response.data


def test_points_update_are_reflected(client):
    """Test that the points are updated."""
    payload = {
            "club": "Iron Temple",
            "competition": "Winter Classic",
            "places": "2",
        }
    res = client.post("/purchasePlaces", data=payload)
    soup = BeautifulSoup(res.data, 'html.parser')
    assert 'Congratulation for booking 2 places !' in soup.prettify()
    assert 'Points available: 2' in soup.prettify()
    h4_winter_classic = soup.find('h4', string='Winter Classic')
    date = h4_winter_classic.find_next_sibling('p')
    place = date.find_next_sibling('p')
    assert place.text == 'Number of Places: 11'


def test_can_book_competition_that_has_a_correct_date_in_the_future(client):
    """Test that the user can book a competition
    that has a correct date in the future."""
    res = client.get('/book/Winter Classic/Simply Lift')
    soup = BeautifulSoup(res.data, 'html.parser')
    assert ("How many places?") in soup.prettify()


def test_book_past_competition_gives_error_message(client):
    """Test that booking a past competition gives an error message."""
    res = client.get('/book/Fall Classic/Iron Temple')
    soup = BeautifulSoup(res.data, 'html.parser')
    assert ("Sorry, you can't book for this competition "
            "as the date has passed.") in soup.prettify()


def test_post_book_past_competition_gives_error_message(client, ):
    """Test that booking a past competition gives an error message."""
    payload = {
            "club": "Iron Temple",
            "competition": "Fall Classic",
            "places": "2",
            }
    res = client.post("/purchasePlaces", data=payload)
    soup = BeautifulSoup(res.data, 'html.parser')
    print(soup.prettify())
    assert ("Sorry, you can't book for this competition "
            "as the date has passed.") in soup.prettify()


def test_access_bad_competition_display_error(client):
    """Test that a bad url gives an error message."""
    res = client.get('/book/Bad Competition/Iron Temple')
    soup = BeautifulSoup(res.data, 'html.parser')
    assert ("Sorry, that competition wasn't found.") in soup.prettify()


def test_access_bad_club_display_error(client):
    """Test that a bad url gives an error message."""
    res = client.get('/book/Fall Classic/Bad Club')
    soup = BeautifulSoup(res.data, 'html.parser')
    assert ("Sorry, that club wasn't found.") in soup.prettify()


def test_club_cannot_book_more_than_twelve_places(client):
    """Test that a club cannot book more than 12 places."""
    payload = {
            "club": "Simply Lift",
            "competition": "Winter Classic",
            "places": "13",
        }
    res = client.post("/purchasePlaces", data=payload)
    soup = BeautifulSoup(res.data, 'html.parser')
    assert ("You can only book 12 places per competition.") in soup.prettify()


def test_club_cannot_book_more_than_twelve_places_in_total(client):
    """Test that a club cannot book more than 12 places in total."""
    payload = {
            "club": "Simply Lift",
            "competition": "Winter Classic",
            "places": "11",
        }
    client.post("/purchasePlaces", data=payload)
    payload = {
            "club": "Simply Lift",
            "competition": "Winter Classic",
            "places": "2",
        }
    res = client.post("/purchasePlaces", data=payload)
    soup = BeautifulSoup(res.data, 'html.parser')
    assert ("You can only book 12 places per competition.") in soup.prettify()


def test_error_for_competition_that_are_full(client):
    """Test that the user receives an error when competition are full."""
    payload = {
            "club": "She Lifts",
            "competition": "Summer Classic",
            "places": "10"
        }
    res = client.post("/purchasePlaces", data=payload)
    res = client.get("/book/Summer Classic/She Lifts")
    soup = BeautifulSoup(res.data, 'html.parser')
    assert ("Sorry, there are no places " +
            "left for this competition.") in soup.prettify()


def test_club_cannot_book_more_than_club_points(client):
    """Test that a club cannot book more than your points."""
    payload = {
            "club": "Iron Temple",
            "competition": "Winter Classic",
            "places": "5",
        }
    res = client.post("/purchasePlaces", data=payload)
    soup = BeautifulSoup(res.data, 'html.parser')
    assert ("You don't have enough points to book 5 places") in soup.prettify()


def test_logout(client):
    """Test that the logout works."""
    res = client.get('/logout')
    assert res.status_code == 302
    assert res.headers['Location'] == '/'
