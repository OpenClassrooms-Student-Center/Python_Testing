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
    
def retrieveDateCompetition(request):
    all_comp = loadCompetitions_test_data()
    for comp in all_comp:
        if comp['name'] == request:
            return comp['date']

def init_db_competitions():

    data = {
            "competitions": [
                {
                    "name": "Competition Test base",
                    "date": "2023-03-27 10:00:00",
                    "numberOfPlaces": "17"
                },
                {
                    "name": "Competition Test not enough points",
                    "date": "2023-10-22 13:30:00",
                    "numberOfPlaces": "3"
                },
                {
                    "name": "Competition Test 12 points",
                    "date": "2023-10-22 13:30:00",
                    "numberOfPlaces": "13"
                },
                {
                    "name": "out dated",
                    "date": "2020-10-22 13:30:00",
                    "numberOfPlaces": "15"
                }
            ]
        }
    
    with open("data/competitions_test.json", "w") as f:
        json.dump(data, f)

def init_db_clubs():
    data = {
            "clubs": [
                {
                    "name": "club test base",
                    "email": "mail1@test.co",
                    "points": "6"
                },
                {
                    "name": "club test not enough points",
                    "email": "mail2@test.co",
                    "points": "3"
                },
                {
                    "name": "club test more than 12 points",
                    "email": "mail3@test.co",
                    "points": "13"
                }
            ]
        }
    
    with open("data/clubs_test.json", "w") as f:
        json.dump(data, f)

def writerJson(alljsonValues: dict, actual: dict, jsonName: str):
    '''
    update json file
    '''

    for jsonValue in alljsonValues:
        if jsonValue['name'] == actual['name']:
            try:
                # club
                jsonValue['points'] = actual['points']
            except KeyError:
                # competition
                jsonValue['numberOfPlaces'] = actual['numberOfPlaces']

            if jsonName[:5] == 'data/':
                alljsonValues = {f'{jsonName[5:-10]}' : alljsonValues}
                with open(f'{jsonName[0:-5]}.json', 'w') as ajv:
                    json.dump(alljsonValues, ajv)
                ajv.close()
                break
            
            alljsonValues = {f'{jsonName[:-10]}' : alljsonValues}

            with open(f'{jsonName[:-10]}.json', 'w') as ajv:
                json.dump(alljsonValues, ajv)
            ajv.close()

def historicwriter(competion_name: str, club_name: str, points: str, test:str):
    '''
    Write and update historic file
    '''
    historic = {
        "competition": [
            {
                "name": competion_name,
                "club": club_name,
                "points": points
            }
        ]
    }

    # load file otherwise create it
    try:
        with open(f'{test}historic.json', 'r') as hist:
            data_historic = json.load(hist)
    except FileNotFoundError:
        with open(f'{test}historic.json', 'w') as hi:
            json.dump(historic, hi)
            return

    # Place values at the good place otherwise create value
    for historic in data_historic['competition']:
        if historic['name'] == competion_name and historic['club'] == club_name:
            historic['points'] = str(int(historic['points']) + int(points))
            with open('historic.json', 'w') as hi:
                json.dump(data_historic, hi)
                return
    else:
        historic_maj = {
            "name": competion_name,
            "club": club_name,
            "points": points
        }
        data_historic['competition'].append(historic_maj)
        with open(f'{test}historic.json', 'w') as hi:
            json.dump(data_historic, hi)