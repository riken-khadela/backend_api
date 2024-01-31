from audioop import avg
import datetime
import random, time, os, json
from selenium_stealth import stealth
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import subprocess
from selenium import webdriver  
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
from urllib.parse import unquote

from home.cron import random_sleep

chromedriver_path = os.path.join(os.getcwd(),'chromedriver')
chrome_binary_path = '/usr/bin/google-chrome'
class Bot():
    def __init__(self,user) :
        self.user = user
        self.username = user.username
        self.password = user.password

    def return_driver(self) : 
        # subprocess.run(['pkill', 'chrome'])
        self.get_driver() 
        return self.check_login() 

    def get_local_driver(self):
        """Start webdriver and return state of it."""
        from selenium import webdriver
        driver = ''
        for _ in range(30):
            options = webdriver.ChromeOptions()
            options.add_argument('--lang=en')  # Set webdriver language to English.
            options.add_argument('log-level=3')  # No logs is printed.
            options.add_argument('--mute-audio')  # Audio is muted.
            options.add_argument("--enable-webgl-draft-extensions")
            options.add_argument('--mute-audio')
            options.add_argument("--ignore-gpu-blocklist")
            options.add_argument('--disable-dev-shm-usage')
            # options.add_argument('--headless')
            prefs = {"credentials_enable_service": True,
                    'profile.default_content_setting_values.automatic_downloads': 1,
                'download.prompt_for_download': False,  # Optional, suppress download prompt
                'download.directory_upgrade': True,
                'safebrowsing.enabled': True ,
                "profile.password_manager_enabled": True}
            options.add_experimental_option("prefs", prefs)
            options.add_argument('--no-sandbox')
            options.add_argument('--start-maximized')    
            options.add_argument('--disable-dev-shm-usage')
            options.add_argument("--ignore-certificate-errors")
            options.add_argument("--enable-javascript")
            options.add_argument("--enable-popup-blocking")
            try:
                # subprocess.run(['pkill', 'chrome'])
                driver = webdriver.Chrome(options=options)
                driver.get('https://www.google.com')
                driver.save_screenshot('aa.png')
                driver.current_url
                driver.execute_script("window.open('about:blank','secondtab');")
                break
            except Exception as e:
                print(e)
        
        self.driver = driver
        return self.driver
    
    def get_driver(self):
        """Start webdriver and return state of it."""
        driver = ''
        for _ in range(30):
            """Start webdriver and return state of it."""
            from undetected_chromedriver import Chrome, ChromeOptions
            options = ChromeOptions()
            options.add_argument('--lang=en')  # Set webdriver language to English.
            options.add_argument('log-level=3')  # No logs is printed.
            options.add_argument('--mute-audio')  # Audio is muted.
            options.add_argument("--enable-webgl-draft-extensions")
            options.add_argument('--mute-audio')
            options.add_argument("--ignore-gpu-blocklist")
            options.add_argument('--disable-dev-shm-usage')
            options.add_argument('--headless')
            prefs = {"credentials_enable_service": True,
                    'profile.default_content_setting_values.automatic_downloads': 1,
                'download.prompt_for_download': False,  # Optional, suppress download prompt
                'download.directory_upgrade': True,
                'safebrowsing.enabled': True ,
                "profile.password_manager_enabled": True}
            options.add_experimental_option("prefs", prefs)
            options.add_argument('--no-sandbox')
            options.add_argument('--start-maximized')    
            options.add_argument('--disable-dev-shm-usage')
            options.add_argument("--ignore-certificate-errors")
            options.add_argument("--enable-javascript")
            options.add_argument("--enable-popup-blocking")
            try:
                # subprocess.run(['pkill', 'chrome'])
                driver = Chrome(options=options,version_main=119,headless=False)
                driver.get('https://www.google.com')
                driver.save_screenshot('aa.png')
                break
            except Exception as e:
                print(e)
        
        self.driver = driver
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
        import time, os
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
        self.driver.get(f'https://www.instagram.com/'+self.username+'/')
        if os.path.exists('cookies/coockies_'+str(self.username)+'.txt') :
            with open('cookies/coockies_'+str(self.username)+'.txt', 'r') as file:
                cookies = eval(file.read())  
            for cookie in cookies:
                self.driver.add_cookie(cookie)
            self.driver.refresh()
        self.find_element('a tag','a',By.TAG_NAME)
        time.sleep(1)
        # https://www.instagram.com/accounts/edit/
        # edit_profile_ele = self.find_element('Edit profile','//a[text()="Edit Profile"]')
        # if not edit_profile_ele :
        #     all_a = [i for i in self.driver.find_elements(By.TAG_NAME,'a') if 'log in' in i.text.lower()]
            
        #     if all_a :
        #         all_a[0].click()
        #         if 'login' in self.driver.current_url.lower() :
        #             self.input_text(self.username,'username',"//input[@name='username']",By.XPATH)
        #             self.input_text(self.password,'password',"//input[@name='password']",By.XPATH)
        #             self.click_element('submit',"//button[@type='submit']",By.XPATH)
        #             self.random_sleep()
        #             cookies = self.driver.get_cookies()
        #             with open('cookies/coockies_'+str(self.username)+'.txt', 'w') as file: file.write(str(cookies))
        #             if 'onetap' in self.driver.current_url :
        #                 save_info_btn = [ i for i in  self.driver.find_elements(By.TAG_NAME,'button') if 'save info' in i.text.lower()]
        #                 if save_info_btn : 
        #                     save_info_btn[-1].click()
        #     time.sleep(5)
        # else :
        print('user has been logged 1!')
        self.driver.get('https://www.instagram.com/')
        self.click_element('search btn',"//a[@href='#']")
        self.click_element('notification not now',"//button[text()='Not Now']")
            
        return self.driver
        print("user hasn't been logged !")
        return False
    
    def TestRunDriver(self,driver : webdriver):
        self.driver = driver
        try :
            self.driver.current_url
            return True
        except : return False

    def scrape_tag_extra_data(self):
        allpostmaindiv = self.find_element('all post main element','/html/body/div[2]/div/div/div[2]/div/div/div[1]/div[1]/div[2]/section/main/article/div/div/div')
        actions = ActionChains(self.driver)
        for _ in range(30) :
            allAelement = allpostmaindiv.find_elements(By.TAG_NAME,'a')
            if len(allAelement) >= 30 : break
            else : time.sleep(0.2)
        json_ = {}
        reel = 0
        post = 0
        post_on_screen = 0
                # self.driver.execute_script("arguments[0].scrollIntoView(true);", a_tag)
        
        for a_tag in allAelement :
                post_on_screen += 1
                if post_on_screen%9 == 0 : 
                    # self.driver.execute_script("arguments[0].scrollIntoView(true);", a_tag)
                    actions.move_to_element(a_tag).perform()
                tmp = {}
                tmp['comments'] = '0'
                tmp['likes'] = '0'
                li_ele = a_tag.find_elements(By.TAG_NAME,'li')
                if li_ele : 
                    post_like = li_ele[0].find_elements(By.TAG_NAME,'span') if len(li_ele) >= 1 else []
                    if post_like :
                        post_like = post_like[1].text if len(post_like) > 1 else '0'
                        if not post_like : post_like = '0'
                        if 'K' in post_like : 
                            post_like = int(float(str(post_like).replace('K',''))*1000)
                        elif 'M' in post_like : 
                            post_like = int(float(str(post_like).replace('K',''))*1000000)
                        tmp['likes'] = post_like
                    
                    post_comment = li_ele[1].find_elements(By.TAG_NAME,'span') if len(li_ele) > 1 else []
                    if post_comment :
                        post_comment = post_comment[1].text if len(post_comment) > 1 else '0'
                        if not post_comment : post_comment = '0'
                        if 'K' in post_comment : 
                            post_comment = int(float(str(post_comment).replace('K',''))*1000)
                        elif 'M' in post_comment : 
                            post_comment = int(float(str(post_comment).replace('K',''))*1000000)
                        tmp['comments'] = post_comment
                
                svg_eles = a_tag.find_elements(By.TAG_NAME,'svg')
                if svg_eles :
                    svg_eles = svg_eles[0]
                    if svg_eles.get_attribute('aria-label') == "Clip" :
                        reel += 1
                post += 1
                json_[allAelement.index(a_tag)] = tmp
                
            
                
        
        if json_ :
            reels_perntage = (reel/post)*100
            avg_likes = [ int(str(value['likes']).replace(',','')) for keys,value in json_.items() ]
            avg_likes = sum(avg_likes)/len(avg_likes)
            avg_cmt = [ int(str(value['comments']).replace(',','')) for keys,value in json_.items() ]
            avg_cmt = sum(avg_cmt)/len(avg_cmt)
            
            return { "likes" : avg_likes,'comment' : avg_cmt, 'reels' : f"{int(reels_perntage)} %"}
        
        else : {}
    
    def close_others_tab(self):
        for window in self.driver.window_handles[1:]:
                self.driver.switch_to.window(window)
                self.driver.close()
        self.driver.switch_to.window(self.driver.window_handles[0])
        ...
    
    def extract_tag(self,tag : str,driver : webdriver):
        self.driver = driver
        responsee = {}
        
        try:
            
            search_input = self.input_text(f"#{tag}",'input',"//input[@aria-label='Search input']",By.XPATH,timeout=0)
            
            if search_input :
                for _ in range(10) :
                    time.sleep(1)
                    all_hashtah_links_elees = []
                    for _ in range(50):
                        all_hashtah_links_elees = self.driver.find_elements(By.TAG_NAME,'a')
                        if all_hashtah_links_elees : break
                        time.sleep(0.1)
                    
                    all_hashtah_links = [ i for i in self.driver.find_elements(By.TAG_NAME,'a') if '/explore/tags/' in i.get_attribute('href')]
                    for a_tag in all_hashtah_links :
                        try:
                            responsee[all_hashtah_links.index(a_tag)+1] = {
                                "hastag" : unquote( a_tag.get_attribute('href').split('/explore/tags/')[-1].replace('/',''), encoding='utf-8'),
                                "total_post" : a_tag.find_element(By.XPATH,'.//div[1]/div/div/div[2]/div/div/span[2]/span/span/span').text, 
                                "link" : a_tag.get_attribute('href')
                                }
                        except : ...
                    
                    scrapped_likes_comment = 0
                    for key, json_ in responsee.items() :
                        if scrapped_likes_comment >= 1 : break
                        self.driver.switch_to.window(self.driver.window_handles[-1])
                        print(datetime.datetime.now())
                        self.driver.get(json_['link'])
                        print(datetime.datetime.now())
                        sucess = self.scrape_tag_extra_data()
                        if sucess : 
                            responsee[key]['likes'] = int(sucess['likes'])
                            responsee[key]['comment'] = int(sucess['comment'])
                            responsee[key]['reels'] = sucess['reels']
                            scrapped_likes_comment += 1
                        print(responsee[key])
                        self.close_others_tab()
                    
                    if  len(all_hashtah_links) < 1:
                        time.sleep(1)
                    else :
                        cookies = self.driver.get_cookies()
                        with open('cookies/coockies_'+str(self.username)+'.txt', 'w') as file:
                            file.write(str(cookies))

                        return responsee
                
                self.input_text(f"",'search input',"//input[@aria-label='Search input']",By.XPATH,timeout=0)
                
            else : 
                self.click_element('search btn',"//a[@href='#']")
        except Exception as e: 
            print(e)
        finally :
            self.close_others_tab()

        return []