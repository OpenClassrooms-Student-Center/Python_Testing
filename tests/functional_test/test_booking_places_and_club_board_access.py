import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
options = Options()
options.add_argument('--start-maximized')
options.add_argument('--disable-extensions')
# options.add_argument('--headless')
options.add_argument('--disable-gpu')
options.add_argument('--no-sandbox')
options.add_argument('disable-infobars')
options.add_argument('--remote-debugging-port=9222')


class TestBookingPlace:
    """Test class for booking a place"""

    def test_booking_places(self):
        """Login to the site, book a competition place and log out"""
        email = "john@simplylift.co"
        service = webdriver.chrome.service.Service('tests/functional_test/chromedriver')
        service.start()
        driver = webdriver.Remote(service.service_url, options=options)

        driver.get("http://127.0.0.1:5000/")
        time.sleep(2)
        assert "GUDLFT Registration" in driver.title

        driver.find_element(By.TAG_NAME, "input").send_keys(email + Keys.ENTER)
        time.sleep(3)
        assert "Summary | GUDLFT Registration" in driver.title

        link = driver.find_element(By.LINK_TEXT, "Book Places")
        link.click()
        time.sleep(2)
        assert "Booking for" in driver.title

        driver.find_element(By.NAME, "places").send_keys("1" + Keys.ENTER)
        time.sleep(3)
        assert "Summary | GUDLFT Registration" in driver.title

        link = driver.find_element(By.LINK_TEXT, "Logout")
        link.click()
        time.sleep(2)
        assert "GUDLFT Registration" in driver.title

        link = driver.find_element(By.LINK_TEXT, "Club points")
        link.click()
        time.sleep(2)
        assert "Club Points" in driver.title

        driver.close()
