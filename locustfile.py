import time
import datetime
import os
from locust import HttpUser, task
from locust import events

from server import update_json, load_json, save_json
import uuid


def _clean_json(file_name):
    tab = load_json(file_name)
    for entry in tab:
        if '__Locust' in entry['name']:
            tab.remove(entry)

    save_json(file_name, tab)


class PerfTest(HttpUser):
    """
        Performance tests on all routes

        Club :
            "id":"0",
            "name":"Club __Locust",
            "email":"club@locust.com",
            "points":"500"

        Competition :
            "name": "Competition __Locust",
            "date": "2030-01-01 10:00:00",
            "numberOfPlaces": "10000"
    """
    unique_id = 0

    @events.test_start.add_listener
    def on_test_start(environment, **kwargs):
        update_json("competitions", {"name": f"Competition __Locust",
                                     "date": "2030-01-01 10:00:00",
                                     "numberOfPlaces": 100000})

    @events.test_stop.add_listener
    def on_test_stop(environment, **kwargs):
        _clean_json('clubs')
        _clean_json('competitions')

    def on_start(self):

        # self.unique_id = uuid.uuid4()
        self.unique_id = time.time()

        update_json("clubs", {"id": f"__Locust {self.unique_id}",
                              "name": f"Club __Locust {self.unique_id}",
                              "email": f"club{self.unique_id}@locust.com",
                              "points": 50000})

    @task
    def login(self):
        self.client.get("/")
        self.client.post("/showSummary", data={"email": f"club{self.unique_id}@locust.com"})

    @task
    def logout(self):
        self.client.get("/logout")

    @task
    def show_competitions(self):
        self.client.get(f"/showCompetitions/Club __Locust {self.unique_id}")

    @task
    def show_clubs(self):
        self.client.get(f"/show_clubs/Club __Locust {self.unique_id}")

    @task
    def book(self):
        self.client.get(f"/book/Competition __Locust/Club __Locust {self.unique_id}")

    @task
    def purchase_places(self):
        # for i in range(12):
        # for i in range(15):
        self.client.post("/purchasePlaces", data={"competition": f"Competition __Locust",
                                                  "club": f"Club __Locust {self.unique_id}",
                                                  "places": 1})


        # update_json("competitions", {"name": f"Competition __Locust {self.unique_id}",
                                     # "date": "2030-01-01 10:00:00",
                                     # "numberOfPlaces": 100000})

        time.sleep(1)







