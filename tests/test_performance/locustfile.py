from locust import HttpUser, task

purchase = {
    'club': 'Simply Lift',
    'competition': 'Spring Festival',
    'places': '4'
}


class ProjectPerfTest(HttpUser):
    @task
    def home(self):
        self.client.get("/")

    @task
    def login(self):
        self.client.post("/showSummary", {'email': 'john@simplylift.co'})

    @task
    def book(self):
        url = "/book/Spring%20Festival/Simply%20Lift"
        self.client.get(url)

    @task
    def purchasePlace(self):
        self.client.post("/purchasePlaces", purchase)

    @task
    def board(self):
        self.client.get("/publicBoard")

    @task
    def logout(self):
        self.client.get("/logout")
