from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from asset_scraper import get_variables

'''
Scrapes any project within the main_variables.json file, output is an html page within the registry that includes each IG's title, url, and decription.
Uses Selenium due to needing to wait until the guides are loaded on the website

DOCS
https://www.selenium.dev/selenium/docs/api/py/index.html
https://www.crummy.com/software/BeautifulSoup/bs4/doc/
'''


def get_guides(url):
    ''' Opens Simplifier Guides page for a project and scrapes all IGs for title, url and description. Note that as this does not include login details no private IGS are scraped'''
    driver = webdriver.Firefox()
    driver.get(url)
    
    # This waits until the urls are loaded before getting webpage which are under class="guides-table-row"
    timeout = 5
    try:
        element_present = EC.presence_of_element_located((By.CLASS_NAME, 'guides-table-row')) # Ensure the relative urls are loaded before getting page
        WebDriverWait(driver, timeout).until(element_present)
    except TimeoutException:
        print ("Timed out waiting for page to load")

    soup = BeautifulSoup(driver.page_source, 'html.parser')
    driver.close()
    results = soup.find(id="guides")

    title_elements = results.find_all("div", class_="title")
    desc_elements = results.find_all("div", class_="description")
    relative_urls = [tr['data-url'] for tr in results.find_all("tr", class_="guides-table-row")]

    titles = []
    for title in title_elements:
        titles.append(title.text.strip()) # strips all \n and whitespace

    descriptions = []
    for description in desc_elements:
        descriptions.append(description.text)
    
    prefix = 'https://simplifier.net'
    relative_urls = [prefix+x.split('?')[0] for x in relative_urls] #adds prefix and removes ?version=current so that guide opens with 'default'

    guides = list(zip(titles,relative_urls, descriptions)) 
    return guides

def sort_ukcore(guides):
    ''' used to ensure latest uk core stu version is shown at the top '''
    igs = []
    other_guides = []
    for tup in guides:
        if 'UK Core Implementation Guide' in tup[0] and 'Development' not in tup[0]:
            igs.append(tup)
        else:
            other_guides.append(tup)
    igs = sorted(igs,reverse=True)
    other_guides = sorted(other_guides)
    guides = igs.append(other_guides)
    return guides

repo_to_url = get_variables('main_variables.json', 'repo_to_url')
project_urls = repo_to_url.values()
print(project_urls)

for url in project_urls:
    print(url+'/~guides')
    guides = get_guides(url+'/~guides')
    if 'hl7uk' in url:
        guides = sort_ukcore(guides)
    print(f"url: {list(guides)}\n\n")

'''
#### Create webpage ####
This creates the html for the page. Note: it is hard to read, Flask is potentially a better way '''
