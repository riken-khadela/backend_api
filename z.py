from selenium import webdriver
from selenium.webdriver.chrome.service import Service

chromedriver_path = '/home/dell/Desktop/selenium_server/chromedriver'
chrome_binary_path = '/usr/bin/google-chrome'

chrome_options = webdriver.ChromeOptions()
chrome_options.binary_location = chrome_binary_path

# chrome_options.add_argument('--headless')  
chrome_options.add_argument('--no-sandbox')  
chrome_options.add_argument('--disable-dev-shm-usage')  

service = Service(chromedriver_path)
driver = webdriver.Chrome(service=service, options=chrome_options)
breakpoint()
website_url = 'https://example.com'

driver.get(website_url)

driver.quit()
