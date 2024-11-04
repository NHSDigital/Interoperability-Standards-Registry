
import xml.etree.ElementTree as ET
import json
import os

global_warnings = {}
global_elements = {}
global_ignore = []

def openXMLFile(xml_file,warnings):        
    try:
        tree = ET.parse(xml_file)
    except Exception as e:
        warnings.append("\t\tThe code has an error that needs to be fixed before it can be checked: "+str(e))
        return {}, warnings
    root = tree.getroot()
    return root,warnings


def openJSONFile(file, warnings):
    try:
        with open(file, 'r') as j:
            jsonFile = json.loads(j.read())
    except Exception as e:
        print("\t\tThe code has an error that needs to be fixed before it can be checked:"+ str(e))       
        return {}, warnings
    return jsonFile, warnings


def getXMLElement(xml_file, element):
    try:
        return xml_file.findall('./{*}'+element)[0].get('value')
    except IndexError:
        return


def getJSONElement(jsonFile, element):
    try:
        return jsonFile[element]
    except KeyError:
        return


def printWarnings(warnings, file):
    if warnings:
        print("\t",file)
        for x in warnings:
            print(x)


def list_files(folder):
    ''' gather a list of xml & json files within a folder. Returns xml_files, json_files '''
    xml_files = []
    json_files = []

    for dirpath, dirnames, filenames in os.walk(folder):
        for filename in filenames:
            if filename.endswith('.xml'):
                xml_files.append(os.path.join(dirpath, filename))
            elif filename.endswith('.json'):
                json_files.append(os.path.join(dirpath, filename))
    return xml_files, json_files


def GlobalUpdates(filename, dict_elements, warnings):
    global_elements.update({filename:dict_elements})
    global_warnings.update({filename:warnings})

        
def get_variables(file, attribute):
    warnings = []
    open_file, warnings = openJSONFile(file, warnings)
    global_warnings.update({file:warnings})
    list = getJSONElement(open_file, attribute)
    global_warnings.update({str(file)+':'+str(list):warnings})
    return list
    


'''Create markdown file'''
def code_assets(asset, elements, title, md_file):
    if 'ukcore' in elements['repo_name'].lower():
        list_class = 'ukcore'
    else:
        list_class = 'nhsengland'
    if title == 'ValueSet' or title == 'CodeSystem':
        print(f'''<a href="{elements['repo_name']}/{title}-{elements['id']}" class="child-title">''',file=md_file)
    else:
        print(f'''<a href="{elements['repo_name']}/{elements['id']}" class="child-title">''',file=md_file)
    print(f'''<div class="title">{elements['id']}</div>
<div class="description">''',file=md_file)
    elements.pop('url')
    elements.pop('repo_name')
    elements.pop('id')
    try:
        elements.pop('type') #used previously for sorting profiles and extensions, now not needed
    except KeyError:
        pass
    for element,value in elements.items():
        if not value:
            continue
        if element == 'status':
            print(f'''<span class="status {str(value).lower()}">{str(value)}</span> &nbsp;&nbsp;&nbsp;&nbsp;''', file = md_file)
        else:
            print(f"  {str(value)} &nbsp;&nbsp;&nbsp;&nbsp;", file = md_file)
    print(f"</div>\n</a>", file = md_file)
    return
    

def write_section(title, items):
    page = path+'/'+title+'s.page.md'
    if os.path.exists(page):
        os.remove(page)
    md_file = open(page,"w")

    print(f'''## {title}s\n\n''', file=md_file)
    profile_header = ''
    for asset, elements in items.items():
        if title == 'Profile' and elements['type'] != profile_header:
            if profile_header:
                print('</div>\n', file=md_file)
            profile_header = elements['type']
            print(f'''<a href="https://hl7.org/fhir/R4/{profile_header}" class="project-banner">{profile_header}</a>\n<div class="project-container">''', file=md_file)
        code_assets(asset, elements, title, md_file)
    print(f'''</div>\n\n---\n\n''',file=md_file)
    md_file.close()
    return

if __name__ == "__main__":
   
    xml_files, json_files = list_files('.')
    asset_elements = get_variables('main_variables.json', 'asset_elements')
    repo_to_url = get_variables('main_variables.json', 'repo_to_url')
    
    
    for xml_file in xml_files:
        dict_elements = {}
        warnings = []
        filename = xml_file.split('/')[-1].split('.')[0]
        file, warnings = openXMLFile(xml_file, warnings)
        url_value = getXMLElement(file, 'url')       
        if not url_value:
            continue
        dict_elements.update({'url':url_value})
        type_value = getXMLElement(file, 'type')
        if type_value:
            dict_elements.update({'type':type_value})
        for element in asset_elements:
            value = getXMLElement(file, element)
            if value:
                dict_elements.update({element:value})
        dict_elements.update({'repo_name': repo_to_url[xml_file.split("/")[1]]})
        GlobalUpdates(filename, dict_elements, warnings)
    
    for json_file in json_files:
        dict_elements = {}
        warnings = []
        filename = json_file.split('/')[-1].split('.')[0]
        file, warnings = openJSONFile(json_file, warnings)
        url_value = getJSONElement(file, 'url')
        if not url_value:
            continue
        dict_elements.update({'url':url_value})
        type_value = getJSONElement(file, 'type') 
        if type_value:
            dict_elements.update({'type':type_value})
        for element in asset_elements:
            value = getJSONElement(file, element)
            if value:
                dict_elements.update({element:value})
        dict_elements.update({'repo_name': repo_to_url[json_file.split("/")[1]]})
        GlobalUpdates(filename, dict_elements, warnings)
    
    for key, value in global_warnings.items():
        printWarnings(value, key)
    
    print("Files ignored:")
    for f in global_ignore:
        print(f"\t{f}")
        
    '''Sort assets into seperate dictionaries'''
    codesystems = {}
    conceptmaps = {}
    capabilitystatements = {}
    valuesets = {}
    profiles = {}
    extensions = {}
    searchparameters = {}
    for asset, elements in global_elements.items():
        for k,v in elements.items():
            if k=='url':
                if 'codesystem' in v.lower():
                    codesystems.update({asset:elements})
                elif 'conceptmap' in v.lower():
                    conceptmaps.update({asset:elements})
                elif 'capabilitystatement' in v.lower():
                    capabilitystatements.update({asset:elements})
                elif 'valueset' in v.lower():
                    valuesets.update({asset:elements})
                elif 'searchparameter' in v.lower():
                    searchparameters.update({asset:elements})
                elif 'type' in elements: #ensures that profiles are sorted from examples that contain url
                    #print(f"{k}: {elements['type']}")
                    profiles.update({asset:elements})
    #print(f"PROFILES: {profiles}")
    profiles_temp = profiles.copy()
    for asset, elements in profiles_temp.items():
        if profiles_temp[asset]['type'].lower() == 'extension':
            extensions.update({asset:elements})
            profiles.pop(asset)
    #print(F"PROFILES: {profiles}")
    #print(F"EXTENSIONS: {extensions}")
            
    codesystems = dict(sorted(codesystems.items()))
    valuesets = dict(sorted(valuesets.items()))
    #profiles = dict(sorted(profiles.items(), key=lambda item: (item[1]['type'], item[0], item[0].count('-'))))
    profiles = dict(sorted(profiles.items(), key=lambda item: (
        item[1]['type'],                   # 1. Sort by 'type'
        not item[0].startswith('UKCore'),  # 2. Give priority to 'UKCore' (False < True)
        item[0],                           # 3. Alphabetically by key
        item[0].count('-')                 # 4. By dash count in the key
    )))
    conceptmaps = dict(sorted(conceptmaps.items()))
    capabilitystatements = dict(sorted(capabilitystatements.items()))
    searchparameters = dict(sorted(searchparameters.items()))
    
    path = './guides/Interoperability-Standard-Registry-Guide/About-Interoperability/FHIR-Assets/R4-Assets/'
    
    write_section("Profile", profiles)
    write_section("Extension", extensions)
    write_section("ValueSet", valuesets)
    write_section("CodeSystem", codesystems)
    write_section("ConceptMap", conceptmaps)
    write_section("CapabilityStatement", capabilitystatements)
    write_section("SearchParameter", searchparameters)





