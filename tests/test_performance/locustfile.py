from locust import HttpUser, between, task


class TestProjectPerf(HttpUser):
    wait_time = between(1, 3)

    def on_start(self):
        self.client.get("/")

    @task(3)
    def show_summary(self):
        self.client.post("/showSummary", data={"email": "john@simplylift.co"})

    def on_stop(self):
        self.client.get("/logout")


class BuyUpdatePoints(HttpUser):
    wait_time = between(1, 3)

    def on_start(self):
        self.client.get("/")

    @task(1)
    def show_summary(self):
        self.client.post("/showSummary", data={"email": "john@simplylift.co"})

    @task(1)
    def book(self):
        self.client.get("/book/Winter Competition/Simply Lift")

    @task(1)
    def purchase_places(self):
        data = {
            "club": "Simply Lift",
            "competition": "Winter Competition",
            "places": 2,
        }
        self.client.post("/purchasePlaces", data=data, catch_response=True)

    @task(1)
    def show_board(self):
        self.client.get("/board")

    def on_stop(self):
        self.client.get("/logout")
