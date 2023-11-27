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
from .models import driver_status
# from .driver_variable import need_to_restart_driver,user_driver_dict

from .bot import Bot
def GetActiveChromeSelenium(hashtag:str):
    breakpoint()
    need_to_restart_driver = {}
    user_driver_dict = {}
    if driver_status.objects.all().count() :
        driver_status.objects.create(user_data = {'key' : 'value'})
    driver_obj = driver_status.objects.all().count()

    if need_to_restart_driver == True:
        all_active_user = instagram_accounts.objects.filter(status='ACTIVE')
        for user in all_active_user:
            user_driver_dict[user] = {
                "activate" : True,
                "driver" : Bot(user=user,start_drivers=need_to_restart_driver),
                "busy" : False,
                "user" : user
            }
            
        need_to_restart_driver = False if need_to_restart_driver == True else False
    
    for user, data in user_driver_dict.items():
        if data['busy'] == False :
            data['busy'] = True
            return Bot(user=user_driver_dict[user]['user'],extract_hashtag=True,driver= user_driver_dict[user]['driver'])

    else : 
        return False