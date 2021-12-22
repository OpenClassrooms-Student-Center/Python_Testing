import shutil

from locust import HttpUser, TaskSet, task, between

class UserBehaviour(TaskSet):
    @task
    def on_start(self):
        self.client.get("/")
        self.client.post('/showSummary', data={"email": "john@simplylift.co"})

    @task
    def on_stop(self):
        self.client.get('/logout')

    @task
    def index(self):
        self.client.get("/")

    @task
    def full_display(self):
        self.client.get("/fullDisplay")

    @task
    def book(self):
        self.client.get("/book/Frozen Drops/Simply Lift")

    @task
    def purchase_places(self):
        self.client.post('/purchasePlaces', data={"club": "Simply Lift",
                                                "competition": "Frozen Drops",
                                                "places": "1"})
        shutil.copyfile('clubs.json', 'test_clubs.json')
        shutil.copyfile('competitions.json', 'test_competitions.json')

class MyUser(HttpUser):
    tasks = [UserBehaviour]

    wait_time = between(5, 15)
