
class EmailNotFound(Exception):
    def __init__(self):
        self.msg = "Sorry, that email wasn't found."

    def __str__(self):
        return self.msg


class ClubNotEnoughPoints(Exception):
    def __init__(self):
        self.msg = "Sorry the club doesn't have enough points."

    def __str__(self):
        return self.msg


class CompetitionNotEnoughPlaces(Exception):
    def __init__(self):
        self.msg = "Sorry this competition doesn't have enough places."

    def __str__(self):
        return self.msg


class BookingLimitPlaces(Exception):
    def __init__(self):
        self.msg = "Sorry a club can only book a maximum of 12 places."

    def __str__(self):
        return self.msg


class CompetitionIsClosed(Exception):
    def __init__(self):
        self.msg = "Sorry the competition is closed."

    def __str__(self):
        return self.msg