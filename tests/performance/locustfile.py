from locust import HttpUser, task

import sys
sys.path.append('../../')

from server import update_json


class PerfTest(HttpUser):
    """
        Performance tests on all routes

        Club :
            "id":"0",
            "name":"Club Locust",
            "email":"club@locust.com",
            "points":"500"

        Competition :
            "name": "Competition Locust",
            "date": "2030-01-01 10:00:00",
            "numberOfPlaces": "10000"
    """

    def on_start(self):
        update_json("clubs", {"id": "0",
                              "name": "Club Locust",
                              "email": "club@locust.com",
                              "points": 50000})
        update_json("competitions", {"name": "Competition Locust",
                                     "date": "2030-01-01 10:00:00",
                                     "numberOfPlaces": 100000})

    @task
    def login(self):
        self.client.get("/")
        self.client.post("/showSummary", data={"email": "club@locust.com"})

    @task
    def logout(self):
        self.client.get("/logout")

    @task
    def show_competitions(self):
        self.client.get("/showCompetitions/Club Locust")

    @task
    def show_clubs(self):
        self.client.get("/show_clubs/Club Locust")

    @task
    def book(self):
        self.client.get("/book/Competition Locust/Club Locust")

    @task
    def purchase_places(self):
        self.client.post("/purchasePlaces", data={"competition": "Competition Locust",
                                                  "club": "Club Locust",
                                                  "places": 1})
