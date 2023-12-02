import random, time, os, json
import undetected_chromedriver as uc
from selenium import webdriver  
from selenium_stealth import stealth
from selenium.common.exceptions import NoSuchElementException, TimeoutException,ElementNotInteractableException,NoSuchElementException,WebDriverException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

class Bot():
    def __init__(self,user) :
        self.user = user
        self.username = user.username
        self.password = user.password

        
                
    def return_driver(self) : 
        self.get_driver(self.user.id) 
        return self.check_login() 

    def get_driver(self,profile_id : int,add_cybeghost=False):
        """Start webdriver and return state of it."""
        from selenium.webdriver.chrome.options import Options
        options = Options()

        options = uc.ChromeOptions()
        options.add_argument('--lang=en')  # Set webdriver language to English.
        options.add_argument('log-level=3')  # No logs is printed.
        options.add_argument('--mute-audio')  # Audio is muted.
        options.add_argument("--enable-webgl-draft-extensions")
        options.add_argument('--mute-audio')
        options.add_argument("--ignore-gpu-blocklist")
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--headless')
        options.add_argument('--disable-dev-shm-usage')
        
        options.add_argument(f"user-data-dir={os.path.join(os.getcwd(),f'profiles','profile_'+str(profile_id))}")

        prefs = {"credentials_enable_service": True,
                 'profile.default_content_setting_values.automatic_downloads': 1,
            'download.prompt_for_download': False,  # Optional, suppress download prompt
            'download.directory_upgrade': True,
            'safebrowsing.enabled': True ,
            "profile.password_manager_enabled": True}
        options.add_experimental_option("prefs", prefs)
        if add_cybeghost :
            options.add_extension('./Stay-secure-with-CyberGhost-VPN-Free-Proxy.crx')
        options.add_extension('./Buster-Captcha-Solver-for-Humans.crx')
        options.add_argument('--no-sandbox')
        options.add_argument('--start-maximized')    
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument("--ignore-certificate-errors")
        options.add_argument("--enable-javascript")
        options.add_argument("--enable-popup-blocking")
        # options.add_argument('--headless')
        for _ in range(30):
            try:
                self.driver = webdriver.Chrome(options=options)
                break
            except Exception as e:
                print(e)
        stealth(self.driver,
            languages=["en-US", "en"],
            vendor="Google Inc.",
            platform="Win32",
            webgl_vendor="Intel Inc.",
            renderer="Intel Iris OpenGL Engine",
            fix_hairline=True,
            )
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
        except (NoSuchElementException, TimeoutException) as e:
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
                except ElementNotInteractableException :...
    
    def ScrollDown(self,px):
        self.driver.execute_script(f"window.scrollTo(0, {px})")
    
    def get_cookies(self,website :str):
        cookies = self.driver.get_cookies()
        with open(os.path.isfile(self.cookies_path), 'w', newline='') as outputdata:
            json.dump(cookies, outputdata)
        return cookies
    
    def ensure_click(self, element, timeout=3):
        try:
            WebDriverWait(self.driver, timeout).until(EC.element_to_be_clickable(element))
            element.click()
        except WebDriverException:
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
    
    def load_cookies(self):
        if os.path.isfile(self.cookies_path):
            with open(self.cookies_path,'rb') as f:cookies = json.load(f)
            for item in cookies:
                self.driver.add_cookie(item)
            self.random_sleep()

    def CloseDriver(self):
        try: 
            self.driver.quit()
            print('Driver is closed !')
        except Exception as e: ...

    def check_login(self) :
        self.driver.get(f'https://www.instagram.com/'+self.username+'/')
        all_a = [i for i in self.driver.find_elements(By.TAG_NAME,'a') if 'log in' in i.text.lower()]
        if all_a :
            all_a[-1].click()
            if 'login' in self.driver.current_url.lower() :
                self.input_text(self.username,'username',"//input[@aria-label='Phone number, username, or email']",By.XPATH)
                self.input_text(self.password,'password',"//input[@aria-label='Password']",By.XPATH)
                self.click_element('submit',"//button[@type='submit']",By.XPATH)
                self.random_sleep(5,7)
                if 'onetap' in self.driver.current_url :
                    save_info_btn = [ i for i in  self.driver.find_elements(By.TAG_NAME,'button') if 'save info' in i.text.lower()]
                    if save_info_btn : 
                        save_info_btn[-1].click()

        self.random_sleep(10,15)
        edit_profile_btn = [ i for i in  self.driver.find_elements(By.TAG_NAME,'a') if 'edit profile' in i.text.lower()]
        if edit_profile_btn :
            self.driver.get('https://www.instagram.com/')
            self.click_element('search btn',"//a[@href='#']")
            return self.driver
        return False

    def extract_tag(self,tag : str,driver):
        self.driver = driver
        self.input_text(f"#{tag}",tag,"//input[@aria-label='Search input']",By.XPATH)
        for _ in range(10) :
            all_hashtah_links = [ i.get_attribute('href').split('/explore/tags/')[-1].replace('/','') for i in self.driver.find_elements(By.TAG_NAME,'a') if '/explore/tags/' in i.get_attribute('href')]
            if not all_hashtah_links :
                time.sleep(1)
            else :
                return all_hashtah_links
        return []
# Bot()