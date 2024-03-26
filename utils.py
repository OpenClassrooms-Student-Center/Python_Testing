class ClubNotFoundError(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)


def get_club(clubs: list, request_email: str):
    for club in clubs:
        if club["email"] == request_email:
            return club
    raise ClubNotFoundError
