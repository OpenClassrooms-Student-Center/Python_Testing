from Python_Testing.server import showSummary
from Python_Testing.tests.conftest import client


def test_return_showSummary_if_mail_does_not_exist(client):
    app, templates = client
    rv = app.post(
        "/showSummary", data=dict(email="wrong@gmail.com"), follow_redirects=True
    )
    data = rv.data.decode()

    assert rv.status_code == 200
    assert "Email not found - try again!" in data
    template, context = templates[0]
    assert template.name == 'index.html'



