import random, time, os, json
from selenium_stealth import stealth
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import logging
from selenium import webdriver  
from selenium.webdriver.chrome.service import Service
chromedriver_path = os.path.join(os.getcwd(),'chromedriver')
chrome_binary_path = '/usr/bin/google-chrome'
class Bot():
    def __init__(self,user) :
        self.user = user
        self.username = user.username
        self.password = user.password

        
                
    def return_driver(self) : 
        self.get_driver(self.user.id) 
        return self.check_login() 

    def get_driver(self,profile_id : int):
        """Start webdriver and return state of it."""
        from selenium.webdriver.chrome.options import Options
        options = webdriver.ChromeOptions()
        service = Service(chromedriver_path)

        options.add_argument('--no-sandbox')
        options.add_argument('--autoplay-policy=no-user-gesture-required')
        # options.add_argument('--start-maximized')    
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument("--disable-blink-features")
        options.add_argument("--ignore-certificate-errors")
        options.add_argument("--enable-javascript")
        options.add_argument("--disable-notifications")
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_argument("--enable-popup-blocking")
        options.add_experimental_option('useAutomationExtension', False)
        options.add_experimental_option("excludeSwitches", [
            "enable-logging",
            "enable-automation",
            "ignore-certificate-errors",
            "safebrowsing-disable-download-protection",
            "safebrowsing-disable-auto-update",
            "disable-client-side-phishing-detection"])
        options.add_argument("disable-infobars")
        options.add_argument(f"user-data-dir={os.path.join(os.getcwd(),f'profile','profile_'+str(profile_id))}")
        options.add_extension('cyberghost.crx')

        
        options.add_argument(f"user-data-dir={str(profile_id)}")
        options.add_argument('--profile-directory=Defualt')
        prefs = {"credentials_enable_service": True,
                 'profile.default_content_setting_values.automatic_downloads': 1,
            'download.prompt_for_download': False,  # Optional, suppress download prompt
            'download.directory_upgrade': True,
            'safebrowsing.enabled': True ,
            "profile.password_manager_enabled": True}
        options.add_experimental_option("prefs", prefs)
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-gpu')
        options.add_argument("--ignore-certificate-errors")
        options.add_argument("--enable-javascript")
        options.add_argument("--enable-popup-blocking")
        # options.add_argument('--headless')
        
        options.add_argument('--start-maximized')    
        self.driver = webdriver.Chrome(service=service, options=options)
        
        return self.driver
    def find_element(self, element, locator, locator_type=By.XPATH,
            page=None, timeout=10,
            condition_func=EC.presence_of_element_located,
            condition_other_args=tuple()):
        """Find an element, then return it or None.
        If timeout is less than or requal zero, then just find.
        If it is more than zero, then wait for the element present.
        """
        try:
            if timeout > 0:
                wait_obj = WebDriverWait(self.driver, timeout)
                ele = wait_obj.until(EC.presence_of_element_located((locator_type, locator)))
                # ele = wait_obj.until( condition_func((locator_type, locator),*condition_other_args))
            else:
                print(f'Timeout is less or equal zero: {timeout}')
                ele = self.driver.find_element(by=locator_type,
                        value=locator)
            if page:
                print(
                    f'Found the element "{element}" in the page "{page}"')
            else:
                print(f'Found the element: {element}')
            return ele
        except Exception as e:
            if page:
                print(f'Cannot find the element "{element}"'
                        f' in the page "{page}"')
            else:
                print(f'Cannot find the element: {element}')
                
    def click_element(self, element, locator, locator_type=By.XPATH,
            timeout=10):
        """Find an element, then click and return it, or return None"""
        ele = self.find_element(element, locator, locator_type, timeout=timeout)
        
        if ele:
            self.driver.execute_script('arguments[0].scrollIntoViewIfNeeded();',ele)
            self.ensure_click(ele)
            print(f'Clicked the element: {element}')
            return ele

    def input_text(self, text, element, locator, locator_type=By.XPATH,
            timeout=10, hide_keyboard=True):
        """Find an element, then input text and return it, or return None"""
        
        ele = self.find_element(element, locator, locator_type=locator_type,
                timeout=timeout)
        
        if ele:
            for i in range(3):
                try: 
                    ele.clear()
                    ele.send_keys(text)
                    print(f'Inputed "{text}" for the element: {element}')
                    return ele    
                except  :...
    
    def ScrollDown(self,px):
        self.driver.execute_script(f"window.scrollTo(0, {px})")

    def ensure_click(self, element, timeout=3):
        try:
            WebDriverWait(self.driver, timeout).until(EC.element_to_be_clickable(element))
            element.click()
        except :
            self.driver.execute_script("arguments[0].click();", element)
    
    def new_tab(self):
        self.driver.find_element(By.XPATH,'/html/body').send_keys(Keys.CONTROL+'t')

    def random_sleep(self,a=3,b=7):
        random_time = random.randint(a,b)
        print('time sleep randomly :',random_time)
        time.sleep(random_time)

    def getvalue_byscript(self,script = '',reason=''):
        """made for return value from ele or return ele"""
        if reason :print(f'Script execute for : {reason}')
        else:
            print(f'execute_script : {script}')
        value = self.driver.execute_script(f'return {script}')  
        return value
    


    def CloseDriver(self):
        try: 
            self.driver.quit()
            print('Driver is closed !')
        except Exception as e: ...

    def check_login(self) :

        if os.path.exists('cookies/coockies_'+str(self.user.id)+'.txt') :
            with open('cookies/coockies_'+str(self.user.id)+'.txt', 'r') as file:
                cookies = eval(file.read())  
            for cookie in cookies:
                self.driver.add_cookie(cookie)

        self.driver.get(f'https://www.instagram.com/'+self.username+'/')
        self.random_sleep(5,10)
        breakpoint()
        

        all_a = [i for i in self.driver.find_elements(By.TAG_NAME,'a') if 'log in' in i.text.lower()]
        if all_a :
            all_a[0].click()
            if 'login' in self.driver.current_url.lower() :
                self.input_text(self.username,'username',"//input[@name='username']",By.XPATH)
                self.input_text(self.password,'password',"//input[@name='password']",By.XPATH)
                self.click_element('submit',"//button[@type='submit']",By.XPATH)
                self.random_sleep()
                cookies = self.driver.get_cookies()
                with open('cookies/coockies_'+str(self.user.id)+'.txt', 'w') as file: file.write(str(cookies))
                if 'onetap' in self.driver.current_url :
                    save_info_btn = [ i for i in  self.driver.find_elements(By.TAG_NAME,'button') if 'save info' in i.text.lower()]
                    if save_info_btn : 
                        save_info_btn[-1].click()
        edit_profile_btn = [ i for i in  self.driver.find_elements(By.TAG_NAME,'a') if 'edit profile' in i.text.lower()]
        if edit_profile_btn :
            print('user has been logged 1!')
            self.driver.get('https://www.instagram.com/')
            self.click_element('search btn',"//a[@href='#']")
            return self.driver
        print("user hasn't been logged !")
        return False

    def extract_tag(self,tag : str,driver):
        self.driver = driver
        self.input_text(f"#{tag}",tag,"//input[@aria-label='Search input']",By.XPATH)
        for _ in range(10) :
            all_hashtah_links = [ i.get_attribute('href').split('/explore/tags/')[-1].replace('/','') for i in self.driver.find_elements(By.TAG_NAME,'a') if '/explore/tags/' in i.get_attribute('href')]
            if  len(all_hashtah_links) < 1:
                time.sleep(1)
            else :
                return all_hashtah_links
        return []