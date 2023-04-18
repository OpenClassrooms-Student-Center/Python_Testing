import json


def loadClubs(clubs_path):
    with open(clubs_path) as c:
        listOfClubs = json.load(c)['clubs']
        return listOfClubs


def loadCompetitions(competitions_path):
    with open(competitions_path) as comps:
        listOfCompetitions = json.load(comps)['competitions']
        return listOfCompetitions


def search_club(club_email, clubs):
    '''
    #1 verify if club exist
    '''
    club = [club for club in clubs if club['email'] == club_email]
    if len(club) == 1:
        return club[0]
    else:
        return None


def retrieveDateCompetition(request, comps_path):
    '''
    #5 return date of request competition
    '''
    all_comp = loadCompetitions(comps_path)
    for comp in all_comp:
        if comp['name'] == request:
            return comp['date']


def writerJson(alljsonValues: list[dict],
               actual: dict,
               jsonName: str,
               path: str) -> dict:
    '''
    #6 update json file
    '''

    for jsonValue in alljsonValues:
        if jsonValue['name'] == actual['name']:
            try:
                # club
                jsonValue['points'] = actual['points']
            except KeyError:
                # competition
                jsonValue['numberOfPlaces'] = actual['numberOfPlaces']

            alljsonValues = {f'{jsonName[:-5]}': alljsonValues}

            with open(path, 'w') as ajv:
                json.dump(alljsonValues, ajv)
            ajv.close()
