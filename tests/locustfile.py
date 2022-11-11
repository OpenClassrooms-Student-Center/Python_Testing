from locust import HttpUser, task
from server import clubs, competitions


class ProjectPerfTest(HttpUser):
    @task
    def index(self):
        self.client.get("/")

    @task
    def show_summary(self):
        self.client.post("/showSummary", {"email": clubs[0]["email"]})

    @task
    def book(self):
        self.client.get(f"/book/{competitions[1]['name']}/{clubs[1]['name']}")

    @task
    def purchase_places(self):
        self.client.post(
            "/purchasePlaces",
            {
                "competition": competitions[0]["name"],
                "club": clubs[0]["name"],
                "places": "2",
                },
        )

    @task
    def listOfClubs(self):
        self.client.get("/list_of_clubs")

    @task
    def logout(self):
        self.client.get("/logout")
