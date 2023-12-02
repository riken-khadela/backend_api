from lib2to3.pgen2 import driver
from .models import instagram_accounts
import random, time, os, json
import undetected_chromedriver as uc
from selenium import webdriver  
from selenium_stealth import stealth
from selenium.common.exceptions import NoSuchElementException, TimeoutException,ElementNotInteractableException,NoSuchElementException,WebDriverException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from dotenv import load_dotenv
load_dotenv()

from .bot import Bot
def GetActiveChromeSelenium():

    user_driver_dict = {}
    all_active_user = instagram_accounts.objects.filter(status='ACTIVE')
    for user in all_active_user : 
        i_bot = Bot(user=user)
        driver = i_bot.return_driver()
        if driver != False :
            user_driver_dict[user.username] = {
                'driver' : driver,
                'status' : True
                }
        
    return user_driver_dict

def scrape_hashtags(username,hashtag, driver):
    user = instagram_accounts.objects.filter(username=username).first()
    i_bot = Bot(user=user)
    return  i_bot.extract_tag(hashtag,driver)