import urllib.parse
import html

CODE_200 = 200


def test_booking_right(client, purchaseBase):

    comp_conv = urllib.parse.quote(purchaseBase['competition'])
    club_conv = urllib.parse.quote(purchaseBase['club'])

    response = client.get(f"/book/{comp_conv}/{club_conv}")
    message = html.unescape(response.data.decode())

    assert response.status_code == CODE_200
    assert f'<input type="hidden" name="club" value="{purchaseBase["club"]}">'\
        in message


def test_booking_past_competition(client):
    comp_conv = urllib.parse.quote("Out Dated")
    club_conv = urllib.parse.quote("Iron Temple")

    response = client.get(f"/book/{comp_conv}/{club_conv}")
    message = html.unescape(response.data.decode())

    assert response.status_code == CODE_200
    assert "Something went wrong-please try again" in message


def test_booking_wrong_url(client):
    comp_conv = urllib.parse.quote("wrong url")
    club_conv = urllib.parse.quote("Simply Lift")

    response = client.get(f"/book/{comp_conv}/{club_conv}")
    message = html.unescape(response.data.decode())

    assert response.status_code == CODE_200
    assert "False request, you have been disconnected" in message
