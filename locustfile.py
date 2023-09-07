from locust import HttpUser, task


class LocustPerfTest(HttpUser):
    @task
    def index(self):
        self.client.get("")

    @task
    def show_summary(self):
        self.client.post("showSummary", data={"email": "admin@irontemple.com"})

    @task
    def book(self):
        self.client.get("book/Spring Festival/Simply Lift")

    def purchasePlaces(self):
        self.client.post(
            "/purchasePlaces",
            data={"competition": "Spring Festival", "club": "Simply Lift", "places": 1},
        )

    @task
    def logout(self):
        self.client.get("logout")
