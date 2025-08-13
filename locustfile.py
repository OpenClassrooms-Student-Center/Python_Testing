from locust import HttpUser, task, between

class SingleUser(HttpUser):
    wait_time = between(1, 2)

    def on_start(self):
        self.client.post("/showSummary", data={"email": "john@simplylift.co"})

    @task
    def booking_scenario(self):
        self.client.get("/")
        self.client.get("/book/Future Sport/Simply Lift")
        self.client.post("/purchasePlaces", data={
            "competition": "Future Sport",
            "club": "Simply Lift",
            "places": "2"
        })
        self.client.get("/logout")
