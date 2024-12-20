# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver import FirefoxOptions
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from asset_scraper import get_variables
import os

'''
Scrapes any project within the main_variables.json file, output is an html page within the registry that includes each IG's title, url, and decription.
Uses Selenium due to needing to wait until the guides are loaded on the website

DOCS
https://www.selenium.dev/selenium/docs/api/py/index.html
https://www.crummy.com/software/BeautifulSoup/bs4/doc/
'''


def get_guides(url):
    ''' Opens Simplifier Guides page for a project and scrapes all IGs for title, url and description. Note that as this does not include login details no private IGS are scraped'''
    opts = FirefoxOptions()
    opts.add_argument("--headless")
    driver = webdriver.Firefox(options=opts)
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
    return soup

def get_attributes(soup, url, guides_dict):
    ''' uses soup results to find header info and guides info. Output is guides_dict in the form {Organisation_name[0]:[description,[project_name[0]:description,[(guide_name[0], guide_relative_url[0], guide description[0]),(...)], ...],...]}. Note that as this does not include login details so no private IGS are scraped'''
    header = soup.find("header")
    organization = header.find("div", class_="pre-title").find("a")
    project = header.find("h1", class_="title").text.strip()
    project_description = header.find("div", class_="description").text.strip()

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
    if organization not in guides_dict.keys():
        guides_dict.update({organization:[{project:[url,project_description,guides]}]})
    else:
        guides_dict[organization].append({project:[url,project_description,guides]})
    return guides_dict

def sort_ukcore(guides):
    ''' used to ensure latest uk core stu version is shown at the top '''
    igs = []
    other_guides = []
    for tup in guides:
        if 'stu' in tup[0].lower():
            igs.append(tup)
        else:
            other_guides.append(tup)
    igs_sorted = sorted(igs,reverse=True)
    other_guides_sorted = sorted(other_guides)
    guides_sorted = igs_sorted+other_guides_sorted
    return guides_sorted


'''
#### Create webpage ####
This creates the html for the page. Note: it is hard to read, Flask is potentially a better way '''

path = './guides/Interoperability-Standard-Registry-Guide/About-Interoperability/FHIR-Guides/'

def guides_to_html(org, projects):
    page = str(path+'/'+org.text+'.page.md').replace(" ","-")
    if os.path.exists(page):
        os.remove(page)
    md_file = open(page,"w")
    print(f'''

# {org}

<br>''', file=md_file)
    for project in projects:
        for project_name, guides in project.items():
            print(f'''

<a href="{guides[0]+'" class="project-banner">'+project_name}
<span class="description">{guides[1]}</span>
</a>

<br>

<div class="project-container">
    ''',file=md_file)
            
            for guide in guides[2]:
                print(f'''
<a href="{guide[1]}" class="child-title">
<div class="title">{guide[0]}</div>
<div class="description">{guide[2]}</div>
</a>
    ''',file=md_file)
        print("</div>\n<b><br>\n\n---\n\n",file=md_file)
    
    md_file.close()
    return

repo_to_url = get_variables('main_variables.json', 'repo_to_url')
project_urls = repo_to_url.values()

guides_dict = {}
for url in project_urls:
    soup = get_guides(url+'/~guides')
    guides_dict = get_attributes(soup, url, guides_dict)
print(f"guides_dict:{guides_dict}\n")
for org, projects in guides_dict.items():
    if 'uk' in org.text.lower() and 'stu' not in org.text.lower():
        print(f"uk in org:{org}\nwith projects:{projects}\n")
        for project in projects:
            for project_name, guides in project.items():
                if 'core' in project_name.lower():
                    guides[2] = sort_ukcore(guides[2])
    print(f"org:{org},\nproject:{projects}\n")
    guides_to_html(org, projects)
