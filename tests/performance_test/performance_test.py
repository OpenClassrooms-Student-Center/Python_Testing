# performance_test.py
# created 25/01/2021 at 10:04 by Antoine 'AatroXiss' BEAUDESSON
# last modified 25/01/2021 at 10:04 by Antoine 'AatroXiss' BEAUDESSON

""" performance_test.py

To do:
    - *
"""

__author__ = "Antoine 'AatroXiss' BEAUDESSON"
__copyright__ = "Copyright 2021, Antoine 'AatroXiss' BEAUDESSON"
__credits__ = ["Antoine 'AatroXiss' BEAUDESSON"]
__license__ = ""
__version__ = "0.1.1"
__maintainer__ = "Antoine 'AatroXiss' BEAUDESSON"
__email__ = "antoine.beaudesson@gmail.com"
__status__ = "Development"

# standard library imports

# third party imports
from locust import HttpUser, task

# local application imports
from server import loadClubs, loadCompetitions

# other imports

# constants

"""
Objective:
    - loading time always below 5s
    - response time always below 2s
    - default user on performance test is 6

    - launch command: locust -f tests/performance_test/performance_test.py
    - url: http://localhost:8089/
    - host: http://127.0.0.1:5000
"""

clubs = loadClubs()
competitions = loadCompetitions()


class ProjectPerftest(HttpUser):

    club = clubs[0]
    competition = competitions[0]

    def on_start(self):
        self.client.post(
            "/showSummary",
            {
                "email": self.club['email'],
            })

    @task
    def index(self):
        self.client.get("/")

    @task
    def book(self):
        self.client.get(
            "/book/" + self.competition['name'] + "/" + self.club['name'])

    @task
    def purchase_places(self):
        self.client.post(
            "/purchasePlaces",
            {
                "club": self.club['name'],
                "competition": self.competition['name'],
                "places": "0"
            }
        )

    @task
    def on_stop(self):
        self.client.get('/logout')
