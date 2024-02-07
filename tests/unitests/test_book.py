import pytest
import server
from server import app

def test_book_past_competition(client):
    """
    Test booking for a past competition.
    """
    response = client.get('/book/Fall%20Classic/Simply%20Lift')
    assert b"Error: can not purchase a place for past competitions" in response.data
    assert response.status_code == 200



def test_book_valid_booking(client, monkeypatch, clubs, competitions):
    """
    Test booking for a valid competition and club.
    """
    
   # Mock the get_club function
    def patch_get_club(dummy):
        """Mock get_club() function"""
        return {"name": "Simply Lift", "points": 13}


    monkeypatch.setattr(server, "get_club", patch_get_club)
    monkeypatch.setattr(server, "competitions", competitions)
    monkeypatch.setattr(server, "clubs", clubs)
    
    response = client.get('/book/Fall%20Classic/Simply%20Lift')
    assert b"Book Places" in response.data
    assert response.status_code == 200
    

    
def test_book_nonexistent_competition(client):
    """
    Test booking for a non-existent competition.
    """
    response = client.get('/book/Nonexistent%20Competition/Simply%20Lift')
    assert b"Something went wrong-please try again" in response.data
    assert response.status_code == 400


def test_book_nonexistent_club(client):
    """
    Test booking for a non-existent club.
    """
    response = client.get('/book/Spring%20Festival/Nonexistent%20Club')
    assert b"Something went wrong-please try again" in response.data
    assert response.status_code == 400
