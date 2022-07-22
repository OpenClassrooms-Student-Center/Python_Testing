from datetime import datetime


def date_is_passed(date) -> bool:
    """Return True if the variable date is passed or not"""
    date = datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
    present = datetime.now()
    if date.date() < present.date():
        return True