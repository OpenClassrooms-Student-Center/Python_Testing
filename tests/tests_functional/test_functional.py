from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium import webdriver

validation = "Great-booking complete!"

class TestFunctional():
    def test_open_chrome_window(self):
        self.browser = webdriver.Chrome("tests/tests_functional/chromedriver.exe")

        self.browser.get("http://127.0.0.1:5000/")
        email = self.browser.find_element(By.NAME, "email")
        email.send_keys("kate@shelifts.co.uk")
        email.send_keys(Keys.ENTER)
        competition = self.browser.find_element(By.LINK_TEXT, "Book Places")
        competition.click()
        nb_places = self.browser.find_element(By.NAME, "places")
        nb_places.send_keys("1")
        input_booking = self.browser.find_element(By.TAG_NAME, "button")
        input_booking.click()
        # valid_booking = self.browser.find_element(By., "Great-booking complete!")

        # assert valid_booking == validation
