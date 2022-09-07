from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

import time

options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])

chrome_driver = webdriver.Chrome(options=options, service=Service(ChromeDriverManager().install()))


def test_login_logout():
    """
    1 - User login with valid email
    2 - User logout
    """


    #1
    chrome_driver.get("http://127.0.0.1:5000")
    email_field = chrome_driver.find_element(By.NAME, 'email')
    email_field.send_keys('luxe@shetest.co.uk')
    email_field.send_keys(Keys.ENTER)
    time.sleep(0)
    element = chrome_driver.find_element(By.TAG_NAME, 'h2')

    assert element.text == 'Welcome, luxe@shetest.co.uk'

    logout = chrome_driver.find_element(By.LINK_TEXT, 'Logout')
    logout.click()

    element = chrome_driver.find_element(By.TAG_NAME, 'h1')

    assert element.text == 'Welcome to the GUDLFT Registration Portal!'


def test_login_invalid():
    """
    1 - Unlogged User click on display board
    2 - User log with unvalid email
    """

    #1
    chrome_driver.get("http://127.0.0.1:5000")
    display_board = chrome_driver.find_element(By.LINK_TEXT, 'Clubs Board')
    display_board.click()
    time.sleep(0)
    element = chrome_driver.find_element(By.TAG_NAME, "h1")

    assert element.text == 'GUDLFT Display Clubs Board !'

    #2
    index = chrome_driver.find_element(By.LINK_TEXT, 'Index')
    index.click()
    time.sleep(0)
    element = chrome_driver.find_element(By.TAG_NAME, 'h1')

    assert element.text == 'Welcome to the GUDLFT Registration Portal!'

    chrome_driver.close()