from locust import HttpUser, task, between


class Tests(HttpUser):
    wait_time = between(1, 3)

    @task
    def access_index(self):
        self.client.get("/")

    @task
    def access_logout(self):
        self.client.get("/logout")

    @task
    def access_summary(self):
        self.client.post("/showSummary", data={"email": "admin@irontemple.com"})

    @task
    def booking_a_competition(self):
        self.client.post(
            "/purchasePlaces",
            data={"places": "2", "club": "Iron Temple", "competition": "Fall Classic"},
        )

    @task
    def access_clubs_overview(self):
        self.client.get("/clubs_overview")
