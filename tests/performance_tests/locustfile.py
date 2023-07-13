from locust import HttpUser, task


class ProjectPerfTest(HttpUser):

    @task
    def index(self):
        self.client.get('')

    @task
    def display_board(self):
        self.client.get('clubsPointsBoard')

    @task
    def show_summary(self):
        self.client.post('showSummary', data={"email": "john@simplylift.co"})

    @task
    def booking(self):
        self.client.get('book/Spring Festival/Simply Lift')

    @task
    def purchase_places(self):
        self.client.post('purchasePlaces', data={"club": "Simply Lift", "competition": "Spring Festival", "places": 0})

    @task
    def logout(self):
        self.client.get('logout')
