from locust import HttpUser, task, between, events
import server


@events.test_start.add_listener
def generate_test_data(**kwargs):
    """Populate server with large dataset before test runs"""
    server.clubs = [
        {"name": f"Club {i}", "email": f"club{i}@test.com", "points": "20"}
        for i in range(1000)
    ]
    server.competitions = [
        {"name": f"Competition {i}", "date": "2026-06-01 10:00:00", "numberOfPlaces": "25"}
        for i in range(500)
    ]

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