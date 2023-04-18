from .tests.utilities import loadClubs, loadCompetitions

CLUBS_PATH = 'clubs.json'
COMPETITIONS_PATH = 'competitions.json'
CLUBS_TEST_PATH = 'data_tests/clubs.json'
COMPETITIONS_TEST_PATH = 'data_tests/competitions.json'


def get_config(app):

    if app["TESTING"] is True:
        app.update({
            'DEBUG': True,
            'CLUBS': loadClubs(CLUBS_TEST_PATH),
            'COMPETITIONS': loadCompetitions(COMPETITIONS_TEST_PATH),
            'CLUBS_PATH': 'data_tests/clubs.json',
            'COMPS_PATH': 'data_tests/competitions.json'
        })
        return app

    app.update({
        'DEBUG': False,
        'CLUBS': loadClubs(CLUBS_PATH),
        'COMPETITIONS': loadCompetitions(COMPETITIONS_PATH),
        'CLUBS_PATH': 'clubs.json',
        'COMPS_PATH': 'competitions.json'
    })

    return app
