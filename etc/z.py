import undetected_chromedriver as uc
from selenium import webdriver

# Install undetected_chromedriver if not already installed

# Set up undetected Chrome options
options = uc.ChromeOptions()
options.headless = False  # Set to True for headless browsing
# Add any other options or configurations as needed

# Create the WebDriver using undetected_chromedriver
driver = uc.Chrome(options=options)

# Navigate to a website
driver.get("https://www.google.com")
breakpoint()
# Perform actions or interact with the webpage
# Example: Find an element and print its text
element = driver.find_element_by_xpath("//h1")
print("Element text:", element.text)

# Close the WebDriver session
driver.quit()
