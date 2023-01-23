from locust import HttpUser, task


class HelloWorldUser(HttpUser):
    @task
    def hello_world(self):
        self.client.get("/")
        payload = {
                'email': 'kate@shelifts.co.uk',
                }
        self.client.post('/showSummary', data=payload)
        self.client.get('/logout')
