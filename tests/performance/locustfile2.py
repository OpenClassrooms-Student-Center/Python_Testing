from locust import HttpUser, between, task


class BuyUpdatePoints(HttpUser):
    """
    testing that updating total of points doesn't exceed 2 secondes.
    """
    wait_time = between(1, 3)
    host = "http://127.0.0.1:5000"

    def on_start(self):
        self.client.get("/")

    @task(1)
    def show_summary(self):
        self.client.post("/showSummary", data={"email": "john@simplylift.co"})

    @task(1)
    def display_book_competition_form(self):
        self.client.get('/book/Winter Competition/Simply Lift')

    @task(1)
    def purchase_places(self):
        data = {'club': 'Simply Lift', 'competition': 'Winter Competition', 'places': 2}
        self.client.post('/purchasePlaces', data=data, catch_response=True)

    @task(1)
    def display_board_points_update(self):
        self.client.get('/board')

    def on_stop(self):
        self.client.get("/logout")
