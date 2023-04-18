import time
from locust import HttpUser, task, between

class Tests(HttpUser):
    wait_time = between(1,5)

    @task
    def get_index(self):
        self.client.get('/')

