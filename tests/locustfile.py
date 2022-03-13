from locust import HttpUser, task


class ProjectPerfTest(HttpUser):
	@task
	def index(self):
		self.client.get("/")

	@task
	def showSummary(self):
		self.client.post("/showSummary", {'email': 'john@simplylift.co'})

	@task
	def book(self):
		self.client.get("/book/Fall Classic/Simply Lift")

	@task
	def purchasePlaces(self):
		self.client.post("/purchasePlaces", {"competition": "Spring Festival",
											 "club": "Iron Temple",
											 "places": "5"})

	@task
	def listOfPoints(self):
		self.client.get("/points")

	@task
	def logout(self):
		self.client.get("/logout")
