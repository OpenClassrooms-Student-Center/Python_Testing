from bs4 import BeautifulSoup


def get_club_test_data(clubs_list):
    """Return the club test data."""
    return clubs_list


def get_competition_test_data(competitions_list):
    """Return the competition test data."""
    return competitions_list


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
    assert 'Great-booking complete!' in soup.prettify()
    assert 'Points available: 2' in soup.prettify()
    h4_winter_classic = soup.find('h4', string='Winter Classic')
    date = h4_winter_classic.find_next_sibling('p')
    place = date.find_next_sibling('p')
    assert place.text == 'Number of Places: 11'


def test_book_past_competition_gives_error_message(client):
    """Test that booking a past competition gives an error message."""
    res = client.get('/book/Fall Classic/Iron Temple')
    soup = BeautifulSoup(res.data, 'html.parser')
    assert ("Sorry, you can't book for this competition "
            "as the date has passed.") in soup.prettify()


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
