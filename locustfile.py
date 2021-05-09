from locust import HttpUser
from locust.user.task import task

from server import FlaskWrapper

class SoftdeskPerf(HttpUser):

    @task
    def perf_index(self):
        self.client.get("/")

    @task
    def perf_showSummary(self):
        self.client.post("/showSummary", data={ "email": "admin@irontemple.com" })

    @task
    def perf_book(self):
        competition = "Ragnarok"
        club = "strongest@mail.com"
        self.client.get("/book/{competition}/{club}")

    @task
    def perf_purchasePlaces(self):
        competition = "Ragnarok"
        club = "The strongs"
        places = "4"
        self.client.post("/purchasePlaces", data={ "competition": competition, "club": club, "places": places })

    @task
    def perf_displayboard(self):
        self.client.get('/displayboard')

    @task
    def perf_logout(self):
        self.client.get("/logout")
