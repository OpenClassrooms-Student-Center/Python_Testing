import json

def loadClubs():
    with open('clubs.json') as c:
         listOfClubs = json.load(c)['clubs']
         return listOfClubs


def loadCompetitions():
    with open('competitions.json') as comps:
         listOfCompetitions = json.load(comps)['competitions']
         return listOfCompetitions
    
def loadClubs_test_data():
    with open('data/clubs_test.json') as c:
         listOfClubs = json.load(c)['clubs']
         return listOfClubs


def loadCompetitions_test_data():
    with open('data/competitions_test.json') as comps:
         listOfCompetitions = json.load(comps)['competitions']
         return listOfCompetitions


def search_club(club_email, clubs):
    club = [club for club in clubs if club['email'] == club_email]
    if len(club) == 1:
        return club[0]
    else:
        return None
    
    
def init_db_competitions():
    with open('data/competitions_test.json') as c:
         listOfCompetitions = json.load(c)['competitions']

    db_competitions = listOfCompetitions

    yield db_competitions

    db_competitions.clear()

def init_db_clubs():
    with open('data/clubs_test.json') as c:
         listOfClubs = json.load(c)['clubs']

    db_clubs = listOfClubs

    yield db_clubs

    db_clubs.clear()
