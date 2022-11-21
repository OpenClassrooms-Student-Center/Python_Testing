from locust import HttpUser, task
from locust import events

from server import update_json, load_json, save_json


def _clean_json(file_name):
    """ Remove all entries with __Locust in name """

    tab = load_json(file_name)
    for entry in tab:
        if '__Locust' in entry['name']:
            tab.remove(entry)

    save_json(file_name, tab)


class TestLocust(HttpUser):

    # Create a competition and a club only for locust
    @events.test_start.add_listener
    def on_test_start(environment, **kwargs):
        update_json("competitions", {"name": "Competition __Locust",
                                     "date": "2030-01-01 10:00:00",
                                     "numberOfPlaces": 100000})

        update_json("clubs", {"id": "__Locust",
                              "name": "name __Locust",
                              "email": "club@locust.com",
                              "points": 100000})

    # Delete them
    @events.test_stop.add_listener
    def on_test_stop(environment, **kwargs):
        _clean_json('clubs')
        _clean_json('competitions')

    @task
    def login_book_visit_logout(self):

        self.client.get("/")
        self.client.post("/login", data={"email": "club@locust.com"})

        self.client.get("/book/Competition __Locust")
        self.client.post("/purchasePlaces", data={"competition": "Competition __Locust",
                                                  "places": 1})
        self.client.get("/showClubs")
        self.client.get("/showCompetitions")
        self.client.get("/logout")

    @task
    def show_clubs(self):
        self.client.get("/showClubs")
