from locust import HttpUser, task

class GudlftPerfTest(HttpUser):
    @task
    def home(self):
        self.client.get("/")

    @task
    def show_summary(self):
        self.client.post("/showSummary", data={"email": "john@simplylift.co"})

    @task
    def book_places(self):
        self.client.get("/book/Spring-Festival/Simply-Lift")

    @task
    def purchase_places(self):
        self.client.post("/purchasePlaces", data={"club": "Simply-Lift", "competition": "Spring-Festival", "places": 2})
