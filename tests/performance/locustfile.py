from locust import HttpUser, task, between

class WebsiteUser(HttpUser):
    host = "http://127.0.0.1:5000"
    wait_time = between(1, 5)

    @task
    def view_index_page(self):
        self.client.get("/")

    @task
    def pointsBoard(self):
        self.client.get("/pointsBoard")


    @task(2)
    def show_summary(self):
        self.client.post("/showSummary", {"email": "john@simplylift.co"})

    @task
    def book_competition(self):
        self.client.get("/book/Winter Showdown/Simply Lift")

    @task
    def purchase_places(self):
        self.client.post("/purchasePlaces", {
            "competition": "Winter Showdown",
            "club": "Simply Lift",
            "places": 1
        })

