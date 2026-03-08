import pytest
import threading
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import time
from webdriver_manager.chrome import ChromeDriverManager
import server

@pytest.fixture
def browser():
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    yield driver
    driver.quit()


@pytest.fixture(scope="session", autouse=True)
def run_server():
    thread = threading.Thread(target=lambda: server.app.run(port=5001, use_reloader=False))
    thread.daemon = True
    thread.start()
    time.sleep(1)
    yield

@pytest.fixture(autouse=True)
def reset_server_data():
    """Reset server data to original JSON values before each test"""
    server.clubs = server.load_clubs()
    server.competitions = server.load_competitions()
    yield

class TestFunctional:
    def test_points_board_accessible_without_login(self, browser, run_server):
        browser.get("http://127.0.0.1:5001/pointsByClub")
        assert "Points Board" in browser.title

    def test_login_journey(self, browser, run_server):
        browser.get("http://127.0.0.1:5001/")
        # find the email input and submit button
        browser.find_element(By.NAME, "email").send_keys("john@simplylift.co")
        browser.find_element(By.TAG_NAME, "button").click()
        assert "Welcome" in browser.page_source

    def test_club_reservation_journey(self, browser, run_server):
        # Step 1 - Login
        browser.get("http://127.0.0.1:5001/")
        browser.find_element(By.NAME, "email").send_keys("john@simplylift.co")
        browser.find_element(By.TAG_NAME, "button").click()
        time.sleep(1)  # wait for welcome page to load

        # Step 2 - Capture points before reservation
        points_before = int(re.search(r'Points available: (\d+)', browser.page_source).group(1))

        # Step 3 - Click Book Places
        browser.find_element(By.LINK_TEXT, "Book Places").click()
        time.sleep(1)  # wait for booking page to load

        # Step 4 - Enter 2 places and submit
        browser.find_element(By.NAME, "places").send_keys("2")
        browser.find_element(By.TAG_NAME, "button").click()
        time.sleep(1)  # wait for purchase to complete

        # Step 5 - Assert success message
        assert "Great-booking complete!" in browser.page_source

        # Step 6 - Assert points decreased by 2
        points_after = int(re.search(r'Points available: (\d+)', browser.page_source).group(1))
        assert points_after == points_before - 2
