from locust import HttpUser, task


class ServerTester(HttpUser):
    @task
    def server_test(self):
        self.client.get('')
        self.client.get('/book/Spring Festival/Simply Lift')
        self.client.get('/logout')

        self.client.post('/showSummary', data={'email': 'john@simplylift.co'})
        self.client.post(
            '/purchasePlaces', data={'places': '2', 'competition': 'Spring Festival', 'club': 'Simply Lift'})
