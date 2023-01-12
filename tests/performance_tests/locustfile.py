from locust import HttpUser, task, between


class LocustTestServer(HttpUser):
    wait_time = between(1, 5)

    def on_start(self):
        self.client.get("/")
        self.client.post("/showSummary", data={'email': "john@simplylift.co"})

    @task
    def booking_get(self):
        self.client.get(f"/book/Spring Festival/Simply Lift")

    @task
    def booking_places_post(self):
        self.client.post(
            "/purchasePlaces",
            data={
                "places": 1,
                "club": "Simply Lift",
                "competition": "Spring Festival"
                 }
        )

    @task
    def logout(self):
        self.client.get("/logout")
