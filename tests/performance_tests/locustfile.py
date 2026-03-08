from locust import HttpUser, task, between

class GudlftUser(HttpUser):
    wait_time = between(1, 2)  # seconds between tasks

    @task
    def view_competitions(self):
        self.client.post("/showSummary", data={"email": "john@simplylift.co"})

    @task
    def view_points_board(self):
        self.client.get("/pointsByClub")

    @task
    def purchase_places(self):
        self.client.post("/purchasePlaces", data={
            "competition": "Spring Festival",
            "club": "Simply Lift",
            "places": 2,
        })