from locust import HttpUser, task, between
from server import loadClubs, loadCompetitions


class TestUser(HttpUser):
    wait_time = between(1, 2)
    competitions = loadCompetitions()[0]['name']
    club = loadClubs()[0]["name"]
    email = loadClubs()[0]["email"]

    @task
    def index(self):
        """"""
        self.client.get("/")

    @task
    def connexion(self):
        self.client.post("/showSummary", data={"email": self.email}, name="showSummary")

    @task
    def purchase_places(self):
        self.client.post("/purchasePlaces", data={
            "club": self.club,
            "competition": self.competitions,
            "places": 2,
        }, name="purchasePlaces")

    @task
    def get_place(self):
        self.client.get("/book/" + self.competitions
                        + "/" + self.club, name="book")

    @task
    def logout(self):
        """"""
        self.client.get("/logout")