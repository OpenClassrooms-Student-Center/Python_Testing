from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time


def test_spend_points(driver):
    """Test registration."""
    driver.get("http://www.localhost:5000/")
    assert "GUDLFT Registration" in driver.title
    mail = driver.find_element(By.NAME, "email")
    mail.send_keys("kate@shelifts.co.uk")
    mail.submit()
    time.sleep(1)
    assert "Welcome, kate@shelifts.co.uk" in driver.page_source
    links = driver.find_elements(By.TAG_NAME, "a")
    for i, link in enumerate(links):
        if i == 3:
            link.click()
    time.sleep(1)

    places_field = driver.find_element(By.NAME, "places")
    places_field.send_keys("5")
    places_field.submit()
    time.sleep(1)
    assert "Congratulation for booking 5 places !" in driver.page_source
    links = driver.find_elements(By.TAG_NAME, "a")
    for i, link in enumerate(links):
        if i == 3:
            link.click()
    time.sleep(1)
    places_field = driver.find_element(By.NAME, "places")
    places_field.send_keys("8")
    places_field.submit()
    time.sleep(1)
    assert "You don't have enough points to book 8 places." in driver.page_source
    driver.quit()
