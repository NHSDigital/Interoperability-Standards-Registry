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


'''
#### Create webpage ####
This creates the html for the page. Note: it is hard to read, Flask is potentially a better way '''

path = './guides/Interoperability-Standard-Registry-Guide/About-Interoperability/FHIR-Guides/'

def guides_to_html(title, guides):
    page = path+'/'+title+'s.page.md'
    if os.path.exists(page):
        os.remove(page)
    md_file = open(page,"w")
    print(f'''<div class="container-nhs-pale-grey">\n\n## {project}\n\n</div>\n</br>\n\n''',file=md_file)
    count = 0
    for guide in guides:
        count+=1
        if count%3==0:
            print("<br>")
        print(f'''
        <div class="col-grid">
        <div class="col-grid-content">
        <div class="col-grid-body">
        <h4 class="col-grid-title"><b><a href="{guide[0]}">{guide[1]}</a></b></h4>
        <p class="col-grid-text">{guide[3]}</p>
        </div>
        </div
        ''',file=md_file)

repo_to_url = get_variables('main_variables.json', 'repo_to_url')
project_urls = repo_to_url.values()
''' TODO get Project title + url from:
<div class="row">
                                            
                                            <header class="col-md-16 col-sm-24" aria-hidden="true">
                                                <div class="pre-title">
                                                    
            Project
                <span>of <a href="https://simplifier.net/organization/hl7uk">HL7 UK</a></span>
        
                                                </div>
                                                <h1 class="title">
                                                    <b>HL7 FHIR® UK Core R4 </b>
                                                </h1> 
                                                <div class="description">
                                                    <p>Project for HL7 FHIR® UK Core  R4</p>

                                                </div>
                                            </header>
                                            <div class="menu col-md-14 col-sm-24">
                                                
                                            </div>
                                        </div>
Add it to guides in form dict {project:[guides]} Have two pages, UK Core & NHSE, each with multiple projects. Separate folders with page per project or separate pages with page per project?

for url in project_urls:
    guides = get_guides(url+'/~guides')
    if 'hl7uk' in url:
        guides = sort_ukcore(guides)
    guides_to_html(title, guides)
