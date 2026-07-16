"""
Tests de performance Locust — GUDLFT Registration Portal.

Critères Phase 2 (rules.md) :
  - Liste des compétitions : temps de réponse < 5 secondes
  - Mise à jour des points   : temps de réponse < 2 secondes
  - Nombre d'utilisateurs    : 6 (défaut)

Lancer (Flask actif sur le port 5000) :
  locust -f locustfile.py --headless -u 6 -r 2 --run-time 30s \\
         --host http://127.0.0.1:5000
"""
from locust import HttpUser, between, task
import random

MAX_COMPETITION_LIST_SECONDS = 5
MAX_POINTS_UPDATE_SECONDS = 2

CLUBS = [
    {"email": "john@simplylift.co", "name": "Simply Lift"},
    {"email": "admin@irontemple.com", "name": "Iron Temple"},
    {"email": "kate@shelifts.co.uk", "name": "She Lifts"},
]

UPCOMING_COMPETITION = "Summer Lift Off"


class SecretaryUser(HttpUser):
    """Simule un secrétaire de club connecté à l'application."""

    wait_time = between(1, 2)

    def on_start(self):
        """Connexion : associe chaque utilisateur virtuel à un club."""
        club = random.choice(CLUBS)
        self.club_email = club["email"]
        self.club_name = club["name"]
        self.client.post("/showSummary", data={"email": self.club_email})

    @task(3)
    def load_competition_list(self):
        """Charge la liste des compétitions à venir (GET /showSummary)."""
        with self.client.get(
            "/showSummary",
            name="/showSummary [liste compétitions]",
            catch_response=True,
        ) as response:
            if response.status_code != 200:
                response.failure(f"HTTP {response.status_code}")
                return
            if response.elapsed.total_seconds() > MAX_COMPETITION_LIST_SECONDS:
                response.failure(
                    f"Temps {response.elapsed.total_seconds():.3f}s "
                    f"> {MAX_COMPETITION_LIST_SECONDS}s"
                )

    @task(2)
    def update_points_via_booking(self):
        """Réserve 1 place et met à jour les points (POST /purchasePlaces)."""
        with self.client.post(
            "/purchasePlaces",
            data={
                "club": self.club_name,
                "competition": UPCOMING_COMPETITION,
                "places": "1",
            },
            name="/purchasePlaces [mise à jour points]",
            catch_response=True,
            allow_redirects=False,
        ) as response:
            if response.status_code not in (302, 200):
                response.failure(f"HTTP {response.status_code}")
                return
            if response.elapsed.total_seconds() > MAX_POINTS_UPDATE_SECONDS:
                response.failure(
                    f"Temps {response.elapsed.total_seconds():.3f}s "
                    f"> {MAX_POINTS_UPDATE_SECONDS}s"
                )

    @task(1)
    def view_public_points_board(self):
        """Consulte le tableau public des points (Phase 2)."""
        self.client.get("/clubsPoints", name="/clubsPoints [tableau public]")
