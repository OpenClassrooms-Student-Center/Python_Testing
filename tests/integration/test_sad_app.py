import pytest
from conftest import get

"""
    Testing a complete worst scenario of a user :
     * Home page : wrong endpoint (/home') doesn't exist.
     * Login : with unknown email
     * book for a unknown competition
     * purchase places :
            * past competition
            * more than 12 places,
            * more than competition's places, (book 12 places, this competition has 8)
            * more than club's points,

     * got to see display board with empty data
     * Logout successfully ;)

    data used for this test :
        Mostly :
        club = Basic lift, 15 points
        competition = Aka League, date [2023-02-05 10:00:00], 20 places.
"""


def test_sad_app(client, fixture):

    # ================================================== WRONG HOME PAGE

    response = client.get('/home')
    assert response.status_code == 404
    assert b'404 error page' in response.data

# ================================================== LOGIN WITH UNKNON EMAIL

    email = get(fixture, "wrong_email")
    response = client.post('/showSummary', data=email)
    assert response.status_code == 302
    with pytest.raises(Exception) as exc_info:
        assert str(exc_info.value) == "Sorry, this email wasn't found. Please try again with a correct email !!"

# ================================================== BOOK WITH UNKNON COMPETITION

    data = get(fixture, "club_unknown_competition")
    response = client.get(f"/book/{data['competition']}/{data['club']}")
    with pytest.raises(Exception) as exc_info:
        assert str(exc_info.value) == "Sorry, this club or competition wasn&#39;t found !!"

# ================================================== BOOK IN PAST COMPETITION

    data = get(fixture, "past_competition_places", 5)
    response = client.post('/purchasePlaces', data=data)
    assert response.status_code == 400
    assert b'Sorry, this competition is over !' in response.data

# ================================================== PURCHASE MORE THAN 12 PLACES

    data = get(fixture, "club_competition_places", 13)
    response = client.post('/purchasePlaces', data=data)
    assert response.status_code == 400
    assert b'Sorry, you can&#39;t book more than 12 places !' in response.data

# ================================================== PURCHASE MORE THAN COMPETITION'S PLACES

    data = get(fixture, "small_competition_places", 12)
    response = client.post('/purchasePlaces', data=data)
    assert response.status_code == 400
    assert b'Sorry, you book more places than available !' in response.data

# ================================================== PURCHASE MORE THAN CLUBS'S POINTS

    data = get(fixture, "club_competition_places", 10)
    response = client.post('/purchasePlaces', data=data)
    data = get(fixture, "club_competition_places", 10)
    response = client.post('/purchasePlaces', data=data)
    assert response.status_code == 400
    assert b'Sorry, your club doesn&#39;t have enough points !' in response.data

# ================================================== DISPLAY EMPTY POINTS BOARD

    get(fixture, "empty_board")
    response = client.get('/board')
    assert b'Sorry, this section has no clubs to display' in response.data

# ================================================== LOGOUT

    response = client.get('/logout')
    assert response.status_code == 302
    assert response.headers["Location"] == "/"
