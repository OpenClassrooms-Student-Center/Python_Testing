from locust import HttpUser, task

class ProjectPerfTest(HttpUser):
    @task
    def index(self):
        self.client.get('/')

    @task
    def show_summary(self):
        self.client.post('/showSummary', data={"email": "john@simplylift.co"})

    @task
    def book(self):
        self.client.get('/book/Spring Festival/Simply Lift')