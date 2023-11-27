# utils.py
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
# from .models import InstagramAccount

def get_related_hashtags(driver, hashtag):
    # Your scraping logic here
    # Use the provided driver to scrape related hashtags for the given hashtag
    ...

def create_driver(username, password):
    # Create a new instance of the WebDriver
    driver = webdriver.Chrome()  # You can choose a different browser or driver

    # Log in to Instagram using provided credentials
    driver.get("https://www.instagram.com/accounts/login/")
    time.sleep(2)  # Add a sleep to wait for the page to load

    username_input = driver.find_element(By.NAME, 'username')
    password_input = driver.find_element(By.NAME, 'password')

    username_input.send_keys(username)
    password_input.send_keys(password)
    password_input.send_keys(Keys.ENTER)

    # Wait for the login to complete
    WebDriverWait(driver, 10).until(EC.url_changes("https://www.instagram.com/"))

    return driver

def get_available_driver():
    # Check the availability of drivers
    accounts = InstagramAccount.objects.all()

    for account in accounts:
        if not account.is_busy:
            return account

    return None

def scrape_instagram_hashtags(hashtag):
    # Get an available driver
    account = get_available_driver()

    if account:
        # Mark the account as busy
        account.is_busy = True
        account.save()

        # Create a driver for the account
        driver = create_driver(account.username, account.password)

        # Get related hashtags
        related_hashtags = get_related_hashtags(driver, hashtag)

        # Mark the account as not busy
        account.is_busy = False
        account.save()

        # Close the driver
        driver.quit()

        return related_hashtags
    else:
        return False
