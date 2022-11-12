from locust import HttpUser, between, task


class ShowAllCompetitions(HttpUser):
    """
    Testing that retrieve all competitions doesn't exceed 5 secondes.
    """
    wait_time = between(1, 3)
    host = "http://127.0.0.1:5000"

    def on_start(self):
        self.client.get("/")

    @task(1)
    def show_summary(self):
        self.client.post("/showSummary", data={"email": "john@simplylift.co"})

    def on_stop(self):
        self.client.get("/logout")
