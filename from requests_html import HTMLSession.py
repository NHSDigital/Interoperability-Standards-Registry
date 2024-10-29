from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time

# Configure Selenium options
options = Options()
options.add_argument('--headless')  # Run in headless mode (no browser window)
options.add_argument('--disable-gpu')
options.add_argument('--no-sandbox')

# Initialize the Chrome WebDriver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# Define the URL
url = "https://simplifier.net/HL7FHIRUKCoreR4/~guides"

try:
    # Open the URL
    driver.get(url)
    time.sleep(3)  # Wait for the page to fully load (adjust as necessary)

    # Extract the page title
    page_title = driver.title
    print("Page Title:", page_title)

    # Extract main content (customize the selector as needed)
    main_content = driver.find_element(By.TAG_NAME, 'body').text
    print("Main Content:", main_content[:500])  # Print first 500 characters for example

finally:
    # Close the browser
    driver.quit()