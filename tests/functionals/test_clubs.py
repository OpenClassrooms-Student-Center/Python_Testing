from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

import time

options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])

chrome_driver = webdriver.Chrome(options=options, service=Service(ChromeDriverManager().install()))


def test_success_purchase():
    """
    1 - User enter valid mail
    2 - User want book place in Test Competition and click it
    3 - User purchase one place in Test Competition, expected 45 club points, 7 competition points
    """
    #1
    chrome_driver.get("http://127.0.0.1:5000")
    email_field = chrome_driver.find_element(By.NAME, 'email')
    email_field.send_keys('luxe@shetest.co.uk')
    email_field.send_keys(Keys.ENTER)
    time.sleep(0)
    element = chrome_driver.find_element(By.TAG_NAME, 'h2')

    assert element.text == 'Welcome, luxe@shetest.co.uk'

    #2
    book_places_list = chrome_driver.find_elements(By.LINK_TEXT, 'Book Places')
    purchase_link = book_places_list[0]
    purchase_link.click()
    time.sleep(0)
    element = chrome_driver.find_element(By.TAG_NAME, 'h2')

    assert 'Test Competition' in element.text

    #3
    places_field = chrome_driver.find_element(By.NAME, 'places')
    places_field.send_keys(1)
    places_field.send_keys(Keys.ENTER)
    time.sleep(0)
    element = chrome_driver.find_elements(By.TAG_NAME, 'li')

    assert 'Great-booking complete!' in element[0].text
    assert 'Points available: 45' in chrome_driver.page_source
    assert 'Number of Places: 7' in chrome_driver.page_source


def test_not_enought_points():
    """
    1 - User connect with valid email
    2 - User want book place in Test Competition and click it
    3 - User book places in test competition with not enought club points
    4 - User attempt to books places but the competition have no enought points
    """

    #1
    chrome_driver.get("http://127.0.0.1:5000")
    email_field = chrome_driver.find_element(By.NAME, 'email')
    email_field.send_keys('luxe@shetest.co.uk')
    email_field.send_keys(Keys.ENTER)
    time.sleep(0)
    element = chrome_driver.find_element(By.TAG_NAME, 'h2')

    assert element.text == 'Welcome, luxe@shetest.co.uk'

    #2
    book_places_list = chrome_driver.find_elements(By.LINK_TEXT, 'Book Places')
    purchase_link = book_places_list[0]
    purchase_link.click()
    time.sleep(0)
    element = chrome_driver.find_element(By.TAG_NAME, 'h2')

    assert 'Test Competition' in element.text

    #3
    places_field = chrome_driver.find_element(By.NAME, 'places')
    places_field.send_keys(32)
    places_field.send_keys(Keys.ENTER)
    time.sleep(0)
    element = chrome_driver.find_elements(By.TAG_NAME, 'li')

    assert element[0].text == 'You cannot use more points then you have !'

    #4
    book_places_list = chrome_driver.find_elements(By.LINK_TEXT, 'Book Places')
    purchase_link = book_places_list[0]
    purchase_link.click()
    time.sleep(0)
    element = chrome_driver.find_element(By.TAG_NAME, 'h2')
    places_field = chrome_driver.find_element(By.NAME, 'places')
    places_field.send_keys(9)
    places_field.send_keys(Keys.ENTER)
    time.sleep(0)
    element = chrome_driver.find_elements(By.TAG_NAME, 'li')

    assert element[0].text == 'This competition does not have enough places'


def test_negative_numbers_and_more_than_12_places():
    """
    1 - User connect with valid mail
    2 - User want book place in Future Competition and click it
    3 - User attempt to purchase 13 places
    4 - User attempt to enter negative numbers
    """

    #1
    chrome_driver.get("http://127.0.0.1:5000")
    email_field = chrome_driver.find_element(By.NAME, 'email')
    email_field.send_keys('luxe@shetest.co.uk')
    email_field.send_keys(Keys.ENTER)
    time.sleep(0)
    element = chrome_driver.find_element(By.TAG_NAME, 'h2')

    assert element.text == 'Welcome, luxe@shetest.co.uk'

    #2
    book_places_list = chrome_driver.find_elements(By.LINK_TEXT, 'Book Places')
    purchase_link = book_places_list[1]
    purchase_link.click()
    time.sleep(0)
    element = chrome_driver.find_element(By.TAG_NAME, 'h2')

    assert 'Future Competition' in element.text

    #3
    places_field = chrome_driver.find_element(By.NAME, 'places')
    places_field.send_keys(13)
    places_field.send_keys(Keys.ENTER)
    time.sleep(0)
    element = chrome_driver.find_elements(By.TAG_NAME, 'li')

    assert 'You cannot take more than 12 places' in element[0].text

    #4
    book_places_list = chrome_driver.find_elements(By.LINK_TEXT, 'Book Places')
    purchase_link = book_places_list[1]
    purchase_link.click()
    time.sleep(0)
    element = chrome_driver.find_element(By.TAG_NAME, 'h2')
    places_field = chrome_driver.find_element(By.NAME, 'places')
    places_field.send_keys(-2)
    places_field.send_keys(Keys.ENTER)
    time.sleep(0)
    element = chrome_driver.find_elements(By.TAG_NAME, 'li')

    assert 'You cannot enter negative number' in element[0].text


def test_past_future_competition():
    """
    1 - User connect with valid mail
    2 - User select a future competition
    3 - User see the past competition is not available because is a past competition
    """

    #1
    chrome_driver.get("http://127.0.0.1:5000")
    email_field = chrome_driver.find_element(By.NAME, 'email')
    email_field.send_keys('luxe@shetest.co.uk')
    email_field.send_keys(Keys.ENTER)
    time.sleep(0)
    element = chrome_driver.find_element(By.TAG_NAME, 'h2')

    assert element.text == 'Welcome, luxe@shetest.co.uk'

    #2
    book_places_list = chrome_driver.find_elements(By.LINK_TEXT, 'Book Places')
    purchase_link = book_places_list[1]
    purchase_link.click()
    time.sleep(0)
    element = chrome_driver.find_element(By.TAG_NAME, 'h2')

    assert 'Future Competition' in element.text

    #3
    chrome_driver.get("http://127.0.0.1:5000")
    email_field = chrome_driver.find_element(By.NAME, 'email')
    email_field.send_keys('luxe@shetest.co.uk')
    email_field.send_keys(Keys.ENTER)
    time.sleep(0)
    book_places_list = chrome_driver.find_elements(By.TAG_NAME, 'li')
    purchase_link = book_places_list[4]
    past_message = purchase_link.find_element(By.TAG_NAME, 'a')

    assert 'Past Competition' in purchase_link.text
    assert '[The competition Past Competition is already passed]' in past_message.text

    chrome_driver.quit()
