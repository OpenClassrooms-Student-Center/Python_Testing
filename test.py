
from datetime import datetime, date

competitions = [
                {
                    "name": "Spring Festival",
                    "date": "20223-03-27 10:00:00",
                    "numberOfPlaces": "25"
                },
                {
                    "name": "Fall Classic",
                    "date": "2020-10-22 13:30:00",
                    "numberOfPlaces": "13"
                }
                ]


now = datetime.now() # current date and time
date_time = now.strftime("%Y/%m/%d %H:%M:%S")
print(type(now))
gg = competitions[1]["date"]
date_time_comp = datetime.strptime(gg, '%Y-%m-%d %H:%M:%S')
print(type(date_time_comp), date_time_comp)
print(now > date_time_comp)