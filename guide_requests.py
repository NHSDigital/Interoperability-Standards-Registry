import requests
from bs4 import BeautifulSoup
from asset_scraper import get_variables

def get_new_guides(url):
    from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.core.utils import ChromeType
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

chrome_service = Service(ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install())

chrome_options = Options()
options = [
    "--headless",
    "--disable-gpu",
    "--window-size=1920,1200",
    "--ignore-certificate-errors",
    "--disable-extensions",
    "--no-sandbox",
    "--disable-dev-shm-usage"
]
for option in options:
    chrome_options.add_argument(option)

driver = webdriver.Chrome(service=chrome_service, options=chrome_options)

driver.get(url)
return driver.title

get_new_guides('https://simplifier.net/HL7FHIRUKCoreR4/~guides')

def get_guides(url):
    ### NO LONGER WORKS DUE TO JSCRIPT. USE https://selenium-python.readthedocs.io/ 
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    results = soup.find(id="guides")
    print(f"{url}:{results}\n\n")

    title_elements = results.find_all("div", class_="title")
    desc_elements = results.find_all("div", class_="description")
    tr_tags = results.find_all("tr", onclick=True)

    titles = []
    for title in title_elements:
        titles.append(title.text)

    descriptions = []
    for description in desc_elements:
        descriptions.append(description.text)

    relative_urls = []
    for tr in tr_tags:
        onclick_value = tr['onclick']
        link = onclick_value.split('"')[1]
        relative_urls.append(link)
    try:
       titles.pop(0) #remove empty title fond from other part of webpage
    except:
       pass
    print(titles)
    guides = zip(titles,relative_urls, descriptions) 
    return guides

def sort_ukcore(guides):
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

'''#### TODO:Import open JSON and getJSON
Get urls from variables.json ####
'''
repo_to_url = get_variables('main_variables.json', 'repo_to_url')
project_urls = repo_to_url.values()
print(project_urls)

for url in project_urls:
    print(url+'/~guides')
    guides = get_guides(url+'/~guides')
    if 'hl7uk' in url:
        guides = sort_ukcore(guides)
    print(f"url: {list(guides)}\n\n")

'''#### Create webpage ####'''

page = requests.get('https://simplifier.net/HL7FHIRUKCoreR4/~guides')
soup = BeautifulSoup(page.content, "html.parser")
results = soup.find(id="guides")
title_elements = results.find_all("div", class_="title")
print(title_elements)