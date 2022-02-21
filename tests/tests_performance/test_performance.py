from locust import HttpUser, task

class ProjectPerfTest(HttpUser):

    @task
    def home(self):
        self.client.get("/")

    @task
    def showSummary(self):
        data = {"email": "admin@irontemple.com"}
        self.client.post("/showSummary", data=data)

    @task
    def book(self):
        self.client.get("/book/Future%20Competition/Simply%20Lift")

    @task
    def purchasePlaces(self):
        data = {"club": "Simply Lift", "competition": "Spring Festival", "places": 1}
        self.client.post("/purchasePlaces", data=data)

    @task
    def clubsPoints(self):
        self.client.get("/clubs")

    @task
    def logout(self):
        self.client.get("/logout")