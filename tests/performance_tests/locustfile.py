from locust import HttpUser, task, between


class LocustTestServer(HttpUser):
    wait_time = between(1, 5)

    def on_start(self):
        self.client.get("/")
        self.client.post("/showSummary", data={'email': "john@simplylift.co"})

    @task
    def task1(self):
        pass
